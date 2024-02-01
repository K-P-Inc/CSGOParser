import time
import brotli
import json
import hydra
import logging
from omegaconf import DictConfig
from dotenv import load_dotenv
from classes import DBClient, SeleniumWireDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def update_sold_item(item_id, db_client):
    try:
        update_query = "UPDATE skins SET is_sold = TRUE WHERE id = %s"
        db_client.execute(update_query, (item_id,))

    except Exception as e:
        logging.error(f'Error while updating sold status in the database for {item_id}: {e}')

def update_link_in_database(in_game_link, item_id, db_client):
    try:
        update_query = "UPDATE skins SET in_game_link = %s WHERE id = %s"
        db_client.execute(update_query, (in_game_link, item_id))

    except Exception as e:
        logging.error(f'Error while updating link in the database for {item_id}: {e}')


def parser_process(item_link, item_id, csgo_link, db_client, driver):
    driver.get(item_link)

    # Open 'View in game page'
    xpath_sold_locator = (By.XPATH, "//*[contains(text(), 'This item has been sold')]")
    xpath_view_locator = (By.XPATH, "//button[@class = 'mat-focus-indicator spinner mat-button mat-button-base']")

    try:
        is_sold = WebDriverWait(driver, timeout=5).until(EC.visibility_of_element_located(xpath_sold_locator))
        if is_sold:
            logging.warning(f'Item {item_link} was sold')
            update_sold_item(item_id, db_client)
            return None

    except TimeoutException:
        pass

    if csgo_link:
        return None

    element = WebDriverWait(driver, timeout=5).until(EC.visibility_of_element_located(xpath_view_locator))
    element.click()

    time.sleep(5) # Need this break to get logs update

    for request in driver.requests:
        if not request.response:
            continue

        if request.url != 'https://market.csgo.com/api/graphql':
            continue

        try:
            decompressed_data = brotli.decompress(request.response.body)
            logging.info(f"Decoding decopressed data {decompressed_data}")
            decoded_json = json.loads(decompressed_data.decode('utf-8'))

            if 'data' not in decoded_json or 'getInGameLink' not in decoded_json['data']:
                logging.warning("Invalid JSON structure")
                continue

            in_game_link = decoded_json['data']['getInGameLink'].get('gameLink')
            if in_game_link and 'steam://rungame/' in in_game_link:

                return in_game_link

        except UnicodeDecodeError:
            pass # Skip decode error, becouse we don't need other value
        except Exception as e:
            logging.error(f'Error processing request: {e}')


@hydra.main(config_path=f'/app/conf', config_name='market_csgo_link_parser')
def main(cfg: DictConfig):
    while True:
        try:
            driver_class = SeleniumWireDriver()
            driver = driver_class.driver
            db_client = DBClient()

            item_links, items_id, csgo_links = db_client.parse_items_without_link()

            for item_link, item_id, csgo_link in zip(item_links, items_id, csgo_links):
                try:
                    logging.info(f"Loading item with {item_id} with {item_link}")
                    in_game_link = parser_process(item_link=item_link, item_id=item_id, csgo_link=csgo_link, db_client=db_client, driver=driver)

                    if in_game_link:
                        logging.info(f"Updating item with {item_id} and link {in_game_link}")
                        update_link_in_database(item_id=item_id, in_game_link=in_game_link, db_client=db_client)

                except KeyboardInterrupt:
                    logging.info('Closing parsing process (KeyboardInterrupt)')
                    break
                except Exception as e:
                    logging.error(f'Error: {e}')
                    continue
        except Exception as e:
            logging.error(f'Error: {e}')
            time.sleep(3)


if __name__ == "__main__":
    load_dotenv()
    main()
