import unittest
import bamsurgeon_handler as bams


class MyTestCase(unittest.TestCase):
    def test_create_snv(self):
        addsnv_location = '/home/mire/.local/bin/addsnv.py'
        variationfile = '/home/mire/PycharmProjects/project_files/mychr17snv.bed'
        referencefile = '/home/mire/PycharmProjects/project_files/fastadocs/hg19.fa'
        bamfile = '/home/mire/PycharmProjects/project_files/' \
                  '17-1143_S26_R_001_nSCLC_NORMAL.molbar.trimmed.deduped.merged.sorted.bam'
        outputfile = '/home/mire/PycharmProjects/project_files/addsnvtest.bam'
        nr_procs = '30'

        bams.create_snv(addsnv_location, variationfile, referencefile, bamfile, outputfile, nr_procs)

    """

    def test_something(self):
        self.assertEqual(True, False)



    def test_create_sv(self):
        self.assertEqual(True, False)

    def test_create_indel(self):
        self.assertEqual(True, False)
    """


if __name__ == '__main__':
    unittest.main()
