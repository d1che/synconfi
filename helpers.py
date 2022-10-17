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
import sys
import hashlib

import constants

def format_sentences(text):
    words = text.split()
    i = 0
    sentence = ''
    sentences = []
    while True:
        if i < len(words):
            if len(sentence) < constants.MAX_WIDTH:
                sentence += words[i] + ' '
                i += 1
            else:
                sentences.append(sentence[0:-1])
                sentence = ''
        else:
            sentences.append(sentence[0:-1])
            break
    return '\n'.join(sentences)

def format_path(p):
    path = ''
    # Attempt to make this portable by performing the right kind of path expansion
    if sys.platform == 'linux' or sys.platform == 'linux2' or sys.platform == 'darwin':
        if '~' in p:
            path = os.path.expanduser(p)
        elif '$HOME' in p:
            rest_path = p.strip('$HOME')
            path = '{}{}'.format(os.environ['HOME'], rest_path)
        else:
            path = os.path.abspath(p)
    elif sys.platform == "win32":
        path = os.path.expandvars(repr(p))

    return path

def calculate_hash(file):
    md5_hash = hashlib.md5()
    with open(file, 'rb') as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096), b''):
            md5_hash.update(byte_block)
        return md5_hash.hexdigest()
