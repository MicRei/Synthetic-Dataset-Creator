import unittest
from Synthetic_Dataset_Creator import user_handler as userh


# FIXME: User mutacc and bamsurgeon tests to test the program instead of writing your own.
#       Why reinvent the wheel, right?
class MyTestCase(unittest.TestCase):
    test_path = '/home/mire/PycharmProjects/project_test/testfiles/'

    def test_create_dataset(self):
        print('Testing create dataset')

        configfile = '/home/mire/PycharmProjects/project_test/mutacc_config.yaml'
        member = 'affected'
        back_bam = '/home/mire/PycharmProjects/project_test/NA12878_mybam.sorted.bam'
        back_f1 = './mutacc_tests/reads/98875/sample69/mutacc_NA12878_mybam_R1.fastq.gz'
        back_f2 = './mutacc_tests/reads/98875/sample69/mutacc_NA12878_mybam_R2.fastq.gz'

        userh.create_dataset(configfile, back_bam, back_f1, back_f2)

        print('Finished create dataset')

    def setUp(self):
        userh.import_to_database('98875', '/home/mire/PycharmProjects/project_test/mutacc_config.yaml', '160',
                                 'sample69', 'female', '0', '0',
                                 '/home/mire/PycharmProjects/project_test/NA12878_mybam.sorted.bam', 'heart',
                                 'affected', '/home/mire/PycharmProjects/project_test/testcases/57746.vcf')

    def tearDown(self):
        userh.remove_case_from_database('98875', '/home/mire/PycharmProjects/project_test/mutacc_config.yaml')


if __name__ == '__main__':
    unittest.main()
