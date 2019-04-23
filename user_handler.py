"""
File to handle user interactions.
"""

import os
import numpy as np
import re
import sys
import pysam as ps
import time
import mutacc_handler as mach
import bamsurgeon_handler as bamh
import argparse


# TODO:
#   Figure out what arguments to use.
#   Add a parser that reads all arguments and stores them.
#   Allow the stored arguments to be used by the correct function.

# TODO:
#   Function that calls bamsurgeon and creates mutations based on arguments received
def create_mutations_in_bamfile():
    bamh.create_mutations()


# TODO:
#   Function that calls mutacc and adds a bam file and case to the database
def add_case_to_database():
    mach.import_to_database()


# TODO:
#   Function to remove case from database
def remove_case_from_database():
    mach.remove_from_database()


# TODO:
#   Function to create mutation and add it directly to the database
def mass_import_to_database():
    create_mutations_in_bamfile()
    add_case_to_database()


# TODO:
#   Function to retrieve a case from the database and synthesize it
def create_dataset():
    mach.export_from_database()
