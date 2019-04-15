import os
import numpy as np
import re
import sys
import pysam as ps
import yaml
import mutacc as mac
import subprocess as sp

#TODO:
#   Take in sample_id, sex, mother, father, and bam_file and add them to mutacc database

class YamlHandler:

    def __init__(self):
        print("Hello from a classy YAML")

    # TODO:  call yaml_parse from mutacc
