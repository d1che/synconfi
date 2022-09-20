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
import subprocess

import paths
import config
from ui import message

def which(command):
    try:
        output = subprocess.run(['which', command], capture_output=True)
        if output.stdout.decode("utf-8").strip() == '':
            raise Exception('Command not found: {}'.format(command))
        return output.stdout.decode("utf-8").strip()
    except Exception as e:
        print(e)

def test_connection():
    try:
        output = subprocess.run([
            'ssh',
            '-T',
            'git@github.com'],
            capture_output=True)
        if not 'successfully authenticated' in output.stderr.decode("utf-8").strip():
            raise Exception('Could not connect to github, please check your internet connection and ssh keys.')
    except Exception as e:
        print(e)

def check_remote(remote):
    try:
        output = subprocess.run([
            'git',
            'ls-remote',
            remote],
            capture_output=True)
        if output.returncode != 0:
            raise Exception('{} does not appear to be remote repository.'.format(remote))
    except Exception as e:
        print(e)

def git_init(path):
    try:
        git = which('git')
        output = subprocess.run([
            '{}'.format(git),
            'init',
            '--bare', '{}'.format(path)],
            capture_output=True)
        if output.returncode != 0:
            raise Exception('Could not initialize git repository in {}.'.format(config.current['local_repo']))
    except Exception as e:
        print(e)

def git(*commands):
    try:
        git = which('git')
        output = subprocess.run([
            '{}'.format(git),
            '--git-dir={}/'.format(config.current['local_repo']),
            '--work-tree={}'.format(paths.HOME),
            *commands],
            capture_output=True)
        if output.returncode != 0:
            raise Exception('{}.'.format(output.stderr.decode("utf-8").strip()))
    except Exception as e:
        print(e)

def edit(*files):
    try:
        nvim = which('nvim')
        commit_list = []
        for file in files[0]:
            if os.path.exists(os.path.abspath(file)):
                state1 = hash(file)
                os.system('{} {}'.format(nvim, file))
                state2 = hash(file)
                if state1 == state2:
                    message('{} was unmodified. Skipping.'.format(file))
                else:
                    commit_list.append(file)
            else:
                message('{} does not exist. Skipping.'.format(file))
        if commit_list != []:
            git('add', *commit_list)
        else:
            message('No files to commit.')
    except Exception as e:
        print(e)
