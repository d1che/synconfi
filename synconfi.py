#!/usr/bin/env python3

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

import paths
from ui import message, error, process_input, ask_confirm, ask_input
from config import Config
from commands import test_connection, check_remote, git_init, git, edit

options = process_input()

config = Config()

def init_repo():
    try:
        repo_local = ask_input('First, specify a path for the local git repository ({})'.format(config.current['repo_local']),
            config.current['repo_local'])
        config.set(repo_local=repo_local)
        message('Initializing empty repository in {}'.format(config.current['repo_local']), 'cyan')
        git_init(repo_local)
        message('Disabling showUntrackedFiles', 'cyan')
        git('config', '--local', 'status.showUntrackedFiles', 'no')
        message('Creating first commit', 'cyan')
        git('add', paths.CONFIG)
        git('commit', '-m', '"Synconfi initial commit"')
    except Exception as err:
        error('{}'.format(err))
        exit()

def add_remote():
    try:
        repo_remote = ask_input('Next, lease create an empty git repository on github or bitbucket you wish to use with synconfi. When you are done, please enter the ssh address')
        message('Testing github connection', 'cyan')
        test_connection()
        message('Checking remote connection', 'cyan')
        if check_remote(repo_remote):
            config.set(repo_remote=repo_remote)
        message('Adding remote', 'cyan')
        git('remote', 'add', 'origin', config.current['repo_remote'])
        message('Pushing changes to remote', 'cyan')
        git('push', 'origin', 'main')
    except Exception as err:
        error('{}'.format(err))
        exit()

if options.restore:
    print('restore')
elif options.new:
    print('new')
elif options.push:
    print('push')
elif options.all:
    print('all')
elif options.init:
    if os.path.exists(config.current['repo_local']):
        if not ask_confirm('This will re-initialize the local git repository. Are you sure you want to continue?'):
            exit()
    init_repo()
    if ask_confirm('Do you wish to set up a remote repository now?'):
        add_remote()      
        message('Initialization complete.')
    else:
        message('Initialization complete. Please don\'t forget to add a remote before pushing changes.', 'cyan')
elif options.configure:
    print('configure')
else:
    if not os.path.exists(config.current['repo_local']):
        message('Local repository not found. Please run --init first.', 'cyan')
    pass#edit(options.files)
