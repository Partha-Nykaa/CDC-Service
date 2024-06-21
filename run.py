from __future__ import absolute_import, unicode_literals

import json
import os
import sys

sys.path.append(os.getcwd() + '/src')

from main.common.nykaa_logger_factory import RootLoggerFactory, ActivityLoggerFactory

debug = None
flask = None

RootLoggerFactory().setup()


def cdc(cfp) -> (str):
    from main import __main__
    with open(cfp) as json_file:
        config = json.load(json_file)
        #return __main__.start_celery(config)
        #TODO start the kafka and cdc pipeline


def application(cfp) -> (str):
    from main import __main__
    ActivityLoggerFactory().setup()
    with open(cfp) as json_file:
        config = json.load(json_file)
        d = False

    return d


def run_tests(test_dir, feature_file_name):
    from pytest import __main__
    if feature_file_name == 'all':
        test_command = test_dir
    else:
        test_command = test_dir + ' -i ' + feature_file_name

    __main__.main(test_command)


def with_coverage(code_to_test, test_dir, feature_name):
    import coverage
    c = coverage.Coverage(branch=True)
    c.start()

    code_to_test(test_dir, feature_name)

    c.stop()
    c.save()
    c.html_report()


def cli_parser():
    import argparse

    usage = '%(prog)s <functional argument> <ouput target argument>'
    description = 'Utility to run catalog backend'
    parser = argparse.ArgumentParser(usage=usage, description=description)

    optional_group = parser.add_argument_group()
    optional_group.add_argument('-c', '--coverage', action='store_true', dest='cov_arg',
                                help="Enabled code coverage. Valid for tests only.")

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-f', '--feed', action='store', nargs=1, dest='feed',
                       help='Run feed server with given environment', metavar='config_path')
    group.add_argument('-c', '--cdc', action='store', nargs=1, dest='cdc',
                       help='Run cdc server with given environment', metavar='config_path')
    group.add_argument('-u', '--unit', action='store', nargs=1, dest='unit',
                       help='Run a single or all unit test feature(s)', metavar='<feature_file_name> | all')
    group.add_argument('-t', '--test', action='store', nargs=1, dest='test',
                       help='Run a single or all unit test feature(s)',
                       metavar='config_path')
    return parser


def cli_controller():
    integration_dir = 'src/integration_tests'
    unit_dir = 'src/unit_tests'
    config_file_path_name = 'config_file_path'

    parser = cli_parser()
    args = parser.parse_args()
    global debug

    enabled_coverage = args.cov_arg

    if args.feed:
        config_file_path = args.main[0]
        debug = application(config_file_path)

    if args.unit:
        feature_name = args.unit[0]

        if enabled_coverage:
            with_coverage(run_tests, unit_dir, feature_name)
        else:
            run_tests(unit_dir, feature_name)

    if args.integration:
        feature_name = args.integration[0]
        os.environ[config_file_path_name] = args.integration[1]

        # start_s3()
        # start_mock_server()
        # start_mysql()

        if enabled_coverage:
            with_coverage(run_tests, integration_dir, feature_name)
        else:
            run_tests(integration_dir, feature_name)

    if args.test:
        feature_name = 'all'
        os.environ[config_file_path_name] = args.test[0]

        def run_it_ut(test_dir, feature_file_name):
            run_tests(unit_dir, feature_name)
            run_tests(integration_dir, feature_name)

        if enabled_coverage:
            with_coverage(run_it_ut, None, None)
        else:
            run_it_ut(None, None)

    if args.cdc:
        config_file_path = args.cdc[0]
        cdc(config_file_path)

    if not (args.unit or args.main or args.integration or args.test or args.job):
        config_file_path = os.environ[config_file_path_name]
        debug = application(config_file_path)


cli_controller()
