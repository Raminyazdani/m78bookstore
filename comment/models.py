from core.models import DBModel


class Order_item(DBModel):  # order_item model
    TABLE = 'order_item'
    PK = 'id'

    def __init__(self, file_id, order_cart_id, date_added=None ,id=None) -> None:
        self.file_id = file_id
        self.order_cart_id = order_cart_id

        if date_added:self.date_added = date_added

        if id: self.id = id
