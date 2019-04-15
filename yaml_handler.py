import os
import numpy as np
import re
import sys
import pysam as ps
import yaml
import mutacc as mac
import subprocess as sp



# TODO: Add location of BAMsurgeons function files? Might allow another class to handle it
#   addsnvlocation = 'locate addsnv.py'
#   os.system(addsnvlocation)
#   addindellocation = 'locate addindel.py'
#   os.system(addindellocation)
#   addsvlocation = 'locate addsv.py'
#   os.system(addsvlocation)


class YamlHandler:

    def __init__(self):
        print("Hello from a classy YAML")

    print("HAH")

    # TODO:  call yaml_parse from mutacc
