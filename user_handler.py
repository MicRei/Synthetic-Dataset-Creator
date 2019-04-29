"""
File to handle user interactions.
"""

import mutacc_handler as mach
import bamsurgeon_handler as bamh

class UserError(Exception):
    pass


# TODO:
#   Add more arguments in case user wants to use more arguments
def create_mutations_in_bamfile(mutationtype, variationfile, referencefile, bamfile, outputfile=None, nr_procs=1):
    """
    Create a mutation in a BAM file and output it to a new BAM file.

    :param mutationtype:    Mutation type wanted. Mutation argument for BAMsurgeon: addsnv, addindel, addsv.
    :param variationfile:   BED file containing the position/-s to mutate.
    :param referencefile:   Fasta of genome to use as template.
    :param bamfile:         BAM file to mutate
    :param outputfile:      Name of output BAMfile. Default will be appending '.mutated.bam' to the original bamfile.
    :param nr_procs:        Number of processors to use. Default is one (1), but more is recommended.
    :return:
    """
    try:
        if outputfile is None:
            outputfile = bamfile + '.mutated.bam'

        if nr_procs is not int:
            raise UserError("Please use a number to specify the number of threads and not words")
        else:
            bamh.create_mutations(mutationtype, variationfile, referencefile, bamfile, outputfile, nr_procs)
    except UserError as e:
        print('An error occurred with the parameters for BAMSurgeon: ', e)


def import_to_database(case_id, configfile, padding, *args):
    """
    Extracts and imports case into database. Uses either an existing yaml file or creates a new one from args.

    :param case_id:     ID of case; can be either a number or a string of letters.
    :param configfile:  Location of configfile for mutacc.
                        See https://github.com/Clinical-Genomics/mutacc#configuration-file for more information
    :param padding:     Length of padding around desired region.
    :param args:        The 8 additional data needed to create a new case;
                            Sample ID of the sample,
                            Gender of the sample,
                            Sample ID of Mothers sample if applicable, '0' if not,
                            Sample ID of Father of sample if applicable, '0' if not,
                            Location of BAM file,
                            Type of analysis performed,
                            Phenotype of the subject,
                            VCF location

                        For an example, see https://github.com/Clinical-Genomics/mutacc#populate-the-mutacc-database
    :return:
    """
    if args is None or len(args) == 8:
        mach.import_to_database(case_id, configfile, padding, *args)
    else:
        raise UserError('Not enough arguments or too many arguments sent. Please look over them.')


def remove_case_from_database(case_id, configfile):
    """
    Removes specified case from the database.
    :param case_id:     ID of case to remove, NOT sample. Will remove all samples of the specified case.
    :param configfile:  Location of configfile for mutacc.
                        See https://github.com/Clinical-Genomics/mutacc#configuration-file
                        for more information.
    :return:            Removal of case from database
    """
    mach.remove_from_database(case_id, configfile)


def mass_synthesize_and_import_to_database(mutationtype, list_of_variationfiles, list_of_referencefiles,
                                           list_of_bamfiles, list_of_outputfiles, nr_procs, list_of_case_ids,
                                           configfile, *matrix_of_args):
    """
    Create more than one(1) mutated bamfile and import them into the database, one at a time.
    :param mutationtype:            Type of mutation to run on all cases.
    :param list_of_variationfiles:  List of BED files to use on BAM files. Sorted in order of BAM file list.
    :param list_of_referencefiles:  List of fasta genome files to use with BAM files. Sorted in order of BAM file list.
    :param list_of_bamfiles:        List of BAM files to mutate.
    :param list_of_outputfiles:     List of names for mutated BAM files. Sorted in order of BAM file list.
    :param list_of_case_ids:        List of case ID's to be assigned to new cases. Sorted in order of BAM file list.
    :param matrix_of_args:          List containing lists of arguments to use for new data of cases.
                                    Sorted in order of BAM file list.
    :param nr_procs:                Number of processes to use. Default is 1. More is recommended.
    :param configfile:              Location of configfile for mutacc.
                                    See https://github.com/Clinical-Genomics/mutacc#configuration-file
                                    for more information.

    :return:
    """
    mutationtype, nr_procs, configfile = mutationtype, nr_procs, configfile
    matrix = matrix_of_args

    for case in list_of_case_ids:
        case_id = list_of_case_ids(case)
        variationfile = list_of_variationfiles(case)
        referencefile = list_of_referencefiles(case)
        bamfile = list_of_bamfiles(case)
        outputfile = list_of_outputfiles(case)
        args = matrix(case)
        create_mutations_in_bamfile(mutationtype, variationfile, referencefile, bamfile, outputfile, nr_procs)
        import_to_database(case_id, configfile, *args)


def create_dataset(configfile, member, background_bam, background_fastq1, background_fastq2, *args):
    """
    Creates a dataset of the specified case/-s from the database. More information can be found at
        https://github.com/Clinical-Genomics/mutacc#export-datasets-from-the-database

    :param configfile:          Location of configfile for mutacc.
                                See https://github.com/Clinical-Genomics/mutacc#configuration-file for more information
    :param member:              Member to extract from database. Default is to extract all 'affected' cases
    :param background_bam:      Path to BAM file to use as background for the dataset.
    :param background_fastq1:   Path to FastQ file to use as background for the dataset.
    :param background_fastq2:   Path to second FastQ file to use as background for the dataset , if pair-ended.
    :param args:
    :return:
    """
    mach.export_from_database(configfile, member, background_bam, background_fastq1, background_fastq2, args)
