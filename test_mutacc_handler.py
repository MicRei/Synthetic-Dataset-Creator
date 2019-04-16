import unittest
import sys

from setuptools.command.test import test

#import mutacc_handler


class TestMutaccHandler(unittest.TestCase):
    def test_something(self):
        self.assertTrue(True)

    def test_YAML_loading(self):
        #yamlfile = self.assertmutacc_handler._create_YAML_file('22655', 'female', 'sample3', '0', './here.bam') # add as arguments --> id, sex, mother, father, bam
        #self.assertis(read('yamlfile', 'r'), msg='Hello there ;)')

if __name__ == '__main__':
    unittest.main()
