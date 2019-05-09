import unittest
from pathlib import Path
from Synthetic_Dataset_Creator import mutacc_handler

test_path = '/home/mire/PycharmProjects/project_test/testfiles/'


class TestMutaccHandler(unittest.TestCase):

    # def test_YAML_loading_with_proper_data(self):
    #     print("Testing Function of yaml loader: ", end="")
    #     case_id = 'test'
    #     sample_id = 'sample32'
    #     sex = 'male'
    #     mother = '0'
    #     father = '0'
    #     bam = './here.bam'
    #     analysis = 'TP53'
    #     phenotype = 'affected'
    #     variants = './my.vcf'
    #
    #     mutacc_handler._create_yaml_file(case_id, sample_id, sex, mother, father, bam, analysis, phenotype, variants)
    #     with open('test.yaml', 'r') as yaml_handle:
    #         self.assertEqual(yaml_handle.readline(), "case:\n", msg='Hello there ;)')
    #     print()
    #
    # def test_import_to_database_using_new_data(self):
    #     print("Testing with new data: ", end="")
    #     case_id = '23423'
    #     sample_id = 'sample59'
    #     sex = 'female'
    #     mother = '0'
    #     father = '0'
    #     bam = './NA12878_mybam.sorted.bam'
    #     analysis = 'TP53'
    #     phenotype = 'affected'
    #     variants = './57742.vcf'
    #     configfile = './mutacc_config_files/mutacc_config.yaml'
    #     padding = '160'
    #
    #     mutacc_handler.import_to_database(case_id, configfile, padding, sample_id, sex, mother, father, bam, analysis,
    #                                       phenotype,
    #                                       variants)
    #     with open('test.yaml', 'r') as yaml_handle:
    #         self.assertEqual(yaml_handle.readline(), "case:\n", msg='Hello there ;)')
    #     print()
    #
    # def test_import_to_database_using_file(self):
    #     print("Testing with file: ", end="")
    #     mutacc_handler.import_to_database('test.merged.deduped.sorted.pileup.yaml', './mutacc_config_files/mutacc_config.yaml', '150')
    #     file = Path('test.merged.deduped.sorted.pileup.yaml')
    #     if file.is_file():
    #         with open('test.merged.deduped.sorted.pileup.yaml', 'r') as yaml_handle:
    #             self.assertEqual(yaml_handle.readline(), "case:\n", msg='Hello there ;)')
    #         print()
    #     else:
    #         print("No such file")

    def test_export_from_database(self):
        print("============================TESTING EXPORT======================")
        mutacc_handler.export_from_database('./mutacc_config_files/mutacc_config.yaml',
                                            background_bam=test_path + 'NA12878west.sorted.bam',
                                            background_fastq1=test_path + 'mutacc_NA12878_mybam_R1.fastq.gz',
                                            background_fastq2=test_path + 'mutacc_NA12878_mybam_R2.fastq.gz')
        print("============================TESTING EXPORT FINISHED======================")


if __name__ == '__main__':
    unittest.main()
