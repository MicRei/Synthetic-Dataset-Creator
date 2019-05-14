"""
File to handle user interactions.
"""
from program_handlers import build_randomized_dataset as build_dataset
from program_handlers import mutacc_handler as mach
from program_handlers import bamsurgeon_handler as bamh
import sys


class UserError(Exception):
    pass


def main():
    try:
        if sys.argv[1] == 'create_mutations':
            if 6 <= len(sys.argv) < 9:
                print(sys.argv[2 - len(sys.argv)])
                print('\x1b[33m' + 'MUTANTS ARISE!' + '\x1b[0m')
            else:
                raise UserError('\x1b[33m' + "Number of arguments for create_mutations are incorrect.\n"
                                             "Should be 4(four) to 6(six) arguments:\n" + '\x1b[0m'
                                + '\x1b[1;34m' + "mutationtype\n"
                                                 "variationfile\n"
                                                 "referencefile\n"
                                                 "bamfile\n"
                                                 "(OPTIONAL) outputfile; default is None\n"
                                                 "(OPTIONAL) number of processes; default is 1(one)" + '\x1b[0m')

        elif sys.argv[1] == 'mass_mutate':
            if 9 <= len(sys.argv) < 13:
                print('\x1b[33m' + "MORE MUTANTS THAN THE WORLD CAN HANDLE!!! MOAHAHAHA!" + '\x1b[0m')
            else:
                raise UserError('\x1b[33m' + "Number of arguments for mass_mutate are incorrect.\n"
                                             "Should be 7(seven) to 12(twelve) arguments:\n" + '\x1b[0m'
                                + '\x1b[1;34m' + "mutationtype\n"
                                                 "configfile\n"
                                                 "padding\n"
                                                 "list of variationfiles\n"
                                                 "list of referencefiles\n"
                                                 "list of bamfiles\n"
                                                 "list of case_ids for each bamfile imported to the database\n"
                                                 "(OPTIONAL) list if outputfiles; default is None\n"
                                                 "(OPTIONAL) number of processes; default is 1(one)" + '\x1b[0m')

        elif sys.argv[1] == 'import':
            if 5 <= len(sys.argv) < 14:
                print('\x1b[33m' + "Scotty beaming you up!" + '\x1b[0m')
            else:
                raise UserError('\x1b[33m' + "Number of arguments for import are incorrect.\n"
                                             "Should be 3(three) to 13(thirteen) arguments:\n" + '\x1b[0m'
                                + '\x1b[1;34m' + "case_id\n"
                                                 "configfile\n"
                                                 "padding\n"
                                                 "(OPTIONAL) Sample ID\n"
                                                 "(OPTIONAL) Gender of sample\n"
                                                 "(OPTIONAL) Sample ID of mother, 0 if none exists\n"
                                                 "(OPTIONAL) Sample ID of father, 0 if none exists\n"
                                                 "(OPTIONAL) Path to BAM file for sample\n"
                                                 "(OPTIONAL) Analysis type of sample (wgs, exon, etc.)\n"
                                                 "(OPTIONAL) Phenotype of the sample (Usually affected)\n"
                                                 "(OPTIONAL) Path to VCF file" + '\x1b[0m')

        elif sys.argv[1] == 'remove':
            if 4 <= len(sys.argv) < 5:
                print('\x1b[33m' + "Death befalls us all . . ." + '\x1b[0m')
            else:
                raise UserError('\x1b[33m' + "Number of arguments for remove are incorrect.\n"
                                             "Should be 2(two) arguments:\n" + '\x1b[0m'
                                + '\x1b[1;34m' + "case_id recorded in database\n"
                                                 "configfile for mutacc"
                                + '\x1b[0m')

        elif sys.argv[1] == 'create_dataset':
            if 8 <= len(sys.argv) < 11:
                print(
                    '\x1b[33m' + "BEEP BEEEP BEEP . . .Sorry, robot in my throat. Creating your datasets." + '\x1b[0m')
            else:
                raise UserError('\x1b[33m' + "Number of arguments for create_dataset are incorrect.\n"
                                             "Should be 4(four) to 6(six) arguments:\n" + '\x1b[0m'
                                + '\x1b[1;34m' + "mutacc configfile\n"
                                                 "BAM file to be used as a background for the dataset\n"
                                                 "FastQ file to be used as a background for the dataset\n"
                                                 "Pair of first FastQ file for pair ended background for dataset\n"
                                                 "(OPTIONAL) Status of samples to use; default is affected cases\n"
                                                 "(OPTIONAL) specific case search term,"
                                                 " see mutacc API for more information; defaults to None" + '\x1b[0m')

        elif sys.argv[1] == 'build_synthetics':
            if 9 <= len(sys.argv) < 12:
                print('\x1b[33m' + "The synths are here . . .  RUN!" + '\x1b[0m')
            else:
                raise UserError('\x1b[33m' + "Number of arguments for build_synthetics are incorrect.\n"
                                             "Should be 7(seven) arguments:\n" + '\x1b[0m'
                                + '\x1b[1;34m' + "mutacc database configfile\n"
                                + '\x1b[1;34m' + "synthetic database configfile(use same root_dir as mutacc database)\n"
                                                 "BAM file to be used as a background for the dataset\n"
                                                 "FastQ file to be used as a background for the dataset\n"
                                                 "Pair of first FastQ file for pair ended background for dataset\n"
                                                 "FastQ file for reference data to be included in the random sampling\n"
                                                 "pair of the first FastQ file for reference data to be included in "
                                                 "the random sampling\n" + '\x1b[0m')

        else:
            print('\x1b[33m' + "No such commands exists . . . You ignorant FOOL!" + '\x1b[0m' + '\n\n')
            raise UserError('\x1b[31m'
                            + "Try 'create_mutations' to create new mutations from a BAM file, \n"
                              "'mass_mutate' to create new mutations from several BAM files, \n"
                              "'import' to import cases to database, \n"
                              "'remove' to delete cases from the database, \n"
                              "'create_dataset' to create synthetic datasets from the database, \n"
                              " or 'build_synthetics' to create randomized datasets from the database"
                              " and from reference data\n"
                            + '\x1b[0m')
    except Exception as e:
        print('\x1b[37m' + "Arguments are faulty or incorrect" + '\x1b[0m', end=':\n')
        print(e)


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
            outputfile = bamfile

        if type(nr_procs) != int:
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
        mach.import_to_database(case_id, configfile, padding)
    elif len(args) == 8:
        mach.import_to_database(case_id, configfile, padding, *args)
    else:
        raise UserError(
            'Not enough arguments or too many arguments sent. Please look over them as only 0(zero) or '
            '8(eight) additional arguments are accepted')


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


