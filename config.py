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
import json

from ui import error
import paths

class Config():
    def __init__(self):
        self.defaults = {
            'repo_local' : paths.REPO,
            'repo_remote': '',
            'editor': 'vim',
        }
        self.current = {}
        self.init()

    def validate(self): 
        try:
            f = open(paths.CONFIG, 'r')
            check = json.load(f)
            f.close()
        except:
            return False

        # Compare stored key names against default key names
        if set(self.defaults.keys()) == set(check.keys()):
            return True
        else:
            return False

    def save_defaults(self):
        try:
            f = open(paths.CONFIG, 'w')
            json.dump(self.defaults, f, sort_keys = True, indent = 4)
            f.write('\n')
            f.close()
            return True
        except:
            error('Could not save preferences.')
            return False

    def load(self):
        try:
            f = open(paths.CONFIG, 'r')
            self.current = json.load(f)
            f.close()
            return True
        except:
            error('Could not load configuration.')
            return False

    def save(self):
        try:
            f = open(paths.CONFIG, 'w')
            json.dump(self.current, f, sort_keys = True, indent = 4)
            f.write('\n')
            f.close()
            return True
        except:
            error('Could not save configuration.')
            return False

    def set(self, **kwargs):
        if not self.current.keys() >= kwargs.keys():
            error('Invalid key supplied.')
        else:
            for key, value in kwargs.items():
                self.current[key] = value
            self.save()

    def init(self):
        self.init_program_root()

        # If config.json exists
        if os.path.exists(paths.CONFIG):
            # If keys in file do not match keys in defaults
            if not self.validate():
                self.save_defaults()
        else:
            self.save_defaults()

        # Load whatever is saved on disk
        self.load()

    def init_program_root(self):
        # Check if program root exists and r/w enabled
        try:
            d = open(os.path.join(paths.PROGRAM_ROOT, '.temp_output'), 'w+')
            d.close()
            os.remove(os.path.join(paths.PROGRAM_ROOT, '.temp_output'))
        except:
            try:
                os.makedirs(paths.PROGRAM_ROOT)
                d = open(os.path.join(paths.PROGRAM_ROOT, '.temp_output'), 'w+')
                d.close()
                os.remove(os.path.join(paths.PROGRAM_ROOT, '.temp_output'))
            except:
                error('ERROR: Could not create program root.')
