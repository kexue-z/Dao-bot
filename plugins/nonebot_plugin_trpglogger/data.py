import sqlite3
from pathlib import Path

_DB_FILE = Path() / "data" / "trpglogger" / "log_record.db"

def is_logging(group_id: int):
    result = select_db("logger", ("status",), {"id": group_id})
    if result:
        return True if result[0] else False
    else:
        return False

def get_logger_time(group_id: int):
    result = select_db("logger", ("time",), {"id": group_id})
    if result:
        return result[0]
    else:
        return False

def start_logging(group_id: int, time: int) -> bool:
    insert_db("logger", {"id": group_id, "time": time, "status": 1})

def stop_logging(group_id: int) -> int:
    return update_db("logger", {"status": 0}, {"id": group_id})

def remove_logging(group_id: int):
    return delete_db("logger", {"id": group_id})

def py2sql(value) -> str:
    if isinstance(value, str):
        result = f'"{value}"'
    else:
        result = str(value)
    return result


def create_db():
    _DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(_DB_FILE)
    cur = conn.cursor()
    # 用户数据
    cur.execute(
        """CREATE TABLE IF NOT EXISTS logger (
                id INTEGER PRIMARY KEY NOT NULL,
                time INTEGER NOT NULL,
                status INTEGER NOT NULL)"""
    )
    conn.commit()
    conn.close()


def update_db(table_name: str, columns: dict, condition: dict) -> bool:
    create_db()
    try:
        conn = sqlite3.connect(_DB_FILE)
        cur = conn.cursor()
        sql = f"UPDATE {table_name} SET "
        for i, key in enumerate(columns.keys()):
            if i:
                sql += ","
            sql += f"{key} = {py2sql(columns[key])}"
        sql += " WHERE "
        for i, key in enumerate(condition.keys()):
            if i:
                sql += " AND "
            sql += f"{key} = {py2sql(condition[key])}"
        cur.execute(sql)
        conn.commit()
        conn.close()
        return True
    except:
        return False


def insert_db(table_name: str, columns: dict) -> bool:
    create_db()
    try:
        conn = sqlite3.connect(_DB_FILE)
        cur = conn.cursor()
        sql = f"INSERT INTO {table_name} ("
        for i, key in enumerate(columns.keys()):
            if i:
                sql += ","
            sql += key
        sql += ") VALUES ("
        for i, key in enumerate(columns.keys()):
            if i:
                sql += ","
            sql += py2sql(columns[key])
        sql += ")"
        cur.execute(sql)
        conn.commit()
        conn.close()
        return True
    except:
        return False


def select_db(table_name: str, columns: tuple, condition: dict):
    create_db()
    try:
        conn = sqlite3.connect(_DB_FILE)
        cur = conn.cursor()
        sql = "SELECT "
        for i, value in enumerate(columns):
            if i:
                sql += ","
            sql += value
        sql += f" FROM {table_name} WHERE "
        for i, key in enumerate(condition.keys()):
            if i:
                sql += " AND "
            sql += f"{key} = {py2sql(condition[key])}"
        cur.execute(sql)
        return cur.fetchall()[0]
        conn.close()
    except:
        return False


def delete_db(table_name: str, condition: dict):
    create_db()
    try:
        conn = sqlite3.connect(_DB_FILE)
        cur = conn.cursor()
        sql = f"DELETE FROM {table_name} WHERE "
        for i, key in enumerate(condition.keys()):
            if i:
                sql += " AND "
            sql += f"{key} = {py2sql(condition[key])}"
        cur.execute(sql)
        conn.commit()
        conn.close()
        return True
    except:
        return False


# 测试
if __name__ == "__main__":
    print(get_logger_time(1026597971))
