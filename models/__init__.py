#!/usr/bin/python3
"""This module instantiates an object of class FileStorage
it follows the following
when the specified environmental variable is set pushes
to DB storage if not there is revert to the default
"""

from os import getenv

# Decide storage based on environment variable
if getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

# Call reload only after storage is defined
storage.reload()
