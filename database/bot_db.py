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
        cursor.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?)")
        db.commit()


async def sql_command_random(message):
    result = cursor.execute("SELECT * FROM products").fetchall()
    random_product = random.choice(result)
    await bot.send_photo(message.from_user.id, random_product[1],
                         caption=f"Имя: {random_product[2]}")