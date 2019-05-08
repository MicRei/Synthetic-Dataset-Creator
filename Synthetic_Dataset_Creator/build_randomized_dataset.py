"""
Module to randomize datasets through mutacc
"""
import subprocess as sp
import re
import pymongo as mongo
from Synthetic_Dataset_Creator import mutacc_handler as muth
import random
from os import listdir


def create_randomized_dataset(case_db_configfile, synth_db_configfile, background_bam, background_fastq1,
                              background_fastq2, reference_data_fq1=None, reference_data_fq2=None):
    """
    Create a new database to load with random variants to use in a dataset.
    :param case_db_configfile:  Configfile with path to root directory of mutacc.
    :param synth_db_configfile: Configfile with path to root directory of mutacc and name of database for synthesizing.
    :param background_bam:      BAM to use as background for dataset.
    :param background_fastq1:   First FastQ to use as background for dataset
    :param background_fastq2:   Second FastQ to use as background for dataset, pair-ended analysis.
    :param reference_data_fq1:  Reference data to add to the sampling pool. FastQ , pairended format.
    :param reference_data_fq2:  Reference data to add to the sampling pool. Complementary list to reference_Data_fq1.
    :return: None, synthesizes a dataset
    """
    case_id_list = _extract_case_ids(case_db_configfile)
    mutacc_import = ['mutacc', '--config-file', synth_db_configfile, 'db', 'import']
    caselist = []
    caselist.extend(case_id_list)

    if reference_data_fq1 is None:
        reference_data_fq1 = []
        reference_data_fq2 = []

    if len(reference_data_fq1) != 0 and len(reference_data_fq2) != 0 \
            and len(reference_data_fq1) == len(reference_data_fq2):
        dict_of_referencedata = _pair_reference_fastq_files(reference_data_fq1, reference_data_fq2)
        caselist.extend(reference_data_fq1)
    else:
        dict_of_referencedata = {}

    if len(caselist) == 1:
        randomized_list = caselist
    else:
        randomized_list = random.sample(caselist, int(len(caselist) * 0.67))

    _create_synthesized_dataset_from_database(background_bam, background_fastq1, background_fastq2, caselist,
                                              mutacc_import, case_db_configfile, randomized_list, synth_db_configfile)

    chosen_references = []
    chosen_references_pair = []
    if len(dict_of_referencedata) != 0:
        for sample in randomized_list:
            if sample in dict_of_referencedata:
                chosen_references.append(reference_data_fq1[reference_data_fq1.index(sample)])
                chosen_references_pair.append(dict_of_referencedata.get(sample))
    else:
        chosen_references = {}

    # TODO: Exclude overlapping fastq data, if present, when merging reference data and synthetic fq's.
    # TODO: Or just use reference data as a dataset? Or use reference data as background?

    root_dir = _get_root_dir_path(synth_db_configfile)
    path_to_synthetic_datasets = root_dir + 'datasets/'
    synthetic_fqs = listdir(path_to_synthetic_datasets)
    if len(chosen_references) > 0:
        for fq_file in range(len(chosen_references)):
            sp.run(['cat', synthetic_fqs[0], chosen_references[fq_file]])
            sp.run(['cat', synthetic_fqs[1], chosen_references_pair[fq_file]])


def _create_synthesized_dataset_from_database(background_bam, background_fastq1, background_fastq2, caselist,
                                              mutacc_import, case_db_configfile, randomized_list, synth_db_configfile):
    root_dir = _get_root_dir_path(case_db_configfile)
    path_to_import_dir = root_dir + 'imports/'

    for case in randomized_list:
        if case in caselist:
            mutacc_import.append(path_to_import_dir + case + '_import.mutacc')
            sp.run(mutacc_import)
            mutacc_import.pop()
    muth.export_from_database(synth_db_configfile, background_bam, background_fastq1, background_fastq2)
    with open(synth_db_configfile, 'r') as synth_db_handle:

        servername = re.search("database.*", synth_db_handle.read()).group().split(": ")[1]
        synthesizer_database = mongo.MongoClient()
        synthesizer_database.drop_database(servername)
        synthesizer_database.close()


def _pair_reference_fastq_files(reference_data_fq1, reference_data_fq2):
    paired_reference_data = {}
    for fq_pairs in range(len(reference_data_fq1)):
        paired_reference_data[reference_data_fq1[fq_pairs]] = reference_data_fq2[fq_pairs]
    return paired_reference_data


def _get_root_dir_path(case_db_configfile):
    with open(case_db_configfile, 'r') as config_handle:
        root_dir = re.search("root_dir", config_handle.read()).string.split(" ")[1].strip("\n")
    return root_dir


def _extract_case_ids(case_db_configfile):
    mutacc_view = ['mutacc', '--config-file', case_db_configfile, 'db', 'view', '-c', '{}']
    cases = re.findall("case_id.*[0-9a-zA-z]", sp.run(mutacc_view, stdout=sp.PIPE).stdout.decode('UTF-8'))
    case_id_list = []
    for case in cases:
        case_id_list.append(case.split("'")[2])
    return case_id_list
