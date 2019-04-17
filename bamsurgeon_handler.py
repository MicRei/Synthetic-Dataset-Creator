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
#   Add more arguments if desired by the user
def create_snv(variationfile, referencefile, bamfile, outputfile, nr_procs, *args):
    sp.run(
        ['addsnv.py', '-v', variationfile, '-r', referencefile, '-f', bamfile, '-o', outputfile,
         '-p', nr_procs, '--maxdepth', '10000'])


# TODO:
#   Add more arguments if desired by the user
def create_sv(variationfile, referencefile, bamfile, outputfile, nr_procs, *args):
    print("HEllo from indel)")
    sp.run(['addsnv.py', '-v', variationfile, '-r', referencefile, '-f', bamfile, '-o', outputfile, '-p',
            nr_procs, '--maxdepth', '10000'])


# TODO:
#   Add more arguments if desired by the user
def create_indel(variationfile, referencefile, bamfile, outputfile, nr_procs, *args):
    print("HEllo from indel)")
    sp.run(
        ['addsnv.py', '-v', variationfile, '-r', referencefile, '-f', bamfile, '-o', outputfile, '-p',
         nr_procs, '--maxdepth', '10000'])
