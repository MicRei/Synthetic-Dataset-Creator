"""
File to handle mutacc interaction.
"""
import yaml
import subprocess as sp
from pathlib import Path


class MutaccError(Exception):
    pass


# TODO:
#   Add the YAML file to mutacc database.

def import_to_database(case_id, configfile, *args):
    """
    Function to create a new data set, or use existing data, and insert it into the mutacc database

    :param case_id:     path to a yamlfile with the correct structure or the ID of a new case
    :param configfile:  config file containing the root directory of mutaccfiles
    :param args:        the 8 additional data needed to create a new case;
                            sample_id, sex, mother, father, bam, analysis, phenotype, variants
    :return:            None
    """

    try:
        if type(case_id) is str and Path(case_id).is_file():
            with open(case_id, 'r') as yaml_case:
                if not yaml_case.readable():
                    raise MutaccError("No read permission granted.")
                else:
                    print("Importing into database")
                    # TODO: Add --config-file <config_file> and
                    #  --padding NUMBER to extract subprocess. Make arguments in extract dynamic.
                    _mutacc_extract_and_import(configfile, yaml_case.name)
                    # TODO: Add a config file or rootdir to mutacc import subprocess
        elif len(args) == 8:
            new_data = [case_id]

            for data in args:
                new_data.append(data)
            file_name = _create_yaml_file(*new_data)
            _mutacc_extract_and_import(configfile, file_name)

        else:
            raise MutaccError("Not enough args sent to import or no such file exists. Please supplement your data")

    except Exception as e:
        print("Something went wrong during import: ", e)


# TODO: Add --config-file <config_file> and
#  --padding NUMBER to extract subprocess. Make arguments in extract dynamic.
# TODO: Add a config file or rootdir to mutacc import subprocess
def _mutacc_extract_and_import(configfile, filename):
    """
    Internal function to handle mutacc data extraction and import to database

    :param configfile:      the config file containing the root directory of mutaccfiles
    :param filename:        The name of the case file
    :return:                None
    """
    sp.run(['mutacc', '--config-file', configfile, 'extract', '--case', filename])
    sp.run(['mutacc', 'db', 'import', '/.../root_dir/imports/' + filename + '.mutacc'])


# TODO:
#   Return wanted sample from database and Create the dataset from exported case
#   Add more options or make options dynamic?
#   Make config file dynamic
def export_from_database(case):
    sp.run(['mutacc', '--config-file', './mutacc_config.yaml', 'db', 'export', '-m', 'affected', '-c', '{}'])
    sp.run(['mutacc', '--config-file', './mutacc_config.yaml', 'synthesize', '-b', '<bam>', '-f', '<fastq1_child>', '-f2',
            '<fastq2_child>', '-q', 'child_query.mutacc'])


# TODO:
#   Remove specific case form database
#   Make config file dynamic
def remove_from_database(case):
    sp.run(['mutacc', '--config-file', './mutacc_config.yaml', 'db', 'remove', case])


# TODO:
#  Check mutacc config file or create one.
#   If config file exist, use it. Else, create default.
# def config_file_handler(file):


def _create_yaml_file(case_id, sample_id, sex, mother, father, bam, analysis, phenotype, variants):
    """
    Internal function to create a YAML document from provided data.

    :param case_id:     name of the case
    :param sample_id:   name for the sample
    :param sex:         gender of patient
    :param mother:      sample id of mother, if applicable
    :param father:      sample id of father, if applicable
    :param bam:         path to bamfile containing reads for patient
    :param analysis:    analysis type performed on patients data
    :param phenotype:   phenotype of patient (affected or unaffected)
    :param variants:    path to variantfile patient
    :return:            The name of the created file
    """
    if case_id is str:
        create_file = case_id + ".yaml"
    else:
        create_file = str(case_id) + ".yaml"

    print("Created file: " + create_file)

    with open(create_file, 'w') as yamlfile:
        try:
            yaml.dump({'case': {'case_id': case_id}, 'samples': [{'sample_id': sample_id, 'analysis_type': analysis,
                                                                  'sex': sex, 'mother': mother, 'father': father,
                                                                  'bam_file': bam, 'phenotype': phenotype}],
                       'variants': variants}, yamlfile)
        except yaml.YAMLError as exc:
            print('Error writing yaml object: ', exc)
            raise MutaccError("Yaml creation error")

    return create_file
