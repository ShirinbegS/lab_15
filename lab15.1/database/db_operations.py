import sqlite3
from contextlib import contextmanager

DATABASE = 'sports.db'

@contextmanager
def db_connection():
    conn = sqlite3.connect(DATABASE)
    try:
        yield conn
    finally:
        conn.close()

def create_tables():
    with db_connection() as conn:
        with open('database/schema.sql', 'r') as f:
            conn.executescript(f.read())
        conn.commit()

def insert_country(name, population=None, gdp=None):
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO countries (name, population, gdp) VALUES (?, ?, ?)",
            (name, population, gdp)
        )
        conn.commit()
        return cursor.lastrowid

def insert_sport(name, description=None):
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO sports (name, description) VALUES (?, ?)",
            (name, description)
        )
        conn.commit()
        return cursor.lastrowid

def insert_athlete(name, country_id, sport_id, birth_date=None, gender=None, 
                   gold=0, silver=0, bronze=0):
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO athletes 
            (name, country_id, sport_id, birth_date, gender, medals_gold, medals_silver, medals_bronze) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (name, country_id, sport_id, birth_date, gender, gold, silver, bronze)
        )
        conn.commit()
        return cursor.lastrowid

def execute_query(query, params=None):
    with db_connection() as conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()