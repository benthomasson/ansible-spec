#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
import os
import sys
import argparse
import logging

from . import compiler

logger = logging.getLogger(__name__)

from logging import config
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'ERROR'
    }
}

COMMANDS = {
    'help': 'Display this help message',
    'compile': 'Compile a spec file into a module skeleton',
}

def command_compile_parser(parser, subparser):
    subparser.add_argument('spec', action='store',
                        help='Input spec file to process')

    subparser.add_argument("--author", action="store",
                           help="Module author field in the format of "
                                "First Last (@GithubId)")

    subparser.add_argument("--version-added", action="store",
                           help="Module version_added field value in the form "
                                "of X.Y")

    subparser.add_argument("--output", action="store",
                           help="Filename to write output to")



def commandline():
    parser = argparse.ArgumentParser(description='Generate Ansible modules '
                                                 'from spec files')

    parser.add_argument('--debug', action='store_true', default=False,
                        help='Enable debug output')

    subparsers = parser.add_subparsers(title='subcommand', dest='subcommand')
    subparsers.required = True
    for subcommand in COMMANDS:
        logger.debug('Registering subcommand %s', subcommand)
        subparser = subparsers.add_parser(subcommand, help=COMMANDS[subcommand])
        func = globals().get('command_%s_parser' % subcommand)
        if func:
            func(parser, subparser)

    args = parser.parse_args()

    if args.subcommand == 'help':
        parser.print_help()
        sys.exit(0)

    config.dictConfig(LOGGING)

    if args.subcommand == 'compile':
        compiler.run(args)

    sys.exit(0)
