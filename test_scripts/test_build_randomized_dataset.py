import unittest
import Synthetic_Dataset_Creator.build_randomized_dataset as build_dataset
import random


class MyTestCase(unittest.TestCase):

    def test_get_root_dir(self):
        self.assertEqual(
            build_dataset._get_root_dir_path(
                '/home/mire/PycharmProjects/project_test/mutacc_config_files/mutacc_config.yaml'),
            '/home/mire/PycharmProjects/project_test/mutacc_tests/')

    def test_extract_case_ids(self):
        caselist = build_dataset._extract_case_ids(
            '/home/mire/PycharmProjects/project_test/mutacc_config_files/mutacc_config.yaml')
        print(caselist)
        self.assertIsNotNone(caselist)
        self.assertTrue('hannahmontana' in caselist)

    def test_pair_reference_fastq_files(self):
        testlist_1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']
        testlist_2 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', ',11', '12', '13', '14', '15', '16']
        testdict_1 = {}

        for fq_pairs in range(len(testlist_1)):
            testdict_1[testlist_1[fq_pairs]] = testlist_2[fq_pairs]

        methoddict_1 = build_dataset._pair_reference_fastq_files(testlist_1, testlist_2)

        self.assertEqual(testdict_1, methoddict_1,
                         "Dictionaries of equal size and containing equal long lists are not equals!")

    def test_create_synthesized_dataset_from_database(self):
        background_bam = '/home/mire/PycharmProjects/project_files/NA12878_mybam.sorted.bam'
        background_fastq1 = '/home/mire/PycharmProjects/project_test/mutacc_tests/reads/57742/sample32/mutacc_NA12878_mybam_R1.fastq.gz'
        background_fastq2 = '/home/mire/PycharmProjects/project_test/mutacc_tests/reads/57742/sample32/mutacc_NA12878_mybam_R2.fastq.gz'
        caselist = build_dataset._extract_case_ids(
            '/home/mire/PycharmProjects/project_test/mutacc_config_files/mutacc_config.yaml')
        case_db_configfile = '/home/mire/PycharmProjects/project_test/mutacc_config_files/mutacc_config.yaml'
        synth_db_configfile = '/home/mire/PycharmProjects/project_test/mutacc_config_files/mutacc_synthDB_config.yaml'

        randomized_list = random.sample(caselist, int(len(caselist) * 0.67))

        build_dataset._create_synthesized_dataset_from_database(background_bam, background_fastq1, background_fastq2,
                                                                caselist,
                                                                case_db_configfile, randomized_list,
                                                                synth_db_configfile)
        # build_dataset._create_synthesized_dataset_from_database(background_bam, background_fastq1, background_fastq2,
        #                                                         caselist,
        #                                                         case_db_configfile, caselist,
        #                                                         synth_db_configfile)
        # self.assertNotEqual(caselist, randomized_list)


if __name__ == '__main__':
    unittest.main()
