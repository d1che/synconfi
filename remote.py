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
import subprocess

import commands
import config
import helpers
import paths
import ui

class Remote:

    def __init__(self):
        self.address = None
        self.pull = False
        self.files = []

    def new(self):
        if commands.git('remote') != '':
            self.address = commands.git('remote', 'get-url', 'origin')
        else:
            self.address = None
        self.pull = False
        print('Please provide a remote address. A remote address has to be an ssh\naddress to either:\n\t1. A freshly initialized remote repository, or\n\t2. An existing remote repository that was previously used with synconfi')
        while True:
            address = ui.ask_input('Remote address')

            # check if new remote is the same as current remote
            if address == self.address:
                print('This remote is already setup as the current remote.')
            else:
                ui.message('Testing github connection')
                commands.test_connection()
                ui.message('Checking remote connection')
                
                # if remote is not empty
                if commands.ls_remote(address) != '':
                    if self.pull_data(address):
                        if self.validate():
                            if ui.ask_confirm(helpers.format_sentences('{} seems to be a valid remote synconfi repository. Would you like to use this remote to pull from?'.format(address))):
                                self.pull = True
                                break
                        else:
                            print(helpers.format_sentences('{} is not a valid remote repository to use with synconfi, please enter a different address.').format(address))
                    else:
                        print(helpers.format_sentences('Could not pull from {}'.format(address)))
                        exit()
                else:
                    break

        # remove old remote if present
        if commands.git('remote') == 'origin':
            commands.git('remote', 'remove', 'origin')

        # add new remote
        if self.address == None:
            ui.message('Adding remote {}'.format(address))
        else:
            ui.message('Updating remote {}'.format(address))
        commands.git('remote', 'add', 'origin', address)
        commands.git('push', '--set-upstream', 'origin', 'main')

        if self.pull:
            # Copy all pulled files to local system
            pass

        # update address
        self.address = address

        ui.message('Successfully updated remote repository')

    def pull_data(self, remote):
        try:
            if os.path.isdir(paths.TEMP):
                shutil.rmtree(paths.TEMP)
            os.makedirs(paths.TEMP)

            output = subprocess.run([
                'git',
                'clone',
                '--bare',
                '--depth=1',
                '{}'.format(remote),
                '{}'.format(paths.TEMP)],
                capture_output=True)

            return True

        except Exception as e:
            print(e)
            return False

    def validate(self):
        try:
            output = subprocess.run([
                'git',
                '--git-dir={}'.format(paths.TEMP),
                'ls-tree',
                '--name-only',
                '-r',
                'HEAD'],
                capture_output=True)

            self.files = output.stdout.decode("utf-8").strip()

            if '.config/synconfi/config.json' in self.files:
                return True
            else:
                return False

        except Exception as e:
            print(e)
            exit()

    def compare():
        # compare local data to remote data
        pass

    def delete_data(self):
        try:
            shutil.rmtree(paths.TEMP)
            return True
        except Exception as e:
            print(e)
            return False
