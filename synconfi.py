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

import paths
from ui import message, process_input, ask_input
from config import Config
from git import git_init, git, test_connection, check_remote

options = process_input()
config = Config()

if options.restore:
  print('restore')
elif options.add:
  print('add')
elif options.all:
  print('all')
elif options.init:
  message('Testing github connection', 'cyan')
  test_connection()
  repo_remote = ask_input('To begin, please create an empty git repository on github or bitbucket you wish to use with synconfi. When you are done, please enter the ssh address')
  message('Checking remote connection', 'cyan')
  if check_remote(repo_remote):
    config.current['repo_remote'] = repo_remote
    config.save()
  message('Initializing empty repository in {}'.format(paths.REPO), 'cyan')
  git_init()
  message('Disabling showUntrackedFiles', 'cyan')
  git('config', '--local', 'status.showUntrackedFiles', 'no')
  message('Creating first commit', 'cyan')
  git('add', paths.CONFIG)
  git('commit', '-m', '"Synconfi initial commit"')
  message('Adding remote', 'cyan')
  git('remote', 'add', 'origin', config.current['repo_remote'])
  message('Pushing changes to remote', 'cyan')
  git('push', 'origin', 'main')
