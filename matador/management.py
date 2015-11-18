#!/usr/bin/env python
import sys
import os
import logging
import argparse
from matador.commands import commands


def _setup_logging(logging_destination='console', verbosity='INFO'):
    logHandlers = {
        'console': logging.StreamHandler(),
        'none': logging.NullHandler(),
        # 'file': logging.FileHandler('./matador.log')
    }
    logHandler = logHandlers[logging_destination]

    logFormatters = {
        'console': '%(message)s',
        'none': '',
        'file': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }
    logFormatter = logging.Formatter(logFormatters[logging_destination])

    logHandler.setFormatter(logFormatter)
    logger = logging.getLogger('matador')
    level = logging.getLevelName(verbosity.upper())
    logger.setLevel(level)
    logger.addHandler(logHandler)


def working_folder(project, environment):
    working_path = os.path.expanduser(
        '~/.matador/%s/%s' % (project, environment))
    os.makedirs(working_path, exist_ok=True)
    return working_path


def execute_command():
    parser = argparse.ArgumentParser(
        description="Taming the bull: Change management for Agresso systems")

    parser.add_argument(
        'command',
        type=str,
        help='Command')

    parser.add_argument(
        '-l', '--logging',
        type=str,
        default='console',
        dest='logging_destination',
        help='logging (none, console or file)')

    parser.add_argument(
        '-v', '--verbosity',
        type=str,
        default='INFO',
        help='Logging level. DEBUG, INFO, ERROR or CRITICAL')

    try:
        args, sub_args = parser.parse_known_args()
        _setup_logging(args.logging_destination, args.verbosity)
    except:
        parser.print_help()
        sys.exit()

    commands[args.command]()