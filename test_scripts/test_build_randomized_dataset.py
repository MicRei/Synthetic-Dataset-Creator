import unittest
import Synthetic_Dataset_Creator.build_randomized_dataset as build_dataset


class MyTestCase(unittest.TestCase):
    # def test_something(self):
    #     self.assertEqual(True, False)

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

    def test_pair_reference_fastq_files(self):


if __name__ == '__main__':
    unittest.main()
