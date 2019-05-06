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
            outputfile = bamfile

        if type(nr_procs) != int:
            print(type(nr_procs))
            print(nr_procs)
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


def mass_mutate_and_import_to_database(mutationtype, configfile, padding, list_of_variationfiles,
                                       list_of_referencefiles, list_of_bamfiles, list_of_case_ids,
                                       list_of_outputfiles=None, matrix_of_args=None, nr_procs=1):
    """
    Create more than one(1) mutated bamfile and import them into the database, one at a time.
    :param mutationtype:            Type of mutation to run on all cases.
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


def create_dataset(configfile, background_bam, background_fastq1, background_fastq2, member='affected', *args):
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
    mach.export_from_database(configfile, background_bam, background_fastq1, background_fastq2, member, args)


if __name__ == '__main__':
    """
    mass_mutate_and_import_to_database('addsnv', './mutacc_config.yaml', '160',
                                       ('/home/mire/PycharmProjects/project_files/mychr17snv1.bed', ),
                                       '/home/mire/PycharmProjects/fasta_hg38/hg38',
                                       '/home/mire/PycharmProjects/project_test/NA12878_mybam.sorted.bam', '434343',
                                       ('434343', 'sample43', 'female', '0', '0',
                                        '/home/mire/PycharmProjects/project_test/NA12878_mybam.sorted.bam', 'heart',
                                        'affected', '/home/mire/PycharmProjects/project_test/testcases/23423.vcf',
                                        './mutacc_config.yaml', '160'), nr_procs=30)

    """
    mass_mutate_and_import_to_database(nr_procs=30, mutationtype='addsnv', configfile='./mutacc_config.yaml',
                                       padding='160',

                                       list_of_variationfiles=[
                                           '/home/mire/PycharmProjects/project_files/mychr17snv1.bed',
                                           '/home/mire/PycharmProjects/project_files/mychr17snv1.bed',
                                           '/home/mire/PycharmProjects/project_files/mychr17snv1.bed'],

                                       list_of_referencefiles=['/home/mire/PycharmProjects/fasta_hg38/hg38.fa',
                                                               '/home/mire/PycharmProjects/fasta_hg38/hg38.fa',
                                                               '/home/mire/PycharmProjects/fasta_hg38/hg38.fa'],

                                       list_of_bamfiles=['/home/mire/PycharmProjects/hg38/NA12878twist.sorted.bam',
                                                         '/home/mire/PycharmProjects/hg38/NA12878west.sorted.bam',
                                                         '/home/mire/PycharmProjects/project_test/NA12878_mybam.sorted.bam'],

                                       list_of_case_ids=['45664', '45763', '45121'],

                                       matrix_of_args=[['sample99', 'female', '0', '0',
                                                        '/home/mire/PycharmProjects/hg38/NA12878twist.sorted.bam',
                                                        'wgs', 'affected',
                                                        '/home/mire/PycharmProjects/project_test/testcases/57742.vcf'],
                                                       ['sample22', 'female', '0', '0',
                                                        '/home/mire/PycharmProjects/hg38/NA12878west.sorted.bam',
                                                        'TP53', 'affected',
                                                        '/home/mire/PycharmProjects/project_test/testcases/57745.vcf'],
                                                       ['sample43', 'female', '0', '0',
                                                        '/home/mire/PycharmProjects/project_test/NA12878_mybam.sorted.bam',
                                                        'heart', 'affected',
                                                        '/home/mire/PycharmProjects/project_test/testcases/57744.vcf']])
