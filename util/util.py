import os
import hashlib
from pathlib import Path

path =  Path(__file__).parent.parent
dbname = "SQL/NetflixDB.sqlite3"


def dbpath():
    return "sqlite:///" + os.path.join(path, dbname)

def hashpassword(password):
    return hashlib.sha512(password.encode('utf-8')).hexdigest()