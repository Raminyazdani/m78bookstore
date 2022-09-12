import psycopg2
import psycopg2.extras
from core.models import DBModel
from configs import DB_CONNECTION
from psycopg2._psycopg import connection, cursor


class DBManager:
    HOST = DB_CONNECTION["HOST"]
    USER = DB_CONNECTION["USER"]
    PORT = DB_CONNECTION["PORT"]
    PASSWORD = DB_CONNECTION["PASSWORD"]

    def __init__(self, database, user=USER, host=HOST, port=PORT, password=PASSWORD) -> None:
        self.database = database
        self.user = user
        self.host = host
        self.port = port
        self.password = password
        self.conn: connection = \
            psycopg2.connect(dbname=self.database, user=self.user, host=self.host, port=self.port, password=password)

    def __del__(self):
        self.conn.close()  # Close the connection on delete

    def get_cursor(self) -> cursor:
        # Changing the fetch output from Tuple to Dict utilizing RealDictCursor cursor factory
        # return self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def check_table_exists(self, model_instance: DBModel) -> bool:
        query = model_instance.db_check_database_table
        cursor = self.get_cursor()
        cursor.execute(query)
        self.conn.commit()
        y = cursor.fetchall()
        result: bool = y[0]["exists"]
        return result

    def check_table_exists_model(self, model_class: DBModel) -> bool:
        query = model_class.db_check_database_table_model()
        cursor = self.get_cursor()
        cursor.execute(query)
        self.conn.commit()
        y = cursor.fetchall()
        result: bool = y[0]["exists"]
        return result

    def create_table(self, model_instance: DBModel) -> bool:
        query = model_instance.db_create_table
        cursor = self.get_cursor()
        try:
            cursor.execute(query)
            self.conn.commit()
            return True
        except:
            cursor.execute("rollback")
            return False

    def create_table_model(self, model_class: DBModel) -> bool:
        query = model_class.db_create_table_model()
        cursor = self.get_cursor()
        try:
            cursor.execute(query)
            self.conn.commit()
            return True
        except:
            cursor.execute("rollback")
            return False

    def delete_table(self, model_instance: DBModel) -> bool:
        if self.check_table_exists(model_instance):

            query = model_instance.db_delete_table
            cursor = self.get_cursor()
            try:
                cursor.execute(query)
                self.conn.commit()
                return True
            except:
                cursor.execute("rollback")
                return False
        else:
            return False

    def insert_table(self, model_instance: DBModel) -> bool:
        if self.check_table_exists(model_instance):
            query = model_instance.db_insert_to_table
            cursor = self.get_cursor()
            try:
                cursor.execute(query)
                self.conn.commit()
                return True
            except:
                cursor.execute("rollback")
                print("duplicated input for ",list(model_instance.__dict__.items())[0])
                self.conn.commit()
                return False
        else:
            print("table not exists")
            print("creating new table",model_instance.__class__.__dict__['TABLE'])
            self.create_table(model_instance)
            self.insert_table(model_instance)
            self.conn.commit()


    def read(self, model_class, pk=None) -> DBModel or list:  # get
        """
            returns an instance of the Model with inserted values
        """
        if self.check_table_exists_model(model_class):

            if pk is not None:
                query = model_class.db_read_from_table(pk)
                cursor = self.get_cursor()
                try:
                    cursor.execute(query)
                    result = cursor.fetchone()
                    self.conn.commit()
                    return model_class(**dict(result))
                except:
                    cursor.execute("rollback")
                    print("Could not read model from table")
            else:
                query = model_class.db_read_from_table()
                cursor = self.get_cursor()
                try:
                    cursor.execute(query)
                    self.conn.commit()
                    result = cursor.fetchall()
                    result_list = [model_class(**dict(x)) for x in result]
                    return result_list
                except:
                    cursor.execute("rollback")
                    print("Could not read models from table")
        else:
            print("table not exists")
            print("creating new table",model_class.__dict__["TABLE"])
            self.create_table_model(model_class)

    def update(self, model_instance: DBModel) -> bool:
        """
            update instance in db table by get all model_instance attrs
        """
        if self.check_table_exists(model_instance):

            query = model_instance.db_update_to_table
            cursor = self.get_cursor()
            try:
                cursor.execute(query)
                self.conn.commit()
                return True
            except:
                cursor.execute("rollback")
                print("Could not update model")
                return False
        else:
            print("table not exists")
            print("creating new table",model_instance.__class__.__dict__['TABLE'])
            self.create_table(model_instance)

    def delete(self, model_instance: DBModel) -> bool:
        """
            delete instance method
        """
        if self.check_table_exists(model_instance):

            query = model_instance.db_delete_from_table
            cursor = self.get_cursor()
            try:
                cursor.execute(query)
                self.conn.commit()
                return True
            except:
                cursor.execute("rollback")
                print("Could not delete")
                return False
        else:
            print("table not exists")
            return False
