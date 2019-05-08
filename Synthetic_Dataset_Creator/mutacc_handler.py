"""
File to handle mutacc interaction.
"""
import yaml
import subprocess as sp
from re import search
from pathlib import Path


class MutaccError(Exception):
    pass


def import_to_database(case_id, configfile, padding, *args):
    """
    Function to create a new data set, or use existing data, and insert it into the mutacc database.

    :param case_id:     Path to a yamlfile with the correct structure or the ID of a new case.
    :param configfile:  Config file containing the root directory of mutaccfiles.
                        See https://github.com/Clinical-Genomics/mutacc#configuration-file for more information.
    :param padding:     Length of padding around desired region.
    :param args:        The 8 additional data needed to create a new case;
                            Sample ID of the sample,
                            Gender of the sample,
                            Sample ID of Mothers sample if applicable, '0' if not,
                            Sample ID of Father of sample if applicable, '0' if not,
                            Location of BAM file,
                            Type of analysis performed,
                            Phenotype of the subject,
                            VCF location.
                        For an example, see https://github.com/Clinical-Genomics/mutacc#populate-the-mutacc-database.
    :return:            None, case added to database.
    """
    try:
        if type(case_id) is str and Path(case_id).is_file():
            with open(case_id, 'r') as yaml_case:
                if not yaml_case.readable():
                    raise MutaccError("No read permission granted.")
                else:
                    print("Importing into database: " + yaml_case.name)
                    _mutacc_extract_and_import(configfile, yaml_case.name, padding, case_id)
        elif len(args) == 8:
            new_data = [case_id]
            new_data.extend(args)
            case_yaml = _create_yaml_file(*new_data)
            _mutacc_extract_and_import(configfile, case_id, padding, case_yaml)

        else:
            raise MutaccError("Not enough args sent to import or no such file exists. Please supplement your data")
    except Exception as e:
        print("Something went wrong during import: ", e)


def _mutacc_extract_and_import(configfile, case_id, padding, case_yaml):
    """
    Internal function to handle mutacc data extraction and import to database.

    :param configfile:      The config file containing the root directory of mutaccfiles.
    :param case_id:         The name of the case file.
    :param padding:         Length of padding around desired region.
    :param case_yaml:       The name of the case YAML file.
    :return:                None, case added to database.
    """
    root_dir = _get_mutacc_root_dir(configfile)

    path_to_imported_case = root_dir + 'imports/' + str(case_id) + '_import.mutacc'

    sp.run(['mutacc', '--config-file', configfile, 'extract', '--padding', padding, '--case', case_yaml])
    sp.run(['mutacc', '--config-file', configfile, 'db', 'import', path_to_imported_case])


def export_from_database(configfile, background_bam, background_fastq1, background_fastq2, member='affected',
                         case=None):
    """
    Export a case from the database and create a dataset, stored as FASTQ, from it. More information can be found at
        https://github.com/Clinical-Genomics/mutacc#export-datasets-from-the-database.

    :param configfile:          The config file containing the root directory of mutaccfiles.
                                See https://github.com/Clinical-Genomics/mutacc#configuration-file for more information.
    :param member:              member to look for, default is 'affected'.
    :param background_bam:      BAM-file to use as base for dataset.
    :param background_fastq1:   FastQ-file to use as base for dataset.
    :param background_fastq2:   FastQ-file to use as base for pair-ended datasets.
    :param case:                Specific case to look for.
    :return:                    Outputs fastq files related to the synthetic dataset created.
    """
    root_dir = _get_mutacc_root_dir(configfile)

    print(root_dir)

    path_to_query = root_dir + 'queries/affected_query.mutacc'

    print(path_to_query)
    # if case is None:
    #     case = '{}'
    # sp.run(['mutacc', '--config-file', configfile, 'db', 'export', '-m', member, '-c', case])
    # sp.run(
    #     ['mutacc', '--config-file', configfile, 'synthesize', '-b', background_bam, '-f', background_fastq1,
    #      '-f2', background_fastq2, '-q', path_to_query])


def remove_from_database(case, configfile):
    """
    Removes the specified case from the database completely.

    :param case:        Case ID of the desired case.
    :param configfile:  Location of configfile for mutacc.
                        See https://github.com/Clinical-Genomics/mutacc#configuration-file
                        for more information.
    :return:            None.
    """
    sp.run(['mutacc', '--config-file', configfile, 'db', 'remove', case])


def _create_yaml_file(case_id, sample_id, sex, mother, father, bam, analysis, phenotype, variants):
    """
    Internal function to create a YAML document from provided data.

    :param case_id:     name of the case.
    :param sample_id:   name for the sample.
    :param sex:         gender of patient.
    :param mother:      sample id of mother, if applicable.
    :param father:      sample id of father, if applicable.
    :param bam:         path to bamfile containing reads for patient.
    :param analysis:    analysis type performed on patients data.
    :param phenotype:   phenotype of patient (affected or unaffected).
    :param variants:    path to variantfile patient.
    :return:            The name of the created file.
    """
    if case_id is str:
        create_file = case_id + ".yaml"
    else:
        create_file = str(case_id) + ".yaml"

    with open(create_file, 'w') as yamlfile:
        try:
            yaml.dump({'case': {'case_id': case_id}, 'samples': [{'sample_id': sample_id, 'analysis_type': analysis,
                                                                  'sex': sex, 'mother': mother, 'father': father,
                                                                  'bam_file': bam, 'phenotype': phenotype}],
                       'variants': variants}, yamlfile)
        except yaml.YAMLError as exc:
            print('Error writing yaml object: ', exc)
            raise MutaccError("Yaml creation error")

    return create_file


def _get_mutacc_root_dir(configfile):
    with open(configfile, 'r') as config_handle:
        root_dir = yaml.safe_load(config_handle).get('root_dir')
    return root_dir
