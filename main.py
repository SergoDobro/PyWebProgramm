import uvicorn
from fastapi import FastAPI, Body
from fastapi.responses import PlainTextResponse
import sqlite3
from enum import Enum, auto

class DBAction(Enum):
    fetchone = auto()
    fetchall = auto()
    commit = auto()

def db_action(sql: str, args: tuple, action: DBAction):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute(sql, args)
    if action == DBAction.fetchone:
        result = cursor.fetchone()
    elif action == DBAction.fetchall:
        result = cursor.fetchall()
    elif action == DBAction.commit:
        conn.commit()
        result = None
    cursor.close()
    conn.close()
    return result

app = FastAPI()



@app.on_event('startup')
def create_db():
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        create table if not exists users (
        id integer primary_key,
        username varchar not null,
        password varchar not null
        );
    ''')
    cursor.close()


@app.get('/')
def MainPageIntro():
    return PlainTextResponse("Welcome!/nHave a nice day!")


@app.post('/login')
def login(username: str = Body(...), password: str = Body(...)):

    user = db_action('''
        select * from users where username = ? and password = ?
    ''', (username, password), DBAction.fetchone)
    if user == None:
        return "Failed to log in"
    return "Successfully logged in"

@app.post('/redister')
def test(username: str = Body(...), password: str = Body(...)):

    res = db_action('''
        insert into users (username, password) values (?, ?)
    ''', (username, password), DBAction.commit)
    return "Success"

uvicorn.run(app)
