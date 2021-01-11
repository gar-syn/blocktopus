import os
from pathlib import Path
from os.path import join as pjoin
from distutils.dir_util import mkpath

from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend

from octopus.blocktopus.database.createdb import createdb

if __name__ == "__main__":
    DATA_DIR = '/app/data'

    print ("Creating Data Directories")

    if not Path(pjoin(DATA_DIR, 'sketches')).exists():
        mkpath(pjoin(DATA_DIR, 'sketches'))
        print ("Sketches data directory created")

    if not Path(pjoin(DATA_DIR, 'experiments')).exists():
        mkpath(pjoin(DATA_DIR, 'experiments'))
        print ("Experiments data directory created")

    if not Path(pjoin(DATA_DIR, 'octopus.db')).exists():
        createdb(DATA_DIR)
        print ("Database created")
