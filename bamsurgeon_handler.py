"""
File to handle bamsurgeon interaction.
"""

import subprocess as sp


# TODO: Parse args in case of more arguments. REMEMBER: addsv does not handle picard.
def create_mutations(mutationtype, variationfile, referencefile, bamfile, outputfile, nr_procs, *args):
    """
        Create mutation based on userinput in bamfile data based on positions given in variationfile and print
         them to outputfile.

        :param variationfile:   BED file specifying position to mutate, optionally with the desired base.
        :param referencefile:   FASTA file containing the genome the sample is mapped against.
        :param bamfile:         BAM file containing the sample reads.
        :param outputfile:      BAM file to store the mutated data.
        :param nr_procs:        Number of processes/threads to run the program with.
        :param args:            Additional arguments, not implemented.
        :return:                None.
        """
    sortedbam = outputfile + '.sorted.bam'

    sp.run(
        [mutationtype + '.py', '-v', variationfile, '-r', referencefile, '-f', bamfile, '-o', outputfile,
         '-p', str(nr_procs), '--maxdepth', '10000'])
    sp.run(['samtools', 'sort', '-@', nr_procs, '-o', sortedbam, outputfile])
    sp.run(['samtools', 'index', '-@', nr_procs, sortedbam])
