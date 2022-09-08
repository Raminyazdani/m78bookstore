from core.models import DBModel
from core.utils import *


class User(DBModel):  # User model
    TABLE = 'users'
    PK = 'id'
    first_name = First_name()
    last_name = Last_name()
    username = User_name()
    email = Email()
    phone = Phone()
    national_id = National_id()
    age = Age()
    password = Password()
    time_created = ""
    time_modified = ""

    def __init__(self, first_name, last_name, username, email, phone, national_id, age, password, time_created=None,
                 time_modified=None, id=None) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.phone = phone
        self.national_id = national_id
        self.age = age
        self.password = password
        self.time_created = time_created
        self.time_modified = time_modified
        if self.time_created is None:
            self.time_created = create_time()
        if self.time_modified is None:
            self.time_modified = create_time()
        self.id = id
        if self.id is None:
            self.id = "?"

    @property
    def __dict__(self):
        return {'first_name': self.first_name,
                "last_name": self.last_name,
                "username": self.username,
                "email": self.email,
                "phone": self.phone,
                "national_id": self.national_id,
                "age": self.age,
                "password": self.password,
                "time_created": self.time_created,
                "time_modified": self.time_modified,
                "id": self.id}


if __name__ == '__main__':
    x = User("ramin", "yazdani", "ramin_yz", "yazdani7ramin@gmail.com", "09124981090", "0020349629", "24",
             "RAmin@12345")
    print(x)
    print(vars(x))
    print(x.__class__.__dict__["TABLE"])
