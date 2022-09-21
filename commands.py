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
import helpers
import ui 

def which(command):
    try:

        # perform which
        output = subprocess.run([
            'which',
            command], 
            capture_output=True)

        if output.stdout.decode("utf-8").strip() == '':
            raise Exception('Command not found: {}'.format(command))

        # return path
        return output.stdout.decode("utf-8").strip()

    except Exception as e:
        print(e)

def test_connection():
    try:

        # check connection to github
        output = subprocess.run([
            'ssh',
            '-T',
            'git@github.com'],
            capture_output=True)

        if not 'successfully authenticated' in output.stderr.decode("utf-8").strip():
            raise Exception('Could not connect to github, please check your internet connection and ssh keys.')

    except Exception as e:
        print(e)
        exit()

def check_remote(remote):
    try:

        # check remote with ls-remote
        output = subprocess.run([
            'git',
            'ls-remote',
            remote],
            capture_output=True)

        if output.returncode != 0:
            raise Exception('{} does not appear to be valid a remote repository.'.format(remote))
        else:
            return True

    except Exception as e:
        print(e)
        return False

def git_init(path):
    try:

        # get full path of git command
        git = which('git')

        # create git repo at specified path
        output = subprocess.run([
            '{}'.format(git),
            'init',
            '--bare', '{}'.format(path)],
            capture_output=True)

        if output.returncode != 0:
            raise Exception('Could not initialize git repository in {}.'.format(path))

    except Exception as e:
        print(e)
        exit()

def git(*commands):
    try:

        # get full path of git command
        git = which('git')

        # run git from configured directory
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
        exit()

def edit(*files):
    try:

        # get full path of configured editor
        editor = which(config.current['editor'])

        # create a list for git to commit
        commit_list = []

        for f in files[0]:
            # format the path of the file
            file = helpers.format_path(f)

            # create the file if it doesn't exist
            if not os.path.exists(file):
                ui.message('Creating {}'.format(file))
                output = subprocess.run([
                    'touch',
                    file],
                    capture_output=True)
                if output.returncode !=0:
                    raise Exception('Could not create {}'.format(file))
            
            # calculate md5 hash before editing the file
            state1 = helpers.calculate_hash(file)
            
            # launch file in configured editor
            output = subprocess.Popen([
                '{}'.format(editor),
                file],
                capture_output=True)
            if output.returncode != 0:
                raise Exception('Could not edit {}'.format(file))

            # calculate md5 hash before editing the file
            state2 = helpers.calculate_hash(file)

            # compare hashes to determine if file was modified
            if state1 == state2:
                print('{} was unmodified. Skipping.'.format(file))
            else:
                # add the file to be committed
                commit_list.append(file)

        # commit files
        if commit_list != []:
            git('add', commit_list)
            git('commit', '-m', '"{}"'.format(commit_list))
        else:
            print('No files to commit.')

    except Exception as e:
        print(e)
        exit()
