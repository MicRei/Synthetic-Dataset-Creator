"""
File to handle bamsurgeon interaction.
"""

import subprocess as sp


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
    sp.run(
        [mutationtype, '-v', variationfile, '-r', referencefile, '-f', bamfile, '-o', outputfile,
         '-p', nr_procs, '--maxdepth', '10000'])


# TODO:
#   Add more arguments if desired by the user
def create_snv(variationfile, referencefile, bamfile, outputfile, nr_procs, *args):
    """
    Create new single nucleotide variations in bamfile data based on positions given in variationfile and print
     them to outputfile.

    :param variationfile:   BED file specifying position to mutate, optionally with the desired base.
    :param referencefile:   FASTA file containing the genome the sample is mapped against.
    :param bamfile:         BAM file containing the sample reads.
    :param outputfile:      BAM file to store the mutated data.
    :param nr_procs:        Number of processes/threads to run the program with.
    :param args:            Additional arguments, not implemented.
    :return:                None.
    """
    sp.run(
        ['addsnv.py', '-v', variationfile, '-r', referencefile, '-f', bamfile, '-o', outputfile,
         '-p', nr_procs, '--maxdepth', '10000'])


# TODO:
#   Add more arguments if desired by the user
def create_sv(variationfile, referencefile, bamfile, outputfile, nr_procs, *args):
    """
    Create new structural variations in bamfile data based on positions given in variationfile and print
     them to outputfile. Very time consuming.

    :param variationfile:   BED file specifying position or region to mutate, with desired mutation type,
                            allelic fraction, and desired bases mutate to specified.
    :param referencefile:   FASTA file containing the genome the sample is mapped against.
    :param bamfile:         BAM file containing the sample reads.
    :param outputfile:      BAM file to store the mutated data.
    :param nr_procs:        Number of processes/threads to run the program with.
    :param args:            Additional arguments, not implemented.
    :return:                None.
    """
    sp.run(['addsnv.py', '-v', variationfile, '-r', referencefile, '-f', bamfile, '-o', outputfile, '-p',
            nr_procs, '--maxdepth', '10000'])


# TODO:
#   Add more arguments if desired by the user
def create_indel(variationfile, referencefile, bamfile, outputfile, nr_procs, *args):
    """
    Create inserts and deletions in bamfile data based on positions given in variationfile and print
     them to outputfile.

    :param variationfile:   BED file specifying position or region to mutate, with the desired mutation type
                            and, for insertions, base specified.
    :param referencefile:   FASTA file containing the genome the sample is mapped against.
    :param bamfile:         BAM file containing the sample reads.
    :param outputfile:      BAM file to store the mutated data.
    :param nr_procs:        Number of processes/threads to run the program with.
    :param args:            Additional arguments, not implemented.
    :return:                None.
    """
    sp.run(
        ['addsnv.py', '-v', variationfile, '-r', referencefile, '-f', bamfile, '-o', outputfile, '-p',
         nr_procs, '--maxdepth', '10000'])
