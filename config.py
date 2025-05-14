#  configuration file

import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI= 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATION: False