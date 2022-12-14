import random
import sqlite3

from config import bot


def sql_create():
    global db, cursor
    db = sqlite3.connect("bot.sqlite3")
    cursor = db.cursor()
    if db:
        print('Succesfully Connected!')

    db.execute("CREATE TABLE IF NOT EXISTS products "
               "(tg_id INTEGER PRIMARY KEY,"
               "photo TEXT,"
               "name TEXT, number TEXT, region TEXT,"
               "price INTEGER, description TEXT)")
    db.commit()


async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (data['tg_id'], data['photo'], data['name'], data['number'],
                        data['region'], data['price'], data['description']))
        db.commit()


async def sql_command_all():
    return cursor.execute("SELECT * FROM products").fetchall()


async def sql_command_delete(id):
    cursor.execute("DELETE FROM products WHERE tg_id = ?", (id,))
    db.commit()


async def sql_command_select_type(region):
    return cursor.execute("SELECT * FROM products WHERE region = ?", (region,)).fetchall()


async def sql_command_exists(tg_id):
    return cursor.execute("SELECT * FROM products WHERE tg_id = ?", (tg_id,)).fetchall()


async def sql_command_update(state):
    async with state.proxy() as data:
        cursor.execute(
            "UPDATE products SET photo = ?, name = ?, number = ?, region = ?, price = ?, description = ? WHERE tg_id = ?",
            (data['photo'], data['name'], data['number'], data['region'], data['price'], data['description'],
            data['tg_id']))
        db.commit()