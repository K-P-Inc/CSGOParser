import time
import brotli
import json
import hydra

import logging
import os

from omegaconf import DictConfig
import pg8000
from dotenv import load_dotenv

from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def connect_to_database():
    try:
        logging.info('Getting connection to the database')
        database = os.environ.get("POSTGRES_DB")
        user = os.environ.get("POSTGRES_USER")
        password = os.environ.get("POSTGRES_PASSWORD")
        host = os.environ.get("POSTGRES_HOST")
        port = os.environ.get("POSTGRES_PORT")
        conn = pg8000.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        logging.info('Connected to the database')
        return conn

    except Exception as e:
        logging.error(f'Got exception: {e}')

    return None

def parse_items_without_link(conn):
    items_id, item_links, csgo_links = [], [], []

    try:
        cur = conn.cursor()
        query = "SELECT id, link, in_game_link FROM skins WHERE ((in_game_link IS NULL or in_game_link = '') AND is_sold = FALSE) or is_sold = FALSE"
        cur.execute(query)
        data_set = cur.fetchall()
        for data in data_set:
            items_id.append(data[0])
            item_links.append(data[1])
            csgo_links.append(data[2])

    except Exception as e:
        logging.error(f'Error while parsing items without link: {e}')

    finally:
        cur.close()

    return item_links, items_id, csgo_links

def update_sold_item(item_id, conn):
    try:
        update_query = "UPDATE skins SET is_sold = TRUE WHERE id = %s"
        cur = conn.cursor()
        cur.execute(update_query, (item_id,))

    except Exception as e:
        logging.error(f'Error while updating sold status in the database for {item_id}: {e}')

    finally:
        cur.close()

def update_link_in_database(in_game_link, item_id, conn):
    try:
        update_query = "UPDATE skins SET in_game_link = %s WHERE id = %s"
        cur = conn.cursor()
        cur.execute(update_query, (in_game_link, item_id))

    except Exception as e:
        logging.error(f'Error while updating link in the database for {item_id}: {e}')
    finally:
        cur.close()

def parser_process(item_link, item_id, csgo_link, conn, driver):
    driver.get(item_link)

    # Open 'View in game page'
    xpath_sold_locator = (By.XPATH, "//*[contains(text(), 'This item has been sold')]")
    xpath_view_locator = (By.XPATH, "//button[@class = 'mat-focus-indicator spinner mat-button mat-button-base']")

    try:
        is_sold = WebDriverWait(driver, timeout=5).until(EC.visibility_of_element_located(xpath_sold_locator))
        if is_sold:
            logging.warning(f'Item {item_link} was sold')
            update_sold_item(item_id, conn)
            conn.commit()
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
            options = webdriver.ChromeOptions()
            options.add_argument('--disable-extensions')
            options.add_argument('--no-sandbox')
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--proxy-server=market_csgo_link_parser:8097')
            seleniumwire_options={
                'auto_config': False,
                'port': 8097,
                'addr': '0.0.0.0'
            }
            capabilities = {
                "browserName": "chrome",
                "selenoid:options": {
                    "enableVNC": True
                }
            }
            capabilities.update(options.to_capabilities())

            logging.info('Connecting to remote driver')
            driver = webdriver.Remote(
                command_executor="http://seleniarm-hub:4444/wd/hub",
                desired_capabilities=capabilities,
                seleniumwire_options=seleniumwire_options
            )

            logging.info('Connecting to database')
            conn = connect_to_database()
            item_links, items_id, csgo_links = parse_items_without_link(conn)

            for item_link, item_id, csgo_link in zip(item_links, items_id, csgo_links):
                try:
                    logging.info(f"Loading item with {item_id} with {item_link}")
                    in_game_link = parser_process(item_link=item_link, item_id=item_id, csgo_link=csgo_link, conn=conn, driver=driver)

                    if in_game_link:
                        logging.info(f"Updating item with {item_id} and link {in_game_link}")
                        update_link_in_database(item_id=item_id, in_game_link=in_game_link, conn=conn)
                        conn.commit()

                except KeyboardInterrupt:
                    logging.info('Closing parsing process (KeyboardInterrupt)')
                    break
                except Exception as e:
                    logging.error(f'Error: {e}')
                    continue


        except Exception as e:
            logging.error(f'Error: {e}')
            time.sleep(3)
        finally:
            if conn:
                conn.close()
            if driver:
                driver.quit()

if __name__ == "__main__":
    load_dotenv()
    main()
