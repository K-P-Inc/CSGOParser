from pathlib import Path
import time
import os
import traceback
import logging
import hydra
import requests
import json
from urllib.parse import urlparse, unquote_plus
from omegaconf import DictConfig
from re import A
from dotenv import load_dotenv
from classes import DBClient, SeleniumDriver
from utils import repo_path
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

ORDER_DELETED_ERROR_CODE = 404
parsed_items = 0

def do_request(link, name, id):
    url = "https://market.csgo.com/api/graphql"

    payload = json.dumps({
        "operationName": "viewItem",
        "variables": { "market_hash_name": name, "id": f'{id}' },
        "query": "query viewItem($id: String, $market_hash_name: String!, $phase: String) {\n  viewItem(id: $id, market_hash_name: $market_hash_name, phase: $phase) {\n    asset\n    color\n    price\n    itemtype\n    quality\n    popularity\n    ctp\n    seo {\n      category\n      type\n      __typename\n    }\n    meta {\n      title\n      description\n      __typename\n    }\n    jsonSchema\n    rarity\n    rarity_ext {\n      id\n      name\n      __typename\n    }\n    slot\n    stattrak\n    stattrak_name\n    quality\n    links {\n      view_3d\n      view_in_game\n      view_screenshot\n      view_refresh_image\n      __typename\n    }\n    stickers {\n      image\n      name\n      id\n      price\n      currency\n      __typename\n    }\n    tags {\n      category\n      category_name\n      internal_name\n      localized_category_name\n      localized_tag_name\n      name\n      value {\n        link\n        name\n        __typename\n      }\n      __typename\n    }\n    type\n    currency\n    descriptions {\n      type\n      value\n      rarity\n      __typename\n    }\n    features\n    float {\n      paintindex\n      paintseed\n      paintwear\n      screenshot\n      __typename\n    }\n    id\n    my_item\n    my_order {\n      price\n      total\n      __typename\n    }\n    my_notify {\n      price\n      __typename\n    }\n    status\n    image_512\n    market_hash_name\n    market_name\n    market_name_ext {\n      subtitle\n      title\n      __typename\n    }\n    quality_ext {\n      id\n      subtitle\n      title\n      __typename\n    }\n    phase\n    phase_short\n    seller {\n      nick\n      avatar\n      chance_to_transfer\n      steam_lvl\n      profile\n      hidden\n      __typename\n    }\n    __typename\n  }\n}"
    })

    headers = {
        'Referer': link,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    try:
        if json.loads(response.text) and json.loads(response.text)["data"]["viewItem"]:
            return json.loads(response.text)["data"]["viewItem"]
        if json.loads(response.text) and json.loads(response.text)["errors"]:
            return json.loads(response.text)["errors"]
        return None
    except:
        time.sleep(5)
        return None


def update_sold_item(item_id, db_client):
    try:
        update_query = "UPDATE skins SET is_sold = TRUE WHERE id = %s"
        db_client.execute(update_query, (item_id,))

    except Exception as e:
        logging.error(f'Error while updating sold status in the database for {item_id}: {e}')

def update_deleted_item(item_id, db_client):
    try:
        update_query = "UPDATE skins SET is_deleted = TRUE WHERE id = %s"
        db_client.execute(update_query, (item_id,))

    except Exception as e:
        logging.error(f'Error while updating deleted status in the database for {item_id}: {e}')

@hydra.main(config_path=str((Path(repo_path()) / 'conf').resolve()), config_name='market_csgo_parser_item_status_api')
def main(cfg: DictConfig):
    global ORDER_DELETED_ERROR_CODE

    while True:
        try:
            db_client = DBClient()

            item_links, items_id, csgo_links = db_client.parse_items_without_link()

            for item_link, item_id, csgo_link in zip(item_links, items_id, csgo_links):
                try:
                    logging.info(f"Loading item with {item_id} with {item_link}")

                    parsed_url = urlparse(item_link)
                    path_parts = parsed_url.path.split('/')
                    last_path_part = path_parts[-1]
                    decoded_last_path_part = unquote_plus(last_path_part)
                    query_params = parsed_url.query.split('=')
                    item_market_id = query_params[-1]

                    item_dict = do_request(item_link, decoded_last_path_part, item_market_id)

                    logging.info(f"Item status by market id {item_market_id} with name {decoded_last_path_part} was loaded: {item_dict}")

                    if item_dict and "status" in item_dict and item_dict["status"] == "SOLD":
                        logging.info(f"Updating item with {item_id} because it was sold")
                        update_sold_item(item_id=item_id, db_client=db_client)
                    elif item_dict and hasattr(item_dict, "__len__") and len(item_dict) > 0 and "code" in item_dict[0] and item_dict[0]["code"] == ORDER_DELETED_ERROR_CODE:
                        logging.info(f"Updating item with {item_id} because it was deleted or order was changed")
                        update_deleted_item(item_id=item_id, db_client=db_client)

                    time.sleep(5)
                except KeyboardInterrupt:
                    logging.info('Closing parsing process (KeyboardInterrupt)')
                    break
                except Exception as e:
                    logging.error(f'Error: {e}')
                    traceback.print_exc()
                    continue
        except Exception as e:
            logging.error(f'Error: {e}')
            time.sleep(3)


if __name__ == "__main__":
    load_dotenv()
    main()