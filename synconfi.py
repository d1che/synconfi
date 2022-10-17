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

import commands
import config
import configcontroller
import paths
import remote
import ui

options = ui.process_input()
configcontroller = configcontroller.ConfigController()
remote = remote.Remote()

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

def change_config():
    while True:
        print('1) Move local repository')
        print('2) Add/change remote repository')
        print('3) Change prefered editor')
        print('4) Show config file')
        print('q) Quit')
        answer = ui.ask_input('Please make your choice')

        match answer:
            case '1':
                ui.local_repo()
                configcontroller.save()
            case '2':
                remote.new()
                configcontroller.save()
            case '3':
                print('Please enter the name of the editor you wish to use (an alias is also valid, if it accepts an argument)')
                e = ui.ask_input('Editor', 'vim')
                config.current['editor'] = e
                configcontroller.save()
            case '4':
                print(configcontroller.print())
            case 'q' | 'Q':
                break
            case _:
                print('Incorrect answer') 

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
        remote.new()

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
    change_config()
else:
    if options.files:
        commands.edit(options.files)
