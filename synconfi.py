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
import ui
import commands
import configcontroller

options = ui.process_input()
configcontroller = configcontroller.ConfigController()

def init_repo():
    # set local repo path and create folders
    ui.local_repo(paths.LOCAL_REPO)

    # create local repo
    ui.message('Initializing empty repository in {}'.format(config.current['local_repo']))
    commands.git_init(config.current['local_repo'])

    ui.message('Disabling showUntrackedFiles')
    commands.git('config', '--local', 'status.showUntrackedFiles', 'no')

    ui.message('Creating first commit')
    commands.git('add', paths.CONFIG)
    commands.git('commit', '-m', '"Synconfi initial commit"')

if options.init:
    if os.path.exists(config.current['local_repo']):
        if not ui.ask_confirm('ATTENTION: By re-initializing, the current local repository at {} will be deleted immediately. Are you sure you want to continue?'.format(config.current['local_repo'])):
            exit()
        try:
            shutil.rmtree(config.current['local_repo'])
        except Exception as e:
            print(e)

    init_repo()
    
    if ui.ask_confirm('Do you wish to set up a remote repository now?'):
        # set remote repository, test it and add.
        ui.remote_repo()

        ui.message('Pushing changes to remote')
        commands.git('push', 'origin', 'main')    
    else:
        ui.message('Please don\'t forget to add a remote before pushing changes.')

    ui.message('Saving settings')
    configcontroller.save()
    
    ui.message('Initialization complete.')

if not os.path.exists(config.current['local_repo']):
    ui.message('Local repository not found. Please run --init first.')
    exit()

if options.new:
    print('new')
elif options.restore:
    print('restore')
elif options.all:
    print('all')
elif options.push:
    ui.message('Pushing changes to remote')
    commands.git('push')
elif options.list:
    commands.git('ls-files')
elif options.configure:
    ui.change_config(configcontroller)
else:
    if options.files:
        commands.edit(options.files)
