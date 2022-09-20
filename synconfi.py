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
import shutil

import paths
import config
from ui import process_input, change_config, local_repo, remote_repo, ask_confirm, ask_input, message
from commands import git_init, git, edit
from configcontroller import ConfigController

options = process_input()
configcontroller = ConfigController()

def init_repo():
    # set local repo path and create folders
    local_repo(paths.LOCAL_REPO)

    # create local repo
    message('Initializing empty repository in {}'.format(config.current['local_repo']))
    git_init(config.current['local_repo'])

    message('Disabling showUntrackedFiles')
    git('config', '--local', 'status.showUntrackedFiles', 'no')

    message('Creating first commit')
    git('add', paths.CONFIG)
    git('commit', '-m', '"Synconfi initial commit"')

def add_remote():
    # set remote repository and test it
    remote_repo()

    # add remote to local repository and perform initial push
    message('Adding remote')
    git('remote', 'add', 'origin', config.current['remote_repo'])
    message('Pushing changes to remote')
    git('push', 'origin', 'main')

if options.init:
    if os.path.exists(config.current['local_repo']):
        if not ask_confirm('ATTENTION: By re-initializing, the current local repository at {} will be deleted immediately. Are you sure you want to continue?'.format(config.current['local_repo'])):
            exit()
        try:
            shutil.rmtree(config.current['local_repo'])
        except Exception as e:
            print(e)

    init_repo()
    
    if ask_confirm('Do you wish to set up a remote repository now?'):
        add_remote()      
    else:
        message('Please don\'t forget to add a remote before pushing changes.')

    message('Saving settings')
    configcontroller.save()
    
    message('Initialization complete.')

if not os.path.exists(config.current['local_repo']):
    message('Local repository not found. Please run --init first.')
    exit()

if options.restore:
    print('restore')
elif options.new:
    print('new')
elif options.push:
    message('Pushing changes to remote')
    git('push')
elif options.all:
    print('all')
elif options.configure:
    change_config(configcontroller)
else:
    if options.files:
        edit(options.files)
