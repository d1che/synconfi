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

from singleton import Singleton
from ui import error, message
import paths
import config

class ConfigController(metaclass=Singleton):

    def __init__(self):
        # initialize program root
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
            except Exception as err:
                error('{}'.format(err))

        # if config.json exists
        if os.path.exists(paths.CONFIG):
            # If keys in file do not match keys in defaults
            if not self.validate():
                self.save_defaults()
                message('Config file was corrupt so defaults were loaded', 'yellow')
        else:
            self.save_defaults()

        # load whatever is saved on disk
        self.load()

    def validate(self):
        try:
            f = open(paths.CONFIG, 'r')
            check = json.load(f)
            f.close()
        except:
            return False

        # Compare stored key names against default key names
        if set(config.defaults.keys()) == set(check.keys()):
            return True
        else:
            return False

    def save_defaults(self):
        try:
            f = open(paths.CONFIG, 'w')
            json.dump(config.defaults, f, sort_keys = True, indent = 4)
            f.write('\n')
            f.close()
            return True
        except:
            error('Could not save preferences.')

    def load(self):
        try:
            f = open(paths.CONFIG, 'r')
            config.current = json.load(f)
            f.close()
            return True
        except:
            error('Could not load configuration.')

    def save(self):
        try:
            f = open(paths.CONFIG, 'w')
            json.dump(config.current, f, sort_keys = True, indent = 4)
            f.write('\n')
            f.close()
            return True
        except:
            error('Could not save configuration.')
