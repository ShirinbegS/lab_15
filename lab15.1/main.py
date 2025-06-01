from database.db_operations import create_tables, execute_query
from parsing.parser import parse_wikipedia_olympics
from queries.queries import (
    top_n_athletes_by_medals,
    top_n_countries_by_medals,
    athletes_by_country,
    athletes_by_sport
)

def main():
    # Инициализация БД
    create_tables()
    
    # Парсинг данных (пример URL)
    olympics_url = "https://en.wikipedia.org/wiki/List_of_multiple_Olympic_medalists"
    print("Парсинг данных...")
    parse_wikipedia_olympics(olympics_url)
    
    # Выполнение запросов
    print("\nТоп 10 спортсменов по медалям:")
    query, params = top_n_athletes_by_medals(10)
    for row in execute_query(query, params):
        print(f"{row[0]} ({row[1]}) - {row[2]} медалей")
    
    print("\nТоп 10 стран по медалям:")
    query, params = top_n_countries_by_medals(10)
    for row in execute_query(query, params):
        print(f"{row[0]} - {row[1]} медалей")
    
    print("\nСпортсмены по странам:")
    query, params = athletes_by_country()
    for row in execute_query(query, params):
        print(f"\n{row[0]}:\n{row[1]}")
    
    print("\nСпортсмены по видам спорта:")
    query, params = athletes_by_sport()
    for row in execute_query(query, params):
        print(f"\n{row[0]}:\n{row[1]}")

if __name__ == "__main__":
    main()