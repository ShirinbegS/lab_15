-- Создание таблицы стран
CREATE TABLE IF NOT EXISTS countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    population INTEGER,
    gdp REAL
);

-- Создание таблицы видов спорта
CREATE TABLE IF NOT EXISTS sports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

-- Создание таблицы спортсменов
CREATE TABLE IF NOT EXISTS athletes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    birth_date TEXT,
    gender TEXT,
    country_id INTEGER,
    sport_id INTEGER,
    medals_gold INTEGER DEFAULT 0,
    medals_silver INTEGER DEFAULT 0,
    medals_bronze INTEGER DEFAULT 0,
    FOREIGN KEY (country_id) REFERENCES countries (id),
    FOREIGN KEY (sport_id) REFERENCES sports (id)
);