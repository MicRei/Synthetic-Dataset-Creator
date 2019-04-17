"""
File to handle bamsurgeon interaction.
"""

import os
import numpy as np
import re
import sys
import pysam as ps
import yaml
import mutacc as mac
import time
import mutacc_handler
import argparse
import subprocess as sp


# TODO:
#   Handle bamsurgeon in this file

# TODO:
#   Add location of BAMsurgeons function files.
#   addsnvlocation = 'locate addsnv.py'
#   os.system(addsnvlocation)
#   addindellocation = 'locate addindel.py'
#   os.system(addindellocation)
#   addsvlocation = 'locate addsv.py'
#   os.system(addsvlocation)


# TODO:
#   run subprocess module with "addsnv  -v REGIONS_TO_MUTATE -r REFERENCE_FASTA -f BAM_FILE -o OUTPUT_FILE"
def create_snv(addsnv_location, variationfile, referencefile, bamfile, outputfile, *args):
    sp.run(['addsnv.py', '-v', 'REGIONS_TO_MUTATE', '-r', 'REFERENCE_FASTA', '-f', 'BAM_FILE', '-o', 'OUTPUT_FILE'])


# TODO:
#   run subprocess module with "addsv  -v REGIONS_TO_MUTATE -r REFERENCE_FASTA -f BAM_FILE -o OUTPUT_FILE"
def create_sv(addsv_location, variationfile, referencefile, bamfile, outputfile, *args):
    sp.run(['addsv.py', '-v', 'REGIONS_TO_MUTATE', '-r', 'REFERENCE_FASTA', '-f', 'BAM_FILE', '-o', 'OUTPUT_FILE'])


# TODO:
#   run subprocess module with "addindel  -v REGIONS_TO_MUTATE -r REFERENCE_FASTA -f BAM_FILE -o OUTPUT_FILE"
def create_indel(addindel_location, variationfile, referencefile, bamfile, outputfile, *args):
    sp.run(['addindel.py', '-v', 'REGIONS_TO_MUTATE', '-r', 'REFERENCE_FASTA', '-f', 'BAM_FILE', '-o', 'OUTPUT_FILE'])
