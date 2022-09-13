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

import subprocess
from os.path import exists

import paths
from ui import message

def which(command):
    output = subprocess.run(['which', command], capture_output=True)
    if output.stdout:
        return output.stdout.decode("utf-8").strip()
    else:
        message('ERROR: git is not installed on this system.', 'red')

def test_connection():
    output = subprocess.run([
        'ssh',
        '-T',
        'git@github.com'],
        capture_output=True)
    if not 'successfully authenticated' in output.stderr.decode("utf-8").strip():
        message('ERROR: Could not connect to github, please check your internet connection and ssh keys.', 'red')
    else:
        return True

def check_remote(remote):
    output = subprocess.run([
        'git',
        'ls-remote',
        remote],
        capture_output=True)
    if output.returncode != 0:
        message('ERROR: {} does not appear to be a git repository.'.format(remote), 'red')
    else:
        return True

def git_init():
    git = which('git')
    output = subprocess.run([
        '{}'.format(git),
        'init',
        '--bare', '{}'.format(paths.REPO)],
        capture_output=True)
    if output.returncode != 0:
        message('ERROR: Could not initialize git repository in {}.'.format(paths.REPO), 'red')
    else:
        return True

def git(*commands):
    git = which('git')
    output = subprocess.run([
        '{}'.format(git),
        '--git-dir={}/'.format(paths.REPO),
        '--work-tree={}'.format(paths.HOME),
        *commands],
        capture_output=True)
    if output.returncode != 0:
        message('ERROR: {}.'.format(output.stderr.decode("utf-8").strip()), 'red')
    else:
        return True

def edit(*files):
    nvim = which('nvim')
    commit_list = []
    for file in files:
        if exists(file):
            state1 = hash(file)
            output = subprocess.run([
                nvim,
            ])
            state2 = hash(file)
            if state1 == state2:
                message('{} was unmodified Skipping.'.format(file), 'cyan')
            else:
                commit_list.append(file)
        else:
            message('ERROR: {} does not exist.'.format(file), 'red')
    git('add', *commit_list)