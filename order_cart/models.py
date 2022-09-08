from core.models import DBModel


class Order_cart(DBModel):  # order_cart model
    TABLE = 'order_cart'
    PK = 'id'

    def __init__(self, owner, date_created=None, id=None, items=None) -> None:
        self.owner = owner

        if date_created: self.date_created = date_created
        if items: self.items = items
        if id: self.id = id
