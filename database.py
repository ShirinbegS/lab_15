import sqlite3
import parser

db_file = "galaxies.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TIP (
            id_tipu INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            description TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS GRUPPA (
            id_gruppi INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            description TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS GALAKTIKA (
            id_galaktiki INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            type VARCHAR(255),
            id_gruppi INTEGER,
            distance REAL,
            size REAL,
            FOREIGN KEY (id_gruppi) REFERENCES GRUPPA(id_gruppi),
            FOREIGN KEY (type) REFERENCES TIP(name)
        )
    """)

    conn.commit()


def populate_database(conn, galaxies):
    """
    Заполняет таблицы данными о галактиках.
    """
    cursor = conn.cursor()

    tipi = set(g['type'] for g in galaxies)  
    for tip in tipi:
        cursor.execute("INSERT OR IGNORE INTO TIP (name) VALUES (?)", (tip,)) 

    cursor.execute("INSERT OR IGNORE INTO GRUPPA (name, description) VALUES (?, ?)", ('Местная группа', 'Группа галактик, включающая Млечный Путь'))
    id_gruppi = 1 

    for galaxy in galaxies:
        try:
            cursor.execute("""
                INSERT INTO GALAKTIKA (name, type, id_gruppi, distance, size)
                VALUES (?, ?, ?, ?, ?)
            """, (galaxy['name'], galaxy['type'], id_gruppi, galaxy['distance'], galaxy['size']))
        except sqlite3.IntegrityError as e:
            print(f"Ошибка при вставке галактики {galaxy['name']}: {e}")

    conn.commit()


def top_n_galaxies(conn, n, order_by, ascending=True):
    """Топ N галактик по заданному критерию."""
    cursor = conn.cursor()
    order = "ASC" if ascending else "DESC"
    query = f"""
        SELECT name, distance, size FROM GALAKTIKA
        ORDER BY {order_by} {order}
        LIMIT {n}
    """
    cursor.execute(query)
    return cursor.fetchall()

def galaxies_grouped_by_type(conn):
    """Галактики, сгруппированные по типу."""
    cursor = conn.cursor()
    query = """
        SELECT type, COUNT(*) FROM GALAKTIKA
        GROUP BY type
    """
    cursor.execute(query)
    return cursor.fetchall()

def galaxies_grouped_by_group(conn):
    """Галактики, сгруппированные по группе."""
    cursor = conn.cursor()
    query = """
        SELECT g.name, COUNT(*) FROM GALAKTIKA ga
        JOIN GRUPPA g ON ga.id_gruppi = g.id_gruppi
        GROUP BY g.name
    """
    cursor.execute(query)
    return cursor.fetchall()

galaxies_data = parser.parse_galaxies("https://ru.wikipedia.org/wiki/Список_ближайших_галактик")

create_tables(conn)

populate_database(conn, galaxies_data)

print("База данных успешно создана и заполнена!")

print("Топ 5 ближайших галактик:")
for row in top_n_galaxies(conn, 5, "distance"):
    print(row)

print("\nТоп 3 самых больших галактик:")
for row in top_n_galaxies(conn, 3, "size", ascending=False):
    print(row)

print("\nГалактики, сгруппированные по типу:")
for row in galaxies_grouped_by_type(conn):
    print(row)

print("\nГалактики, сгруппированные по группе:")
for row in galaxies_grouped_by_group(conn):
    print(row)

conn.close()