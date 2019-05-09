import unittest
import Synthetic_Dataset_Creator.build_randomized_dataset as build_dataset


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
        testlist_3 = ['%', '#', '(', '!', '½', '=', '>']
        testdict_1 = {}
        testdict_2 = {}

        for fq_pairs in range(len(testlist_1)):
            testdict_1[testlist_1[fq_pairs]] = testlist_2[fq_pairs]

        for fq_pairs in range(len(testlist_1)):
            testdict_2[testlist_1[fq_pairs]] = testlist_3[fq_pairs]

        methoddict_1 = build_dataset._pair_reference_fastq_files(testlist_1, testlist_2)
        methoddict_2 = build_dataset._pair_reference_fastq_files(testlist_1, testlist_3)

        self.assertEqual(testdict_1, methoddict_1,
                         "Dictionaries of equal size and containing equal long lists are not equals!")
        self.assertEqual(testdict_1, methoddict_2,
                         "Dictionaries of equal size and containing unequal list lenghts are not equals!")


if __name__ == '__main__':
    unittest.main()
