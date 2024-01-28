import time
import brotli
import json
import logging
import os
import pg8000

from seleniumwire import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

def connect_to_database():
    try:
        logging.info('Getting connection to the database')
        database = os.environ.get("POSTGRES_DB")
        user = os.environ.get("POSTGRES_USER")
        password = os.environ.get("POSTGRES_PASSWORD")

        conn = pg8000.connect(
            host="db",
            database=database,
            user=user,
            password=password
        )
        logging.info('Connected to the database')
        return conn

    except Exception as e:
        logging.error(f'Got exception: {e}')

    return None

def parse_items_without_link(conn):
    items_id, item_links = [], []
    
    try:
        cur = conn.cursor()
        query = "SELECT link, id FROM skins WHERE in_game_link IS NULL"
        cur.execute(query)
        data_set = cur.fetchall()
        for data in data_set:
            item_links.append(data[0])
            items_id.append(data[1])

    except Exception as e:
        logging.error(f'Error while parsing items without link: {e}')

    finally:
        cur.close()

    return item_links, items_id

def update_link_in_database(in_game_link, item_id, conn):
    try:
        update_query = "UPDATE skins SET in_game_link = %s WHERE id = %s"
        cur = conn.cursor()
        cur.execute(update_query, (in_game_link, item_id))

    except Exception as e:
        logging.error(f'Error while updating link in the database for {item_id}: {e}')

    return None

def main(item_link, driver):
    driver.get(item_link)

    # Open 'View in game page'
    xpath_route = "//button[@class = 'mat-focus-indicator spinner mat-button mat-button-base']"
    element = driver.find_element(By.XPATH, xpath_route)
    element.click()

    time.sleep(5) # Need this break to get logs update

    for request in driver.requests:
            if not request.response:
                continue

            if request.url != 'https://market.csgo.com/api/graphql':
                continue

            try:
                decompressed_data = brotli.decompress(request.response.body)
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


if __name__ == "__main__":
    options = ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--enable-javascript")
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(60)

    try:
        conn = connect_to_database()
        item_links, items_id = parse_items_without_link(conn)

        for item_link, item_id in zip(item_links, items_id):
            in_game_link = main(item_link=item_link)

            update_link_in_database(item_id=item_id, in_game_link=in_game_link, conn=conn)

    except KeyboardInterrupt:
        logging.info('Closing parsing process (KeyboardInterrupt)')

    except Exception as e:
        logging.error(f'Error: {e}')

    finally:
        conn.commit()
        conn.close()
        driver.quit()
