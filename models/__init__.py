from os import getenv

storage_t = getenv("FAVOURS_ENV")

if storage_t == "db":
  from models.engine.db_storage import DbStorage
  storage = DbStorage()
else:
  from models.engine.file_storage import FileStorage
  storage = FileStorage()

storage.reload()
