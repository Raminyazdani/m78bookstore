from routes import router
from users.models import User
from core.managers import DBManager
from file.models import Files

if __name__ == "__main__":
# router.generate()
    DB = DBManager("test")

    x = User("ramin", "yazdani", "ramin_yz", "yazdani76ramin@gmail.com", "09124981090", "0020349629", "24",
             "RAmin@12345")
    res = DB.insert_table(x)
    DB.conn.commit()
    w = DB.read(User)
    DB.conn.commit()
    DB.conn.close()