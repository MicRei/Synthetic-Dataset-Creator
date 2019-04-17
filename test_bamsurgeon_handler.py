import unittest
import bamsurgeon_handler as bams


class MyTestCase(unittest.TestCase):
    def test_create_snv(self):
        variationfile = '/home/mire/PycharmProjects/project_files/mychr17snv.bed'
        referencefile = '/home/mire/PycharmProjects/project_files/fastadocs/hg19.fa'
        bamfile = '/home/mire/PycharmProjects/project_files/' \
                  'rawdata/newbam.bam'
        outputfile = '/home/mire/PycharmProjects/project_test/bms_output/addsnvtest.bam'
        nr_procs = '30'

        bams.create_snv(variationfile, referencefile, bamfile, outputfile, nr_procs)


    def test_create_sv(self):
        variationfile = '/home/mire/PycharmProjects/project_files/mychr17snv.bed'
        referencefile = '/home/mire/PycharmProjects/project_files/fastadocs/hg19.fa'
        bamfile = '/home/mire/PycharmProjects/project_files/' \
                  'rawdata/newbam.bam'
        outputfile = '/home/mire/PycharmProjects/project_test/bms_output/addsnvtest.bam'
        nr_procs = '30'

        bams.create_snv(variationfile, referencefile, bamfile, outputfile, nr_procs)

    def test_create_indel(self):
        variationfile = '/home/mire/PycharmProjects/project_files/mychr17snv.bed'
        referencefile = '/home/mire/PycharmProjects/project_files/fastadocs/hg19.fa'
        bamfile = '/home/mire/PycharmProjects/project_files/' \
                  'rawdata/newbam.bam'
        outputfile = '/home/mire/PycharmProjects/project_test/bms_output/addsnvtest.bam'
        nr_procs = '30'

        bams.create_snv(variationfile, referencefile, bamfile, outputfile, nr_procs)


if __name__ == '__main__':
    unittest.main()
