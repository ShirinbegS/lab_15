def top_n_athletes_by_medals(n=10):
    query = """
    SELECT a.name, c.name as country, 
           (a.medals_gold + a.medals_silver + a.medals_bronze) as total_medals
    FROM athletes a
    JOIN countries c ON a.country_id = c.id
    ORDER BY total_medals DESC
    LIMIT ?
    """
    return query, (n,)

def top_n_countries_by_medals(n=10):
    query = """
    SELECT c.name, 
           SUM(a.medals_gold + a.medals_silver + a.medals_bronze) as total_medals
    FROM countries c
    JOIN athletes a ON c.id = a.country_id
    GROUP BY c.name
    ORDER BY total_medals DESC
    LIMIT ?
    """
    return query, (n,)

def athletes_by_country():
    query = """
    SELECT c.name as country, 
           GROUP_CONCAT(a.name, ', ') as athletes
    FROM countries c
    JOIN athletes a ON c.id = a.country_id
    GROUP BY c.name
    ORDER BY c.name
    """
    return query, ()

def athletes_by_sport():
    query = """
    SELECT s.name as sport, 
           GROUP_CONCAT(a.name, ', ') as athletes
    FROM sports s
    JOIN athletes a ON s.id = a.sport_id
    GROUP BY s.name
    ORDER BY s.name
    """
    return query, ()