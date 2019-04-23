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
def create_mutations_in_bamfile(mutationtype, variationfile, referencefile, bamfile, outputfile, nr_procs):
    bamh.create_mutations(mutationtype, variationfile, referencefile, bamfile, outputfile, nr_procs)


# TODO:
#   Function that calls mutacc and adds a bam file and case to the database
def import_to_database(case_id, configfile, *args):
    mach.import_to_database(case_id, configfile, *args)


# TODO:
#   Function to remove case from database
def remove_case_from_database(case_id):
    mach.remove_from_database(case_id)


# TODO:
#   Function to create mutation and add it directly to the database
def mass_import_to_database(mutationtype, list_of_variationfiles, list_of_referencefiles, list_of_bamfiles,
                            list_of_outputfiles, nr_procs, list_of_case_ids, configfile, *matrix_of_args):
    mutationtype, nr_procs, configfile = mutationtype, nr_procs, configfile

    # TODO: loop through all the files below and call create_mutations + import_to_database for each file/case.

    for case in list_of_case_ids:
        case_id = list_of_case_ids(case)
        variationfile = list_of_variationfiles(case)
        referencefile = list_of_referencefiles(case)
        bamfile = list_of_bamfiles(case)
        outputfile = list_of_outputfiles(case)
        args = matrix_of_args(case)
        create_mutations_in_bamfile(mutationtype, variationfile, referencefile, bamfile, outputfile, nr_procs)
        import_to_database(case_id, configfile, *args)


# TODO:
#   Function to retrieve a case from the database and synthesize it
def create_dataset():
    mach.export_from_database()
