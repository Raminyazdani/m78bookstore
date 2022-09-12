from core.models import DBModel
from core.utils import *


class Files(DBModel):  # Files model
    TABLE = 'files'
    PK = 'id'
    name = FileName()
    owner = User_name()
    path = FilePath()
    info = Info()
    time_created = ""
    time_modified = ""

    def __init__(self, name, owner, path, info, time_created=None, time_modified=None, id=None) -> None:
        self.name = name
        self.owner = owner
        self.path = path
        self.time_created = time_created
        self.time_modified = time_modified
        self.info = info

        if self.time_created is None:
            self.time_created = create_time()
        if self.time_modified is None:
            self.time_modified = create_time()
        self.id = id
        if self.id is None:
            self.id = "?"

    @property
    def __dict__(self):
        return {'name': self.name,
                "owner": self.owner,
                "path": self.path,
                "info": self.info,

                "time_created": self.time_created,
                "time_modified": self.time_modified,
                "id": self.id}
