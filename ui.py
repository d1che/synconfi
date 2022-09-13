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

import os
from argparse import ArgumentParser, RawTextHelpFormatter

import constants

def process_input():
    usage = '%(prog)s [options] file(s)'
    version = '0.9.0'
    description = 'Synchronize dot files and other config files across multiple systems.'
    epilog = ''
    formatter = lambda prog: RawTextHelpFormatter(prog, max_help_position=28)

    parser = ArgumentParser(
        usage=usage,
        description=description,
        epilog=epilog,
        formatter_class=formatter,
        argument_default=False)

    parser.add_argument(
        '-r', '--restore',
        metavar='FILE',
        action='store',
        help='restore a file from the repository')
    parser.add_argument(
        '-n', '--new',
        metavar='FILE',
        action='store',
        help='add a new file to the repository without editing it.')
    parser.add_argument(
        '-p', '--push',
        action='store_true',
        help='push all changes to the remote')
    parser.add_argument(
        '-a', '--all',
        action='store_true',
        help='restore all files from the repository')
    parser.add_argument(
        '-i', '--init',
        action='store_true',
        help='initialize a git repository to be used with %(prog)s')
    parser.add_argument(
        '-c', '--configure',
        action='store_true',
        help='edit the configuration')
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
    elif (options.restore or options.new) and len(options.files) < 1:
        parser.error('Please supply exactly 1 argument when using --restore or --add.')
    else:
        return options

def format_sentences(text):
    words = text.split()
    count = 0
    sentence = ''
    sentences = []
    while True:
        if len(sentence) >= constants.MAX_WIDTH or count >= len(words):
            sentences.append(sentence[0:-1])
            sentence = ''
            if count >= len(words)-1:
                break
        else:
            sentence += words[count] + ' '
            count += 1
    return '\n'.join(sentences)

def ask_confirm(prompt='Continue?'):
    while True:
        answer = input('{} [y/N]: '.format(format_sentences(prompt)))
        match answer:
            case 'y' | 'Y':
                return True
            case 'n' | 'N' | '':
                return False
            case _:
                print('Incorrect answer')

def ask_input(prompt):
    answer = input('{}: '.format(format_sentences(prompt)))
    if answer != None:
        return answer

def message(text, color=None):
    match color:
        case 'black':
            os.system(constants.BLACK)
        case 'red':
            os.system(constants.RED)
        case 'green':
            os.system(constants.GREEN)
        case 'yellow':
            os.system(constants.YELLOW)
        case 'blue':
            os.system(constants.BLUE)
        case 'magenta':
            os.system(constants.MAGENTA)
        case 'cyan':
            os.system(constants.CYAN)
        case 'white':
            os.system(constants.WHITE)
        case None:
            pass
    os.system(constants.BOLD)
    print(text)
    os.system(constants.RESET)

def error(text):
    os.system(constants.RED)
    os.system(constants.BOLD)
    print('ERROR: {}'.format(text))
    os.system(constants.RESET)
