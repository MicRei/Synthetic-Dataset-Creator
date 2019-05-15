#!/usr/bin/env python

"""
File to handle user interactions.
"""
from program_handlers import build_randomized_dataset as build_dataset
from program_handlers import mutacc_handler as mach
from program_handlers import bamsurgeon_handler as bamh
import sys
import pathlib as path


class UserError(Exception):
    pass


def main(args):
    """
    Check which command is invoked and check that the arguments provided are valid.
    :param args: arguments for the run
    :return: None, depends on the function called.
    """
    if len(args) == 1:
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n"
              "Welcome to Synthetic Dataset Creator.\n"
              "Usage:\n"
              "\t create_mutations: Mutate a BAM file at the regions specified in a BED file.\n"
              "\t import: Import a new case into the mutacc database. Case can be either:\n"
              "\t\t -- new case data entered here.\n"
              "\t\t -- A case YAML file in the specified layout of mutacc.\n"
              "\t remove: Remove a case from the mutacc database using the case_id it is registered under.\n"
              "\t create_dataset: Create a dataset from all the cases in mutacc database or from the fetched cases\n"
              "\t\t\t Cases can be fetched by a JSON string of valid MongoDB language.\n"
              "\t build_synthetics: Randomly choose cases in the mutacc database and referencedata, and build\n"
              "\t\t\t  a new dataset from them.\n"
              "\t mass_mutate: NOT IMPLEMENTED YET. Mutate several BAM files at the regions specified in \n"
              "\t\t\t their specific BED file and import them to the mutacc database.\n"
              "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
    else:
        try:
            # Check each argument and assure that
            # they correspond with the arguments sent to create_mutations_in_bamfile
            if args[1] == 'create_mutations':
                if 6 <= len(args) < 9:
                    if args[2] in {'addsnv', 'addsv', 'addindel'}:
                        file_checker = [path.Path(arg).is_file() for arg in args[3:6]]
                        suffixes = [path.Path(arg).suffix for arg in args[3:6]]
                        if False not in file_checker:
                            if (suffixes[0] == '.bed' and
                                    suffixes[1] == '.fa' and
                                    suffixes[2] == '.bam'):
                                create_mutation_arguments = []
                                create_mutation_arguments.extend(args[2:6])
                                if len(args) > 6:
                                    if path.Path(args[6]).suffix == '.bam':
                                        create_mutation_arguments.append(args[6])
                                    else:
                                        raise UserError('\x1b[31m'
                                                        + "Please see over your arguments as the "
                                                          "outputfile was not a .bam file"
                                                        + '\x1b[0m')
                                if len(args) > 7:
                                    if args[7].isdigit():
                                        create_mutation_arguments.append(args[7])
                                    else:
                                        raise UserError('\x1b[31m'
                                                        + "Please see over your arguments as the "
                                                          "number of processes sent in was not a number"
                                                        + '\x1b[0m')
                                create_mutations_in_bamfile(*create_mutation_arguments)

                        else:
                            raise UserError('\x1b[31m'
                                            + "Please see over your arguments as one or more was not a file."
                                            + '\x1b[0m')

                else:
                    print(len(args))
                    raise UserError('\x1b[33m' + "Number of arguments for create_mutations are incorrect.\n"
                                                 "Should be 4(four) to 6(six) arguments:\n" + '\x1b[0m'
                                    + '\x1b[1;34m' + "mutationtype: addsnv, addsv, or addindel are accepted.\n"
                                                     "variationfile\n"
                                                     "referencefile\n"
                                                     "bamfile\n"
                                                     "(OPTIONAL) outputfile; default is None\n"
                                                     "(OPTIONAL) number of processes; default is 1(one)" + '\x1b[0m')
            # TODO: Fix mass_mutate and add capability to open a file and store a list of arguments
            elif args[1] == 'mass_mutate':
                if 9 <= len(args) < 13:
                    print('\x1b[33m' + "CURRENTLY NOT IMPLEMENTED!" + '\x1b[0m')
                else:
                    raise UserError('\x1b[33m' + "CURRENTLY NOT IMPLEMENTED\n"
                                                 "Number of arguments for mass_mutate are incorrect.\n"
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

            elif args[1] == 'import':
                if len(args) == 5 or len(args) == 13:
                    if not path.Path(args[3]).is_file() or path.Path(args[3]).suffix != '.yaml':
                        raise UserError('\x1b[31m'
                                        + "Please see over your arguments as the config file is not a .yaml file"
                                        + '\x1b[0m')
                    if args[4].isdigit() is False:
                        raise UserError('\x1b[31m'
                                        + "Please see over your arguments as the padding must be a number"
                                        + '\x1b[0m')

                    if len(args) == 5:
                        import_args = args[2:5]
                        import_to_database(*import_args)

                    elif len(args) == 13:
                        additional_args = args[5:]
                        if additional_args[1] not in {'male', 'female', 'unknown'}:
                            raise UserError('\x1b[31m'
                                            + "Please see over your arguments as the only genders accepted are male,"
                                              " female, and unknown (all lower case letters)"
                                            + '\x1b[0m')

                        if not path.Path(additional_args[4]).is_file() \
                                and path.Path(additional_args[4]).suffix != '.bam':
                            raise UserError('\x1b[31m'
                                            + "Please see over your arguments as a valid .bam file was not given."
                                            + '\x1b[0m')

                        if additional_args[6] not in {'affected', 'unaffected'}:
                            raise UserError('\x1b[31m'
                                            + "Please see over your arguments as the phenotype should "
                                              "be affected or unaffected (all lower case letters)"
                                            + '\x1b[0m')

                        if not path.Path(additional_args[7]).is_file() \
                                and path.Path(additional_args[7]).suffix != '.vcf':
                            raise UserError('\x1b[31m'
                                            + "Please see over your arguments as a valid .vcf file was not given."
                                            + '\x1b[0m')
                        import_args = args[2:]
                        import_to_database(*import_args)

                else:
                    raise UserError('\x1b[33m' + "Number of arguments for import are incorrect.\n"
                                                 "Should be 3(three) OR 13(thirteen) arguments:\n" + '\x1b[0m'
                                    + '\x1b[1;34m' + "case_id\n"
                                                     "configfile\n"
                                                     "padding\n"
                                                     "(OPTIONAL) Sample ID\n"
                                                     "(OPTIONAL) Gender of sample; male, female, or unknown\n"
                                                     "(OPTIONAL) Sample ID of mother, 0 if none exists\n"
                                                     "(OPTIONAL) Sample ID of father, 0 if none exists\n"
                                                     "(OPTIONAL) Path to BAM file for sample\n"
                                                     "(OPTIONAL) Analysis type of sample (wgs, exon, etc.)\n"
                                                     "(OPTIONAL) Phenotype of the sample (Usually affected)\n"
                                                     "(OPTIONAL) Path to VCF file" + '\x1b[0m')

            elif args[1] == 'remove':
                if 4 <= len(args) < 5:
                    if not path.Path(args[3]).is_file() or path.Path(args[3]).suffix != '.yaml':
                        raise UserError('\x1b[31m'
                                        + "Please see over your arguments as the config file is not a .yaml file"
                                        + '\x1b[0m')
                    remove_case_from_database(args[2], args[3])
                else:
                    raise UserError('\x1b[33m' + "Number of arguments for remove are incorrect.\n"
                                                 "Should be 2(two) arguments:\n" + '\x1b[0m'
                                    + '\x1b[1;34m' + "case_id to be recorded in database\n"
                                                     "configfile for mutacc"
                                    + '\x1b[0m')

            elif args[1] == 'create_dataset':
                if 6 <= len(args) < 9:
                    file_checker = [path.Path(arg).is_file() for arg in args[2:6]]
                    suffixes = [path.Path(arg).suffix for arg in args[2:6]]
                    if False in file_checker:
                        raise UserError('\x1b[31m'
                                        + "Please look over your arguments as one or more of the 4(four) required"
                                          " ones them was not a file or in the right order; {}".format(args[2:6])
                                        + '\x1b[0m')
                    if ('.yaml' != suffixes[0]
                            or '.bam' != suffixes[1]
                            or suffixes[2] not in {'.gz', '.fastq'}
                            or suffixes[3] not in {'.gz', '.fastq'}):
                        raise UserError('\x1b[31m'
                                        + "Please look over your arguments as one or more of the 4(four) required"
                                          " ones them was not a filetype or in the right order: {}".format(suffixes)
                                        + '\x1b[0m')
                    dataset_args = args[2:6]
                    if len(args) > 6:
                        if args[6] not in {'affected', 'mother', 'father', 'child'}:
                            raise UserError('\x1b[31m'
                                            + "Please look over your arguments as " + '\x1b[33m'
                                            + '{} '.format(args[6]) + '\x1b[31m'
                                            + "is not a valid member to search "
                                              "for. valid ones are affected, child, mother, and father"
                                            + '\x1b[0m')
                        else:
                            dataset_args.append(args[6])
                    if len(args) > 7:
                        dataset_args.append(args[7])
                    create_dataset(*dataset_args)
                else:
                    raise UserError('\x1b[33m' + "Number of arguments for create_dataset are incorrect.\n"
                                                 "Should be 4(four) to 6(six) arguments:\n" + '\x1b[0m'
                                    + '\x1b[1;34m' + "mutacc configfile\n"
                                                     "BAM file to be used as a background for the dataset\n"
                                                     "FastQ file to be used as a background for the dataset\n"
                                                     "Pair of first FastQ file for pair ended background for dataset\n"
                                                     "(OPTIONAL) Status of samples to use; default is affected cases\n"
                                                     "(OPTIONAL) specific case search term, see mutacc API for "
                                                     "more information; defaults to None" + '\x1b[0m')

            elif args[1] == 'build_synthetics':
                print(len(args))
                if 7 == len(args) or len(args) == 9:
                    file_checker = [path.Path(arg).is_file() for arg in args[2:]]
                    suffixes = [path.Path(arg).suffix for arg in args[2:]]
                    if False in file_checker:
                        raise UserError('\x1b[31m'
                                        + "Please look over your arguments as one or more of the provided arguments "
                                          "was not a file or in the right order;\n {}".format(args[2:])
                                        + '\x1b[0m')
                    if ('.yaml' != suffixes[0]
                            or '.yaml' != suffixes[1]
                            or '.bam' != suffixes[2]
                            or suffixes[3] not in {'.gz', '.fastq'}
                            or suffixes[4] not in {'.gz', '.fastq'}):
                        raise UserError('\x1b[31m'
                                        + "Please look over your arguments as one or more of the 4(four) required"
                                          " ones them was not a filetype or in the right order: {}".format(suffixes[:4])
                                        + '\x1b[0m')
                    if len(suffixes) > 5:
                        if (suffixes[5] not in {'.gz', '.fastq'}
                                or suffixes[6] not in {'.gz', '.fastq'}):
                            raise UserError('\x1b[31m'
                                            + "Please look over your arguments as one or more of the 2(two) references"
                                              " was not a fastq or fastq.gz filetype: {}".format(suffixes[5:])
                                            + '\x1b[0m')
                    synthetic_args = args[2:]
                    build_synthetic_dataset(*synthetic_args)
                else:
                    raise UserError('\x1b[33m' + "Number of arguments for build_synthetics are incorrect.\n"
                                                 "Should be 5(five) or 7 (seven) arguments:\n" + '\x1b[0m'
                                    + '\x1b[1;34m' + "mutacc database configfile\n"
                                    + '\x1b[1;34m' + "synthetic database configfile(same root_dir as mutacc database)\n"
                                                     "BAM file to be used as a background for the dataset\n"
                                                     "FastQ file to be used as a background for the dataset\n"
                                                     "Pair of first FastQ file for pair ended background for dataset\n"
                                                     "(OPTIONAL)FastQ file for reference data to be included in the "
                                                     "random sampling\n"
                                                     "(OPTIONAL)pair of the first FastQ file for reference data to "
                                                     "be included in the random sampling\n" + '\x1b[0m')

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
            print("\n**************************************************************\n"
                  "Arguments are faulty or incorrect:")
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

    if args is None or len(args) == 0:
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
                            reference_data_fq1=None, reference_data_fq2=None):
    build_dataset.create_randomized_dataset(mutaccdb_config, syntheticdb_config, background_bam, background_fastq1,
                                            background_fastq2, reference_data_fq1, reference_data_fq2)


if __name__ == '__main__':
    main(sys.argv)
