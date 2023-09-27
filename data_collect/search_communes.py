import requests
from bs4 import BeautifulSoup
from loguru import logger
from tqdm import tqdm


def analyse_departement_link(link_soup):
    url = link_soup.get("href")
    departement_code = url.split("/")[-1].replace("departement-", "")
    departement_name = link_soup.get("title").replace("Prix immobilier ", "")
    return {
        "url": url,
        "departement_code": departement_code,
        "departement_name": departement_name,
    }


def analyse_commune_link(link_soup):
    url = link_soup.get("href")
    commune_code = url.split("/")[-1].replace("ville-", "")
    simple_name = url.split("/")[-2]
    return {
        "code_commune_INSEE": commune_code,
        "simple_name": simple_name,
    }


def get_departement_infos(url_source):
    """Get the list of all the departements in France, with their code, their name, and their url"""
    all_departements_raw_text = requests.get(url_source).text
    with open("test.html", "w") as f:
        f.write(all_departements_raw_text)
    all_departements_soup = BeautifulSoup(all_departements_raw_text, "html.parser")
    all_departements_soup_links = all_departements_soup.select_one(
        'div[class="section-wrapper mapael jMap1"]'
    ).find_all("a")
    all_departements_infos = [
        analyse_departement_link(link) for link in all_departements_soup_links
    ]
    return all_departements_infos


def get_commune_links(departement_infos):
    """Get the list of all the communes in a departement, with their code, their name, and their url"""
    all_communes_raw_text = requests.get(departement_infos["url"]).text
    all_communes_soup = BeautifulSoup(all_communes_raw_text, "html.parser")
    all_communes_soup_links = [
        link
        for link in all_communes_soup.find_all("a", {"class": "h-decoration-underline"})
        if link.get("href").split("/")[-1].startswith("ville-")
    ]
    return all_communes_soup_links


def get_commune_list(config):
    url_source = config["data"]["seed_m2_prices"]["url"]
    logger.info("Getting all the departements in France")
    all_departements_infos = get_departement_infos(url_source)
    all_communes_links = []
    logger.info("Getting all the communes links in France")
    for departement_infos in tqdm(all_departements_infos):
        all_communes_links += get_commune_links(departement_infos)
    logger.info("Getting all the communes infos in France")
    all_communes = [analyse_commune_link(link) for link in tqdm(all_communes_links)]
    unique_communes = []
    commune_ids = []
    for commune in all_communes:
        if commune["code_commune_INSEE"] not in commune_ids:
            commune_ids.append(commune["code_commune_INSEE"])
            unique_communes.append(commune)
    return unique_communes
