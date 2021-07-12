import os
from pathlib import Path


class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    static_dir = str(Path(basedir,'static'))
    templates_dir = str(Path(basedir, 'templates'))
    data_dir = {'default': str(Path(basedir, 'data'))}

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
