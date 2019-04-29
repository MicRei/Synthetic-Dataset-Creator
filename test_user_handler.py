import unittest
import user_handler as userh


class MyTestCase(unittest.TestCase):

    def test_import_to_database(self):
        print("Testing import_to_database")

        userh.import_to_database('98875', '/home/mire/PycharmProjects/project_test/mutacc_config.yaml', '160',
                                 'sample69', 'female', '0', '0',
                                 '/home/mire/PycharmProjects/project_test/NA12878_mybam.sorted.bam', 'heart',
                                 'affected', '/home/mire/PycharmProjects/project_test/testcases/57746.vcf')
        print("Finished import_to_database")

    def test_remove_case_from_database(self):
        print("Testing remove_to_database")
        userh.remove_case_from_database('98875', '/home/mire/PycharmProjects/project_test/mutacc_config.yaml')
        print("Finished remove_to_database")


if __name__ == '__main__':
    unittest.main()
