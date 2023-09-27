import sqlite3


def create_commune_database():
    """
    Create a database with the list of all the cities in France
    """
    con = sqlite3.connect("commune.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS commune")
    cur.execute(
        """CREATE TABLE commune(
    code_commune_INSEE INTEGER PRIMARY KEY,
    simple_name TEXT,
    name TEXT,
    code_postal INTEGER,
    latitude REAL,
    longitude REAL,
    population INTEGER,
    density REAL,
    median_age REAL,
    avg_temperture REAL,
    avg_max_temperature REAL,
    avg_min_temperature REAL,
    avg_sunshine REAL,
    heat_wave_days INTEGER,
    avg_rainfall REAL,
    raindays INTEGER,
    ice_days INTEGER,
    median_income REAL,
    unemployment_rate REAL,
    highspeed_internet_rate REAL,
    avg_price_m2 REAL,
    crime_rate REAL,
    distance_to_nearest_doctor REAL,
    distance_to_nearest_dentist REAL,
    distance_to_nearest_pharmacy REAL,
    distance_to_nearest_hospital REAL,
    distance_to_nearest_hypemarket REAL,
    distance_to_nearest_supermarket REAL,
    distance_to_nearest_grocery REAL,
    distance_to_nearest_bakery REAL,
    distance_to_nearest_daycare REAL,
    distance_to_nearest_library REAL,
    distance_to_nearest_cinema REAL,
    distance_to_nearest_school REAL,
    distance_to_nearest_Collège REAL,
    distance_to_nearest_Lycée REAL,
    distance_to_nearest_train_station REAL,
    time_to_lucies_parents REAL,
    distance_to_lucies_parents REAL,
    time_to_adriens_parents REAL,
    distance_to_adriens_parents REAL
    )"""
    )
    con.commit()
    con.close()


def insert_data(commune_infos):
    for key in [
        "code_commune_INSEE",
        "simple_name",
        "code_postal",
        "latitude",
        "longitude",
        "name",
        "avg_price_m2",
        "population",
        "density",
        "median_age",
        "avg_temperture",
        "avg_max_temperature",
        "avg_min_temperature",
        "avg_sunshine",
        "heat_wave_days",
        "avg_rainfall",
        "raindays",
        "ice_days",
        "median_income",
        "unemployment_rate",
        "highspeed_internet_rate",
        "crime_rate",
        "distance_to_nearest_doctor",
        "distance_to_nearest_dentist",
        "distance_to_nearest_pharmacy",
        "distance_to_nearest_hospital",
        "distance_to_nearest_daycare",
        "distance_to_nearest_school",
        "distance_to_nearest_Collège",
        "distance_to_nearest_Lycée",
        "distance_to_nearest_hypemarket",
        "distance_to_nearest_supermarket",
        "distance_to_nearest_grocery",
        "distance_to_nearest_bakery",
        "distance_to_nearest_cinema",
        "distance_to_nearest_library",
        "distance_to_nearest_train_station",
        "time_to_lucies_parents",
        "distance_to_lucies_parents",
        "time_to_adriens_parents",
        "distance_to_adriens_parents",
    ]:
        commune_infos[key] = commune_infos.get(key, None)
    con = sqlite3.connect("commune.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO commune (code_commune_INSEE, simple_name, code_postal, latitude, longitude, name, avg_price_m2, population, density, median_age, avg_temperture, avg_max_temperature, avg_min_temperature, avg_sunshine, heat_wave_days, avg_rainfall, raindays, ice_days, median_income, unemployment_rate, highspeed_internet_rate, crime_rate, distance_to_nearest_doctor, distance_to_nearest_dentist, distance_to_nearest_pharmacy, distance_to_nearest_hospital, distance_to_nearest_daycare, distance_to_nearest_school, distance_to_nearest_Collège, distance_to_nearest_Lycée, distance_to_nearest_hypemarket, distance_to_nearest_supermarket, distance_to_nearest_grocery, distance_to_nearest_bakery, distance_to_nearest_cinema, distance_to_nearest_library, distance_to_nearest_train_station, time_to_lucies_parents, distance_to_lucies_parents, time_to_adriens_parents, distance_to_adriens_parents) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            commune_infos["code_commune_INSEE"],
            commune_infos["simple_name"],
            commune_infos["code_postal"],
            commune_infos["latitude"],
            commune_infos["longitude"],
            commune_infos["name"],
            commune_infos["avg_price_m2"],
            commune_infos["population"],
            commune_infos["density"],
            commune_infos["median_age"],
            commune_infos["avg_temperture"],
            commune_infos["avg_max_temperature"],
            commune_infos["avg_min_temperature"],
            commune_infos["avg_sunshine"],
            commune_infos["heat_wave_days"],
            commune_infos["avg_rainfall"],
            commune_infos["raindays"],
            commune_infos["ice_days"],
            commune_infos["median_income"],
            commune_infos["unemployment_rate"],
            commune_infos["highspeed_internet_rate"],
            commune_infos["crime_rate"],
            commune_infos["distance_to_nearest_doctor"],
            commune_infos["distance_to_nearest_dentist"],
            commune_infos["distance_to_nearest_pharmacy"],
            commune_infos["distance_to_nearest_hospital"],
            commune_infos["distance_to_nearest_daycare"],
            commune_infos["distance_to_nearest_school"],
            commune_infos["distance_to_nearest_Collège"],
            commune_infos["distance_to_nearest_Lycée"],
            commune_infos["distance_to_nearest_hypemarket"],
            commune_infos["distance_to_nearest_supermarket"],
            commune_infos["distance_to_nearest_grocery"],
            commune_infos["distance_to_nearest_bakery"],
            commune_infos["distance_to_nearest_cinema"],
            commune_infos["distance_to_nearest_library"],
            commune_infos["distance_to_nearest_train_station"],
            commune_infos["time_to_lucies_parents"],
            commune_infos["distance_to_lucies_parents"],
            commune_infos["time_to_adriens_parents"],
            commune_infos["distance_to_adriens_parents"],
        ),
    )
    con.commit()
    con.close()
