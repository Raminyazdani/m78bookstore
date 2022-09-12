from routes import router
from users.models import User
from file.models import Files
from comment.models import Comment
from order_cart.models import Order_cart
from order_item.models import Order_item
from core.managers import DBManager

if __name__ == "__main__":
    # router.generate()
    DB = DBManager("test")

    x = User("ramin", "yazdani", "ramin_yz", "yazdani76ramin@gmail.com", "09124981090", "0020349629", "24",
             "RAmin@12345")
    DB.insert_table(x)
    w = DB.read(User)
    print("users\n",w)

    y = Files("ketab", "ramin_yz", "C://desktop/","ketabe darsi")
    DB.insert_table(y)
    w = DB.read(Files)
    print("files\n",w)

    z = Comment("1", "ramin_yz", "asdasdasda")
    DB.insert_table(z)
    w = DB.read(Files)
    print("comments\n",w)

    n = Order_cart("ramin_yz")
    DB.insert_table(n)
    w = DB.read(Files)
    print("order_carts\n",w)

    m = Order_item("1","1")
    DB.insert_table(m)
    w = DB.read(Files)
    print("order_items\n",w)


    DB.conn.close()
