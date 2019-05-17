"""
Module to randomize datasets through mutacc
"""
import subprocess as sp
import re
import pymongo as mongo
from program_handlers import mutacc_handler as muth
import random
from os import listdir
from yaml import safe_load
from pathlib import Path


class BuildingError(Exception):
    pass


def create_randomized_dataset(case_db_configfile, synth_db_configfile, background_bam, background_fastq1,
                              background_fastq2, reference_data_fq1=None, reference_data_fq2=None):
    """
    Create a new database to load with random variants to use in a dataset.

    :param case_db_configfile:  Configfile with path to root directory of mutacc.
    :param synth_db_configfile: Configfile with path to root directory of mutacc and name of database for synthesizing.
    :param background_bam:      BAM to use as background for dataset.
    :param background_fastq1:   First FastQ to use as background for dataset.
    :param background_fastq2:   Second FastQ to use as background for dataset, pair-ended analysis.
    :param reference_data_fq1:  Reference data to add to the sampling pool. FastQ , pairended format.
                                    Either a file with a 1 (one) file per row or a list of filenames.
    :param reference_data_fq2:  Reference data to add to the sampling pool.
                                    Complementary list to reference_data_fq1 in the same format as reference_data_1.
    :return: None, synthesizes a dataset
    """
    case_id_list = _extract_case_ids(case_db_configfile)
    caselist = []
    caselist.extend(case_id_list)
    if reference_data_fq1 is None:
        reference_data_fq1 = []
        reference_data_fq2 = []
    elif Path(reference_data_fq1).is_file() is True:
        reference_data_fq1 = [reference_data_fq1, ]
        reference_data_fq2 = [reference_data_fq2, ]
    else:
        raise BuildingError('Reference data is not a valid file or list. Please see API for proper usage.')

    if len(reference_data_fq1) != 0 and len(reference_data_fq1) == len(reference_data_fq2):
        dict_of_referencedata = _pair_reference_fastq_files(reference_data_fq1, reference_data_fq2)
        caselist.extend(reference_data_fq1)
    else:
        dict_of_referencedata = {}

    if len(caselist) == 1:
        randomized_list = caselist
    else:
        randomized_list = random.sample(caselist, int(len(caselist) * 0.67))

    _create_synthesized_dataset_from_database(background_bam, background_fastq1, background_fastq2, case_id_list,
                                              case_db_configfile, randomized_list, synth_db_configfile)

    chosen_references = []
    chosen_references_pair = []
    if len(dict_of_referencedata) != 0:
        for sample in randomized_list:
            if sample in dict_of_referencedata:
                chosen_references.append(reference_data_fq1[reference_data_fq1.index(sample)])
                chosen_references_pair.append(dict_of_referencedata.get(sample))
    else:
        chosen_references = {}

    root_dir = _get_root_dir_path(synth_db_configfile)
    path_to_synthetic_datasets = root_dir + 'synthetics/'
    if not Path(path_to_synthetic_datasets).is_dir():
        Path(path_to_synthetic_datasets).mkdir()
    path_to_mutacc_datasets = root_dir + 'datasets/'
    synthetic_fqs = listdir(path_to_mutacc_datasets)

    if len(chosen_references) > 0:
        for fq_file in range(len(chosen_references)):
            with open(path_to_synthetic_datasets + Path(chosen_references[fq_file]).name + '_' + str(fq_file)
                      + '.dataset_1.fastq.gz', 'w') as synthetic_fq_1, open(
                path_to_synthetic_datasets + Path(chosen_references_pair[fq_file]).name + '_' + str(fq_file)
                    + '.dataset_2.fastq.gz', 'w') as synthetic_fq_2:
                sp.run(['cat', path_to_mutacc_datasets + synthetic_fqs[0], chosen_references[fq_file]],
                       stdout=synthetic_fq_1)
                sp.run(['cat', path_to_mutacc_datasets + synthetic_fqs[1], chosen_references_pair[fq_file]],
                       stdout=synthetic_fq_2)

                print(synthetic_fq_1.name)
                print(synthetic_fq_2.name)

    else:
        sp.run(['cp', path_to_mutacc_datasets + synthetic_fqs[0], path_to_synthetic_datasets + synthetic_fqs[0]])
        sp.run(['cp', path_to_mutacc_datasets + synthetic_fqs[1], path_to_synthetic_datasets + synthetic_fqs[1]])
    sp.run(['rm', '-v', path_to_mutacc_datasets + synthetic_fqs[0]])
    sp.run(['rm', '-v', path_to_mutacc_datasets + synthetic_fqs[1]])


def _create_synthesized_dataset_from_database(background_bam, background_fastq1, background_fastq2, caselist,
                                              case_db_configfile, randomized_list, synth_db_configfile):
    """
    :param background_bam:      BAM to use as background for dataset.
    :param background_fastq1:   First FastQ to use as background for dataset
    :param background_fastq2:   Second FastQ to use as background for dataset, pair-ended analysis.
    :param caselist:            List if cases from mutacc database to include in dataset.
    :param case_db_configfile:  Configfile with path to root directory of mutacc.
    :param randomized_list:     List with randomized cases and data to create a dataset from.
    :param synth_db_configfile: Configfile with path to root directory of mutacc and name of database for synthesizing.
    :return:
    """
    mutacc_import = ['mutacc', '--config-file', synth_db_configfile, 'db', 'import']
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
    """
    Pairs FQ files with each other. Makes a dictionary with names in FastQ1 file as keys and FastQ2 file as values.
    :param reference_data_fq1:
    :param reference_data_fq2:
    :return:
    """
    paired_reference_data = {}
    for fq_pairs in range(len(reference_data_fq1)):
        paired_reference_data[reference_data_fq1[fq_pairs]] = reference_data_fq2[fq_pairs]
    return paired_reference_data


def _get_root_dir_path(case_db_configfile):
    """
    :param case_db_configfile:  Extracts the root directory from a configfile
    :return:
    """
    with open(case_db_configfile, 'r') as config_handle:
        root_dir = safe_load(config_handle).get('root_dir')
    return root_dir


def _extract_case_ids(case_db_configfile):
    """
    :param case_db_configfile: Configfile containing the path to root-dir for mutacc mongo database.
    :return:
    """
    mutacc_view = ['mutacc', '--config-file', case_db_configfile, 'db', 'view', '-c', '{}']
    cases = re.findall("case_id.*[0-9a-zA-z]", sp.run(mutacc_view, stdout=sp.PIPE).stdout.decode('UTF-8'))
    case_id_list = []
    for case in cases:
        case_id_list.append(case.split("'")[2])
    return case_id_list
