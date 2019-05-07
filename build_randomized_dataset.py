"""
Module to randomize datasets through mutacc
"""
import subprocess as sp
import re
import pymongo as mongo
import mutacc_handler as muth


# TODO: ADD IN REFERENCE DATA TO THE SYNTHESISED BAM AND FASTQ FILES

def create_randomized_dataset(case_db_configfile, synth_db_configfile, background_bam, background_fastq1,
                              background_fastq2):
    """
    Create a new database to load with random variants to use in a dataset.
    :param case_db_configfile:  Configfile with path to root directory of mutacc.
    :param synth_db_configfile: Configfile with path to root directory of mutacc and name of database for synthesizing.
    :param background_bam:      BAM to use as background for dataset.
    :param background_fastq1:   First FastQ to use as background for dataset
    :param background_fastq2:   Second FastQ to use as background for dataset, pair-ended analysis.
    :return: None, synthesizes a dataset
    """
    mutacc_view = ['mutacc', '--config-file', case_db_configfile, 'db', 'view', '-c', '{}']

    # find all ID's of cases in the database and add them to a list
    cases = re.findall("case_id.*[0-9a-zA-z]", sp.run(mutacc_view, stdout=sp.PIPE).stdout.decode('UTF-8'))

    # strip away everything but the case_id from the fetched strings.
    case_id_list = []
    for case in cases:
        case_id_list.append(case.split("'")[2])

    with open(case_db_configfile, 'r') as config_handle:
        root_dir = re.search("root_dir", config_handle.read()).string.split(" ")[1].strip("\n")

    path_to_import_dir = root_dir + 'imports/'

    mutacc_import = ['mutacc', '--config-file', synth_db_configfile, 'db', 'import']

    # TODO: randomize this! Do not use all cases, but use instead a random number of cases.
    for case in case_id_list:
        mutacc_import.append(path_to_import_dir + case + '_import.mutacc')
        sp.run(mutacc_import)
        mutacc_import.pop()

    muth.export_from_database(synth_db_configfile, background_bam, background_fastq1, background_fastq2)

    with open(synth_db_configfile, 'r') as synth_db_handle:

        servername = re.search("database.*", synth_db_handle.read()).group().split(": ")[1]
        synthesizer_database = mongo.MongoClient()
        synthesizer_database.drop_database(servername)
        synthesizer_database.close()
