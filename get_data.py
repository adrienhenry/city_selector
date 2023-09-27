import argparse
import yaml
from yaml.loader import SafeLoader
from data_collect import get_commune_list,database,get_commune_infos,setup_commune_codes
import pandas as pd
from tqdm import tqdm
from loguru import logger
import json
import sqlite3
from joblib import Parallel, delayed
config = None
def run_commune_infos(commune,config):
    all_infos = get_commune_infos(commune, config)
    database.insert_data(all_infos)
def main():
    global config
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--config", type=str, default="config.yaml", help="Configuration file")
    parser.add_argument("--commune", type=str, help="Commune to get the infos from")
    args = parser.parse_args()
    logger.add("logs/get_data.log", rotation="500 MB")
    with open(args.config, 'r') as f:
        config = yaml.load(f, Loader=SafeLoader)
    if args.commune:
        commune = json.loads(args.commune.replace("'",'"'))
        all_infos = get_commune_infos(commune,config)
        database.insert_data(all_infos)
        return
    
    database.create_commune_database()
    setup_commune_codes(config)
    commune_list = get_commune_list(config)
    logger.info(f"Found {len(commune_list)} communes")
    logger.info("Getting all the communes infos in France")
    for commune in tqdm(commune_list):
        try:
            all_infos = get_commune_infos(commune,config)
            database.insert_data(all_infos)
        except:
            logger.error(f"Error with {commune['simple_name']}({commune['code_commune_INSEE']}))")
            with open("logs/error_communes.log","a") as f:
                f.write(str(commune))
                f.write("\n")
    
if __name__ == "__main__":
    main()