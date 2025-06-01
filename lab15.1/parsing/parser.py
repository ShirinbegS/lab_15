import requests
from bs4 import BeautifulSoup
from database.db_operations import insert_country, insert_sport, insert_athlete

def parse_wikipedia_olympics(url):
    """Парсер для Wikipedia страницы с олимпийскими медалями"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Находим все таблицы на странице
        tables = soup.find_all('table', {'class': 'wikitable'})
        if not tables:
            print("Не найдено таблиц с классом 'wikitable'")
            return []
        
        athletes_data = []
        
        # Берем первую подходящую таблицу
        table = tables[0]
        
        for row in table.find_all('tr')[1:]:  # Пропускаем заголовок
            cols = row.find_all(['th', 'td'])
            try:
                # Более гибкое извлечение данных
                name = cols[0].get_text(strip=True)
                country = cols[1].get_text(strip=True)
                sport = cols[2].get_text(strip=True)
                
                # Ищем колонки с медалями (может быть разное количество колонок)
                medals = []
                for col in cols[3:]:
                    text = col.get_text(strip=True)
                    if text.isdigit():
                        medals.append(int(text))
                    elif text:  # Если не число, но не пустое
                        medals.append(0)
                
                # Если нашли меньше 3 значений медалей, дополняем нулями
                while len(medals) < 3:
                    medals.append(0)
                
                gold, silver, bronze = medals[:3]
                
                # Добавляем страну и вид спорта в БД
                country_id = insert_country(country)
                sport_id = insert_sport(sport)
                
                # Добавляем спортсмена
                athlete_id = insert_athlete(
                    name=name,
                    country_id=country_id,
                    sport_id=sport_id,
                    gold=gold,
                    silver=silver,
                    bronze=bronze
                )
                
                athletes_data.append({
                    'name': name,
                    'country': country,
                    'sport': sport,
                    'gold': gold,
                    'silver': silver,
                    'bronze': bronze
                })
                
            except (IndexError, ValueError, AttributeError) as e:
                print(f"Ошибка обработки строки: {e}. Пропускаем...")
                continue
        
        return athletes_data
    
    except Exception as e:
        print(f"Ошибка при парсинге: {e}")
        return []