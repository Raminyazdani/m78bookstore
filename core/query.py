from core.utils import table_column_types, unique_table_column_types


def manager_db_insert_to_table(instance):
    query = f"INSERT INTO {instance.__class__.__dict__['TABLE']}"
    keys, values = ",".join(list(vars(instance).keys())[:-1]), "','".join(list(vars(instance).values())[:-1])
    return f"{query} ({keys}) VALUES ('{values}');"


def manager_db_read_from_table(class_name, pk):
    if pk is not None:
        return f"SELECT * FROM {class_name.__dict__['TABLE']} WHERE id='{pk}';"
    else:
        return f"SELECT * FROM {class_name.__dict__['TABLE']}"


def manager_db_update_to_table(instance):
    query = f"UPDATE {instance.__class__.__dict__['TABLE']} SET "
    query += ",".join([f"{key}='{value}'" for key, value in list(instance.__dict__.items())[:-1]])
    query += f" WHERE id={instance.id};"
    return query


def manager_db_delete_from_table(instance):
    return f"DELETE FROM {instance.__class__.__dict__['TABLE']} WHERE id={vars(instance)['id']};"


def manager_db_check_database_table(instance):
    return f"""SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name='{instance.__class__.__dict__['TABLE']}');"""


def manager_db_check_database_table_model(class_name):
    return f"""SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name='{class_name.__dict__['TABLE']}');"""


def manager_db_create_table(instance):
    query = f"CREATE TABLE {instance.__class__.__dict__['TABLE']} ( id serial PRIMARY KEY," + ",".join(
        [f"{key} {table_column_types.get(key)}" for key in list(vars(instance).keys())[:-1]])
    adding = list(filter(lambda x: x in unique_table_column_types, list(vars(instance).keys())))
    if len(adding) > 0:
        query += f", CONSTRAINT {instance.__class__.__dict__['TABLE']}_const UNIQUE ({','.join(adding)})"

    query += ");"
    return query


def manager_db_delete_table(instance):
    return f"DROP TABLE {instance.__class__.__dict__['TABLE']}"


def manager_db_create_table_model(class_name):
    query = f"CREATE TABLE {class_name.__dict__['TABLE']} ( id serial PRIMARY KEY," + ",".join(
        [f"{key} {table_column_types.get(key)}" for key in list(vars(class_name).keys())[3:-4]])
    adding = list(filter(lambda x: x in unique_table_column_types, list(vars(class_name).keys())))
    if len(adding) > 0:
        query += f", CONSTRAINT {class_name.__dict__['TABLE']}_const UNIQUE ({','.join(adding)})"
    query += ");"
    return query