import pandas as pd
from urllib.request import urlretrieve


def get_csv(url, keys):
    data = pd.read_csv(url)
    return data[keys]


def get_geocom(config):
    urlretrieve(
        config["data"]["city_codes"]["url"], config["data"]["city_codes"]["file"]
    )
