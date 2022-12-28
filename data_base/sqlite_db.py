import sqlite3 as sq
from bot_initializate import bot

#Function started SQL database
def sql_start():
    global base, cur
    base = sq.connect('translate.db')
    cur = base.cursor()
    if base:
        print('DB connected')
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, descriprion TEXT, price TEXT)')
    base.commit()

#Adds information to database
async  def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()
#Show inforimation from database on request
async def sql_get(message):
    for each in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id, each[0], f'Наименование:{each[1]}\nОписание: {each[2]}\nЦена: {each[-1]}')

#Show #2
async def sql_read():
    return cur.execute('SELECT * FROM menu').fetchall()

#Deletet inf from database
async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()

