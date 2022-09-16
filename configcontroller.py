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
from ui import ask_confirm, message
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
            except Exception as e:
                print(e)

        self.validate()
        self.load()

    def validate(self):
        # check if config file exists
        if not os.path.exists(paths.CONFIG):
            self.save_defaults()

        while True:
            try:
                # check if config file is readable and if it is valid json
                f = open(paths.CONFIG, 'r')
                check = json.load(f)
                f.close()
                if set(config.defaults.keys()) != set(check.keys()):
                    raise Exception('Config file contains invalid keys.')
            except json.JSONDecodeError as e:
                print('Config file is corrupt.')
                if ask_confirm('Load defaults?'):
                    self.save_defaults()
                else:
                    exit()
            except Exception as e:
                print(e)
                if ask_confirm('Load defaults?'):
                    self.save_defaults()
                else:
                    exit()
            finally:
                break

    def save_defaults(self):
        try:
            f = open(paths.CONFIG, 'w')
            json.dump(config.defaults, f, sort_keys = True, indent = 4)
            f.write('\n')
            f.close()
        except Exception as e:
                print(e)

    def load(self):
        try:
            f = open(paths.CONFIG, 'r')
            config.current = json.load(f)
            f.close()
        except Exception as e:
                print(e)

    def save(self):
        try:
            f = open(paths.CONFIG, 'w')
            json.dump(config.current, f, sort_keys = True, indent = 4)
            f.write('\n')
            f.close()
        except Exception as e:
                print(e)
