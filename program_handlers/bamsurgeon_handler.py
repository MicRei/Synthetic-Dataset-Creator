"""
File to handle bamsurgeon interaction.
"""

import subprocess as sp
from pathlib import Path


# TODO: Parse args in case of more arguments. REMEMBER: addsv does not handle picard.
def create_mutations(mutationtype, variationfile, referencefile, bamfile, outputfile, nr_procs):  # *args
    """
        Create mutation based on user input in bamfile data based on positions given in variationfile and print
         them to outputfile.

        :param mutationtype:    mutation type to perform: addsnv, addsv, or addindel;
                                    addsnv adds a single nucleotide variance
                                    addsv adds a structural variance
                                    addindel adds the specified nucleotides or deletes the specified region.
                                    See https://github.com/adamewing/bamsurgeon for better specifications.
        :param variationfile:   BED file specifying position to mutate, optionally with the desired base.
        :param referencefile:   FASTA file containing the genome the sample is mapped against.
        :param bamfile:         BAM file containing the sample reads.
        :param outputfile:      BAM file to store the mutated data.
        :param nr_procs:        Number of processes/threads to run the program with.
        #:param args:            Additional arguments, not implemented.
        :return:                None.
        """

    sp.run([mutationtype + '.py',
            '-v', variationfile,
            '-r', referencefile,
            '-f', bamfile,
            '-o', outputfile,
            '-p', str(nr_procs),
            '--maxdepth', '10000'])

    if Path(outputfile).is_file() is True:
        sp.run(['samtools', 'sort', '-@', str(nr_procs), '-o', outputfile, outputfile])
        sp.run(['samtools', 'index', '-@', str(nr_procs), outputfile])
