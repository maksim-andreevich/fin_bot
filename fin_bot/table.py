import sqlite3

from typing import Dict, List, Tuple

conn = sqlite3.connect("db.db", check_same_thread=False)
cursor = conn.cursor()

# Таблица с расходами
cursor.execute("""create table if not exists expense (user_id integer,
                id integer primary key,
                amount integer,
                created datetime,
                category_codename varchar(255),
                raw_text text,
                FOREIGN KEY(category_codename) REFERENCES category(codename))""")

# Таблица с лимитом бюджета
cursor.execute("""create table if not exists budget
                (codename text primary key,
                daily_limit integer)
                """)

# Таблица с категориями
cursor.execute("""create table if not exists category
                (codename text primary key,
                name text,
                is_base_expense boolean,
                aliases text)
                """)

# Добавление дефолтной категории (не советую убирать этот запрос)
cursor.execute("""insert or ignore into category
                  values ("other", "прочее", 0, "прочее")""")

# Добавление дефолтного лимита
cursor.execute("""insert or ignore into budget
                values ('base', 100)
                """)


# Возвращает курсор
def get_cursor():
    return cursor


# Добавление расхода в БД
def insert_expense(table: str, column_values: Dict):
    columns = ', '.join( column_values.keys() )
    values = [tuple(column_values.values())]
    placeholders = ", ".join( "?" * len(column_values.keys()) )
    cursor.executemany(
        f"INSERT INTO {table}"
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    cursor.execute("""select * from category""")
    a = cursor.fetchall()
    print(a)
    conn.commit()


# Достает все расходы
def fetchall_expense(table: str, columns: List[str]) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


# Удаление расхода
def delete_expense(table: str, row_id: int) -> None:
    row_id = int(row_id)
    cursor.execute(f"delete from {table} where id={row_id}")
    conn.commit()


# Достает категории для удаления
def fetchall_category(table: str, columns: List[str]) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table} WHERE codename!='other'")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


# Добавление категории в БД
def insert_category(table: str, column_values: Dict):
    columns = ', '.join( column_values.keys() )
    values = [tuple(column_values.values())]
    placeholders = ", ".join( "?" * len(column_values.keys()) )
    cursor.executemany(
        f"INSERT INTO {table}"
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


# Удаление категории
def delete_category(table: str, row_id: str) -> None:
    row_id = str(row_id)
    cursor.execute(f"delete from {table} where codename=(?)", (row_id,))
    conn.commit()


# Обновление лимимта
def update_budget(table: str, raw_message: int):
    raw_message = int(raw_message)
    cursor.execute(f"UPDATE {table} SET daily_limit={raw_message} where codename='base'")
    conn.commit()

