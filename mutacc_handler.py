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


class MutaccError(Exception):
    pass


# TODO:
#   #   Take in sample_id, sex, mother, father, and bam_file and create a YAML file.
#   use subprocess module for command line "mutacc --config-file <config_file> extract --padding 600 --case <case_file>"
#
def create_YAML_file(id, sex, mother, father, bam):


# TODO:
#   Add the YAML file to mutacc database.
#   use subprocess module for command line "mutacc db import /.../root_dir/imports/<case_id>.mutacc"
def import_to_database(id, sex, mother, father, bam):
    # TODO:
    #   Call create_YAML_file with args and then import to database.


# TODO:
#   Return wanted sample from database
#   use subprocess module for command line "mutacc --config-file <config.yaml> db export -m affected -c '{}'"
def export_from_database(case):
    # TODO: export case and if that is successful, call create_dataset_from_case


# TODO:
#   Create the dataset from exported case
#   use subprocess module for command line
#   "mutacc --config-file <config_file> synthesize -b <bam> -f <fastq1_child> -f2 <fastq2_child> -q child_query.mutacc"
def create_dataset_from_case(data):


# TODO:
#   Remove specific case form daatabase
#   use subprocess module for command line "mutacc --config-file <config.yaml> db remove <case_id>"
def remove_from_database(case):


# TODO:
#  Check mutacc config file or create one.
#   If config file exist, use it. Else, create default.
def config_file_handler(file):
