from core.models import DBModel
from core.utils import *


class Order_item(DBModel):  # order_item model
    TABLE = 'order_item'
    PK = 'id'
    file_id = FileId()
    order_cart = FileId()
    time_created = ""

    def __init__(self, file_id, order_cart_id, time_created=None, id=None) -> None:
        self.file_id = file_id
        self.order_cart_id = order_cart_id
        self.time_created = time_created
        if self.time_created is None:
            self.time_created = create_time()
        self.id = id
        if self.id is None:
            self.id = "?"

    @property
    def __dict__(self):
        return {"file_id": self.file_id,
                "order_cart_id": self.order_cart_id,
                "time_created": self.time_created,
                "id": self.id}
