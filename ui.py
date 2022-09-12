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
import constants

from argparse import ArgumentParser, RawTextHelpFormatter

def process_input():
    usage = '%(prog)s [options] file'
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
        help='restore a configuration file from the repository')
    parser.add_argument(
        '-n', '--add',
        metavar='FILE',
        action='store',
        help='add a file to the repository without editing it.')
    parser.add_argument(
        '-a', '--all',
        action='store_true',
        help='restore all configuration files from the repository')
    parser.add_argument(
        '-i', '--init',
        action='store_true',
        help='initialize or change configuration')
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s {}'.format(version),
        help='display the program\'s version number')
    parser.add_argument(
        'file',
        action='store',
        help='the file to add or edit',
        nargs='?')

    options = parser.parse_args()

    if all(x==False for x in vars(options).values()):
        parser.error('Incorrect number of arguments.')

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
