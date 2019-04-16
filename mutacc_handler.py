"""
File to handle mutacc interaction.
"""

import os
import numpy as np
import re
import sys
import pysam as ps
import yaml
import mutacc as mac
import subprocess as sp
from pathlib import Path


class MutaccError(Exception):
    pass


# TODO:
#   Add the YAML file to mutacc database.

def import_to_database(case_id, *args):
    """
    Function to create a new data set, or use existing data, and insert it into the mutacc database

    :param case_id: path to a yamlfile with the correct structure or the ID of a new case
    :param args: the 8 additional data needed to create a new case;
                    sample_id, sex, mother, father, bam, analysis, phenotype, variants
    :return: None
    """

    try:
        if type(case_id) is str:
            yaml_path = Path(case_id)
            if yaml_path.is_file():
                with open(case_id, 'r') as yaml_case:
                    # TODO: Add --config-file <config_file> and
                    #  --padding NUMBER to extract subprocess. Make arguments in extract dynamic.
                    sp.run(['mutacc', '--root-dir', 'mutacc_tests', 'extract', '--case', yaml_case.name])
                    # TODO: Add a config file or rootdir to mutacc import subprocess
                    sp.run(['mutacc', 'db', 'import', 'root_dir/imports/' + yaml_case.name + '.mutacc'])
                    if not yaml_case.readable():
                        raise MutaccError("No read permission granted.")
            else:
                raise MutaccError("No such file exists.")
        elif len(args) == 8:
            new_data = [case_id]

            for data in args:
                new_data.append(data)
            _create_yaml_file(*new_data)
        else:
            raise MutaccError("Not enough args sent to import. Please supplement your data")

    except Exception as e:
        print("Something went wrong during import: ", e)


# TODO:
#   Return wanted sample from database
#   use subprocess module for command line "mutacc --config-file <config.yaml> db export -m affected -c '{}'"
# def export_from_database(case):


# TODO: export case and if that is successful, call create_dataset_from_case


# TODO:
#   Create the dataset from exported case
#   use subprocess module for command line
#   "mutacc --config-file <config_file> synthesize -b <bam> -f <fastq1_child> -f2 <fastq2_child> -q child_query.mutacc"
# def create_dataset_from_case(data):


# TODO:
#   Remove specific case form database
#   use subprocess module for command line "mutacc --config-file <config.yaml> db remove <case_id>"
# def remove_from_database(case):


# TODO:
#  Check mutacc config file or create one.
#   If config file exist, use it. Else, create default.
# def config_file_handler(file):


def _create_yaml_file(case_id, sample_id, sex, mother, father, bam, analysis, phenotype, variants):
    """
        Internal function to create a YAML document from provided data.
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
