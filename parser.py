import requests
from bs4 import BeautifulSoup
import re

def parse_galaxies(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})

    galaxies = []
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:
            cells = row.find_all('td')
            if len(cells) >= 6:
                name = cells[0].text.strip()
                type_galaxy = cells[1].text.strip()
                distance_str = cells[3].text.strip().replace(',', '.').split(' ')[0]
                size_str = cells[4].text.strip().replace(',', '.').split(' ')[0]

                try:
                    distance_str = re.sub(r'[^\d.]', '', distance_str)
                    size_str = re.sub(r'[^\d.]', '', size_str)

                    if not distance_str or distance_str == '.' or distance_str == '..':
                        distance = None
                    else:
                        distance = float(distance_str)

                    if not size_str or size_str == '.' or size_str == '..':
                        size = None
                    else:
                        size = float(size_str)

                    galaxies.append({'name': name, 'type': type_galaxy, 'distance': distance, 'size': size})
                except ValueError:
                    print(f"Ошибка преобразования для галактики: {name}.  Данные: distance='{distance_str}', size='{size_str}'")
                    continue
    else:
        print("Таблица с данными о галактиках не найдена.")

    return galaxies

if __name__ == '__main__':
    url = "https://ru.wikipedia.org/wiki/Список_ближайших_галактик"
    galaxies_data = parse_galaxies(url)
    for galaxy in galaxies_data[:5]:
        print(galaxy)