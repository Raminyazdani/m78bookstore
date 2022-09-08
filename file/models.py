from core.models import DBModel
from core.utils import *


class Files(DBModel):  # Files model
    TABLE = 'files'
    PK = 'id'
    name = FileName()
    owner = User_name()
    path = FilePath()
    time_added = ""
    time_modified = ""
    info = Info()

    def __init__(self, name, owner, path, time_added, time_modified, info, id=None) -> None:
        self.name = name
        self.owner = owner
        self.path = path
        self.time_added = time_added
        self.time_modified = time_modified
        self.info = info

        if self.time_added is None:
            self.time_added = create_time()
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
                "time_added": self.time_added,
                "time_modified": self.time_modified,
                "info":self.info,
                "id": self.id}
