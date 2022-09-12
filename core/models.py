from abc import ABC
from core.query import *


class DBModel(ABC):  # abstract base Database model
    TABLE: str  # table name
    PK: str  # primary key column of the table

    def __repr__(self):
        return f"{self.__class__.__name__} {vars(self)}"

    def __str__(self) -> str:
        return f"{self.__class__.__name__} {vars(self)}"

    @property
    def db_check_database_table(self):
        query = manager_db_check_database_table(self)
        return query

    @property
    def db_create_table(self):
        query = manager_db_create_table(self)
        return query

    @property
    def db_delete_table(self):
        query = manager_db_delete_table(self)
        return query

    @property
    def db_insert_to_table(self):
        query = manager_db_insert_to_table(self)
        return query

    @classmethod
    def db_read_from_table(cls, pk=None):
        query = manager_db_read_from_table(cls, pk)
        return query

    @classmethod
    def db_check_database_table_model(cls):
        query = manager_db_check_database_table_model(cls)
        return query

    @classmethod
    def db_create_table_model(cls):
        query = manager_db_create_table_model(cls)
        return query

    @property
    def db_update_to_table(self):
        query = manager_db_update_to_table(self)
        return query

    @property
    def db_delete_from_table(self):
        query = manager_db_delete_from_table(self)
        return query
