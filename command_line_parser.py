import os
import numpy as np
import re
import sys
import pysam as ps
import yaml
import mutacc as mac
import time
import yaml_handler
import argparse


def run():
    command_parser = argparse.ArgumentParser
    