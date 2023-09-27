import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import math

all_commune_codes = {}


def setup_commune_codes(config):
    global all_commune_codes
    if len(all_commune_codes) == 0:
        all_commune_codes = pd.read_csv(config["data"]["city_codes"]["url"])
        all_commune_codes["code_commune_INSEE"] = all_commune_codes[
            "code_commune_INSEE"
        ].apply(lambda x: x.replace(" ", "") if len(str(x)) == 5 else "0" + str(x))
        all_commune_codes = all_commune_codes.set_index("code_commune_INSEE")


def get_m2_price(soup=None):
    try:
        return float(
            soup.find("div", {"class": "od-same-cols"})
            .find("strong")
            .text.replace("\xa0", "")[:-5]
        )
    except AttributeError:
        return math.nan


def get_commune_codes(code_commune_INSEE, config):
    global all_commune_codes
    try:
        ref_data = all_commune_codes.loc[str(code_commune_INSEE)]
    except KeyError:
        import pdb

        pdb.set_trace()
    if len(ref_data.shape) > 1:
        ref_data = ref_data.iloc[0]
    return {
        "code_postal": int(ref_data["code_postal"]),
        "latitude": float(ref_data["latitude"]),
        "longitude": float(ref_data["longitude"]),
        "name": ref_data["nom_commune_complet"],
    }


def get_demography(soup):
    numbers = soup.find("div", {"class": "info-demographie"}).find_all(
        "p", {"class": "big-number"}
    )
    return {
        "population": float(numbers[0].text.replace(" ", "")),
        "density": float(numbers[2].text.replace("\u202f", "")),
        "median_age": float(re.search("\d+", numbers[3].text).group(0)),
    }


def get_climate(soup):
    elmts = soup.find("section", {"id": "climat"}).find_all("p")
    find_temp = lambda x: float(re.search("-?\d+(.\d+)?", x).group(0))
    return {
        "avg_temperture": find_temp(elmts[0].text),
        "avg_max_temperature": find_temp(elmts[1].text),
        "avg_min_temperature": find_temp(elmts[2].text),
        "avg_sunshine": float(re.search(r"(\d+) heure", elmts[3].text).group(1)),
        "heat_wave_days": int(re.search(r"(\d+) jours", elmts[3].text).group(1)),
        "avg_rainfall": float(re.search(r"(\d+)mm", elmts[4].text).group(1)),
        "raindays": int(re.search(r"(\d+) jours", elmts[4].text).group(1)),
        "ice_days": int(re.search(r"(\d+) jours", elmts[5].text).group(1)),
    }


def search_income(elmt):
    try:
        return float(re.search("[\d\u202f]+", elmt).group(0).replace("\u202f", ""))
    except AttributeError:
        return math.nan


def search_unemployment(elmt):
    try:
        return float(re.search("[\d\,]+", elmt).group(0).replace(",", "."))
    except AttributeError:
        return math.nan


def search_highspeed(elmt):
    try:
        return float(re.search("[\d\,]+", elmt).group(0).replace(",", "."))
    except AttributeError:
        return math.nan


def get_economy(soup):
    elmts = soup.find("section", {"id": "economie"}).find_all("p")

    return {
        "median_income": search_income(elmts[0].text),
        "unemployment_rate": search_unemployment(elmts[2].text),
        "highspeed_internet_rate": search_highspeed(elmts[4].text),
    }


def extract_service_distance(elmt):
    try:
        int(elmt)
        return 0
    except ValueError:
        return float(re.search("[\d\,]+", elmt).group(0).replace(",", "."))


def get_services(soup):
    elmts = soup.find("section", {"id": "services"}).find_all("span")
    return {
        "distance_to_nearest_doctor": extract_service_distance(elmts[0].text),
        "distance_to_nearest_dentist": extract_service_distance(elmts[1].text),
        "distance_to_nearest_pharmacy": extract_service_distance(elmts[3].text),
        "distance_to_nearest_hospital": extract_service_distance(elmts[4].text),
        "distance_to_nearest_daycare": extract_service_distance(elmts[5].text),
        "distance_to_nearest_school": extract_service_distance(elmts[6].text),
        "distance_to_nearest_Collège": extract_service_distance(elmts[8].text),
        "distance_to_nearest_Lycée": extract_service_distance(elmts[9].text),
        "distance_to_nearest_hypemarket": extract_service_distance(elmts[10].text),
        "distance_to_nearest_supermarket": extract_service_distance(elmts[11].text),
        "distance_to_nearest_grocery": extract_service_distance(elmts[12].text),
        "distance_to_nearest_bakery": extract_service_distance(elmts[13].text),
        "distance_to_nearest_cinema": extract_service_distance(elmts[19].text),
        "distance_to_nearest_library": extract_service_distance(elmts[20].text),
        "distance_to_nearest_train_station": extract_service_distance(elmts[21].text),
    }


def all_commune_infos(soup):
    infos = {
        **get_demography(soup),
        **get_climate(soup),
        **get_economy(soup),
        "crime_rate": float(
            soup.find("section", {"id": "securite"})
            .find("p")
            .text.replace("\u202f", "")
        ),
        **get_services(soup),
    }
    return infos


def get_url_soup(url):
    return BeautifulSoup(requests.get(url).text, "html.parser")


def get_distanceto_parent(commune_infos, parent_infos, config, name):
    parent_infos.update(get_commune_codes(parent_infos["code_commune_INSEE"], config))
    url = f"{config['data']['driving_distances']['url']}/{commune_infos['longitude']},{commune_infos['latitude']};{parent_infos['longitude']},{parent_infos['latitude']}"
    route = requests.get(url).json()
    return {
        f"time_to_{name}": route["routes"][0]["duration"] / 3600,
        f"distance_to_{name}": route["routes"][0]["distance"] / 1000,
    }


def get_commune_infos(commune_infos, config):
    simple_name = commune_infos["simple_name"]
    code_commune_INSEE = commune_infos["code_commune_INSEE"]

    commune_infos.update(get_commune_codes(code_commune_INSEE, config))
    figaro_soup = get_url_soup(
        f"{config['data']['seed_m2_prices']['url']}/{simple_name}/ville-{code_commune_INSEE}"
    )
    commune_infos["avg_price_m2"] = get_m2_price(figaro_soup)
    villesavivre_soup = get_url_soup(
        f"{config['data']['villes_a_vivre']['url']}/{simple_name}-{code_commune_INSEE}"
    )
    if ("Page non trouvée" not in villesavivre_soup.title.text) and (
        "Server error" not in villesavivre_soup.title.text
    ):
        commune_infos.update(all_commune_infos(villesavivre_soup))
    commune_infos.update(
        get_distanceto_parent(
            commune_infos, config["data"]["lucies_parents"], config, "lucies_parents"
        )
    )
    commune_infos.update(
        get_distanceto_parent(
            commune_infos, config["data"]["adriens_parents"], config, "adriens_parents"
        )
    )
    return commune_infos
