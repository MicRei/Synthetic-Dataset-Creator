import unittest
import sys
import os

from setuptools.command.test import test

import mutacc_handler


class TestMutaccHandler(unittest.TestCase):
    def test_something(self):
        self.assertTrue(True)

    def test_YAML_loading(self):
        caseID = 57744
        sample_id = 'sample32'
        sex = 'male'
        mother = '0'
        father = '0'
        bam = './here.bam'
        analysis = 'TP53'
        phenotype = 'affected'
        variants = './my.vcf'

        mutacc_handler._create_YAML_file(caseID, sample_id, sex, mother, father, bam, analysis, phenotype, variants)
        with open('test.yaml', 'r') as yaml_handle:
            self.assertEqual(yaml_handle.readline(), "case:\n", msg='Hello there ;)')
            self.assert

if __name__ == '__main__':
    unittest.main()
