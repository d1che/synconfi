# Copyright 2022 Willem Deen.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
import shutil

import commands
import config
import constants
import helpers

def process_input():
    usage = '%(prog)s [options] file(s)'
    version = '0.9.0'
    description = 'Synchronize dot files and other config files across multiple systems.'
    epilog = ''
    formatter = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=28)

    parser = argparse.ArgumentParser(
        usage=usage,
        description=description,
        epilog=epilog,
        formatter_class=formatter,
        argument_default=False)

    parser.add_argument(
        '-n', '--new',
        metavar='FILE',
        action='store',
        help='add a new file to the repository without editing it.')
    parser.add_argument(
        '-r', '--restore',
        metavar='FILE',
        action='store',
        help='restore a file from the repository')
    parser.add_argument(
        '-a', '--all',
        action='store_true',
        help='restore all files from the repository')
    parser.add_argument(
        '-p', '--push',
        action='store_true',
        help='push all changes to the remote')
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='list all files in the repository')
    parser.add_argument(
        '-c', '--configure',
        action='store_true',
        help='edit the configuration')
    parser.add_argument(
        '-i', '--init',
        action='store_true',
        help='initialize a new git repository to be used with %(prog)s')
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s {}'.format(version),
        help='display the program\'s version number')
    parser.add_argument(
        'files',
        metavar='file(s)',
        action='store',
        default='',
        help='file or list of files to edit',
        nargs='*')

    options = parser.parse_args()

    # check not more than 1 option is given
    if sum(list(vars(options).values())[0:-1]) > 1:
        parser.error('Only one option can be supplied at a time.')
    # check if either an option or a file is given
    elif not any(list(vars(options).values())[0:-1]) and len(options.files) < 1:
        parser.error('Please supply a file or option. (-h for help)')
    # check that not more than one file is given when using specific options
    elif (options.restore or options.new) and len(options.files) != 1:
        parser.error('Please supply exactly 1 argument when using --restore or --add.')
    else:
        return options   

def local_repo(default=None):
    p = None
    while True:
        local_repo = ask_input('Please specify a new path for the local git repository', default)

        p = helpers.format_path(local_repo)

        if os.path.exists(p):
            if len(os.listdir(p)) != 0:
                print('This directory is not empty.')
        else:
            try:
                # primitive way of checking if current repo exists
                if os.path.exists('{}/HEAD'.format(config.current['local_repo'])):
                    if ask_confirm('Are you sure you wish to move the repo to {} ?'.format(p)):
                        # move the existing repo to new location
                        shutil.move(config.current['local_repo'], p)
                        message('Successfully moved local repository to {}'.format(p))
                        break
                else:
                    if ask_confirm('Are you sure you want to create a new repo at {} ?'.format(p)):
                        # just make new dirs
                        os.makedirs(p)
                        break
            except Exception as e:  
                print(e)

    # save new path
    config.current['local_repo'] = p

def ask_confirm(prompt='Continue?'):
    while True:
        answer = input('{} [y/N]: '.format(helpers.format_sentences(prompt)))
        match answer:
            case 'y' | 'Y':
                return True
            case 'n' | 'N' | '':
                return False
            case _:
                print('Incorrect answer')

def ask_input(prompt, default=None):
    while True:
        answer = input(
            '{}: '.format(helpers.format_sentences(prompt)) if default == None else
            '{} ({}): '.format(helpers.format_sentences(prompt), default))
        if answer != '':
            return answer
        elif default != None:
            return default
        else:
            print('No input was received')

def message(text):
    os.system(constants.BOLD)
    print(text)
    os.system(constants.RESET)