def mass_mutate_and_import_to_database(mutationtype, configfile, padding, list_of_variationfiles,
                                       list_of_referencefiles, list_of_bamfiles, list_of_case_ids,
                                       list_of_outputfiles=None, matrix_of_args=None, nr_procs=1):
    """
    Create more than one(1) mutated bamfile and import them into the database, one at a time.
    :param mutationtype:            Type of mutation to run on all cases.
    :param padding:                 How much padding around the variance of interest there should be.
    :param list_of_variationfiles:  Tuple of BED files to use on BAM files. Sorted in order of BAM file list.
    :param list_of_referencefiles:  Tuple of fasta genome files to use with BAM files. Sorted in order of BAM file list.
    :param list_of_bamfiles:        Tuple of BAM files to mutate.
    :param list_of_outputfiles:     Tuple of names for mutated BAM files. Sorted in order of BAM file list.
    :param list_of_case_ids:        Tuple of case ID's to be assigned to new cases. Sorted in order of BAM file list.
    :param matrix_of_args:          Tuple containing tuples of arguments to use for new data of cases.
                                    Sorted in order of BAM file list.
    :param nr_procs:                Number of processes to use. Default is 1. More is recommended.
    :param configfile:              Location of configfile for mutacc.
                                    See https://github.com/Clinical-Genomics/mutacc#configuration-file
                                    for more information.

    :return:                        None, imports all cases to database
    """
    mutationtype, nr_procs, configfile = mutationtype, nr_procs, configfile

    for case in list_of_case_ids:

        position = list_of_case_ids.index(case)
        case_id = list_of_case_ids[position]
        variationfile = list_of_variationfiles[position]
        referencefile = list_of_referencefiles[position]
        bamfile = list_of_bamfiles[position]
        args = matrix_of_args[position]
        if list_of_outputfiles is None:
            outputfile = bamfile + '.mutated.bam'
        else:
            outputfile = list_of_outputfiles[position]
        bamposition = args.index(bamfile)
        args[bamposition] = outputfile
        create_mutations_in_bamfile(mutationtype, variationfile, referencefile, bamfile, outputfile, nr_procs)
        import_to_database(case_id, configfile, padding, *args)


def create_dataset(configfile, background_bam, background_fastq1, background_fastq2, member='affected', case=None):
    """
    Creates a dataset of the specified case/-s from the database. More information can be found at
        https://github.com/Clinical-Genomics/mutacc#export-datasets-from-the-database

    :param configfile:          Location of configfile for mutacc.
                                See https://github.com/Clinical-Genomics/mutacc#configuration-file for more information
    :param member:              Member to extract from database. Default is to extract all 'affected' cases
    :param background_bam:      Path to BAM file to use as background for the dataset.
    :param background_fastq1:   Path to FastQ file to use as background for the dataset.
    :param background_fastq2:   Path to second FastQ file to use as background for the dataset , if pair-ended.
    :param case:
    :return:
    """
    mach.export_from_database(configfile, background_bam, background_fastq1, background_fastq2, member, case)


def build_synthetic_dataset(mutaccdb_config, syntheticdb_config, background_bam, background_fastq1, background_fastq2,
                            reference_data_fq1, reference_data_fq2):
    build_dataset.create_randomized_dataset(mutaccdb_config, syntheticdb_config, background_bam, background_fastq1,
                                            background_fastq2, reference_data_fq1, reference_data_fq2)


# TODO:
#       Allow calling of any function in this file.
if __name__ == '__main__':
    main()
