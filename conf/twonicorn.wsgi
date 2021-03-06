#  Copyright 2015 CityGrid Media, LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import os
# CHANGEME - if you don't install in /app
activate_this = "/app/twonicorn_web/venv/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))

from pyramid.paster import get_app, setup_logging
# CHANGEME - if you don't install in /app
ini_path = '/app/twonicorn_web/conf/twonicorn-web.ini'
setup_logging(ini_path)
application = get_app(ini_path, 'main')
