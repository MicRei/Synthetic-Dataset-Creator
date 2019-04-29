import unittest
import bamsurgeon_handler as bams


class MyTestCase(unittest.TestCase):

    def test_create_mutations(self):
        mutationtype = '/home/mire/miniconda3/envs/py2/bin/addsnv.py'
        variationfile = '/home/mire/PycharmProjects/project_files/mychr17snv1.bed'
        referencefile = '/home/mire/PycharmProjects/fasta_hg38/hg38.fa'
        bamfile = '/home/mire/PycharmProjects/hg38/NA12878twist.sorted.bam'
        outputfile = '/home/mire/PycharmProjects/project_test/bms_output/addsnvtest.bam'
        nr_procs = '30'

        bams.create_mutations(mutationtype, variationfile, referencefile, bamfile, outputfile, nr_procs)


if __name__ == '__main__':
    unittest.main()
