#!/usr/bin/env python3

import os

JOHNS_HOPKINS_DATA_DIR = os.path.join('data', 'COVID-19')

os.chdir(JOHNS_HOPKINS_DATA_DIR)

os.system('git pull')
