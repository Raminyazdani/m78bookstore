from core.models import DBModel
from core.utils import *


class Comment(DBModel):  # order_item model
    TABLE = 'comments'
    PK = 'id'
    file_id = FileId()
    owner = User_name()
    info = Info()
    time_created = ""

    def __init__(self, file_id, owner, info, time_created=None, id=None) -> None:
        self.file_id = file_id
        self.owner = owner
        self.info = info
        self.time_created = time_created
        if self.time_created is None:
            self.time_created = create_time()

        self.id = id
        if self.id is None:
            self.id = "?"

    @property
    def __dict__(self):
        return {"file_id": self.file_id,
                "owner": self.owner,
                "info": self.info,
                "time_created": self.time_created,
                "id": self.id}
