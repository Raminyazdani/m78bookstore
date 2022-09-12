from core.models import DBModel
from core.utils import *


class Order_cart(DBModel):  # order_cart model
    TABLE = 'order_cart'
    PK = 'id'
    owner_id_cart = User_name()
    items = Items()
    time_created = ""

    def __init__(self, owner_id_cart, items=None, time_created=None, id=None) -> None:
        self.owner_id_cart = owner_id_cart
        self.time_created = time_created
        self.items = items
        if self.time_created is None:
            self.time_created = create_time()

        self.id = id
        if self.id is None:
            self.id = "?"

    @property
    def __dict__(self):
        return {"owner_id_cart": self.owner_id_cart,
                "items": self.items,
                "time_created": self.time_created,
                "id": self.id}
