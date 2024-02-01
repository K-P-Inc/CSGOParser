from pathlib import Path
import time
import os
import traceback
import logging
import hydra
from urllib.parse import quote, urlencode
from omegaconf import DictConfig
from re import A
from dotenv import load_dotenv
from classes import DBClient, SeleniumDriver
from utils import repo_path
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

parsed_items = 0

def get_stickers_dict(db_client):
    stickers_dict = {}
    while len(stickers_dict) == 0:
        logging.info('Getting stickers from database for keys')
        stickers = db_client.get_all_stickers()
        for sticker in stickers:
            key = sticker[2]
            stickers_dict[key] = sticker
        logging.info(f'Fetched {len(stickers_dict)} stickers')
        time.sleep(1)

    return stickers_dict

def get_weapons_array_by_type(db_client, weapon_config):
    global parsed_items
    weapons = []
    weapons_prices = {}

    while len(weapons) == 0:
        logging.info(f'Getting skins from database, already parsed {parsed_items}')
        weapons = db_client.get_all_weapons(weapon_config.min_steam_item_price, weapon_config.max_steam_item_price)
        weapons_prices = {}
        for weapon in weapons:
            if weapon_config.type in weapon[0]:
                key = f'{"StatTrak™ " if weapon[3] == True else ""}{weapon[0]} ({weapon[2]})'
                weapons_prices[key] = weapon[1]

        weapons = sorted(list(set([
            (weapon[0].split(' | ')[0], weapon[0].split(' | ')[1], weapon[3], weapon[2], weapon[4])
            for weapon in weapons
            if weapon[0].split(' | ')[0] == weapon_config.type
        ])))

        if len(weapons) > parsed_items:
            weapons = weapons[parsed_items:]
        else:
            logging.info(f'All items parsed, reseting parsed items counter')
            parsed_items = 0

        logging.info(f'Fetched {len(weapons)} skins from database')
        time.sleep(1)

    return weapons, weapons_prices


def generate_market_link(type, name, quality, is_stattrak):
    return f'https://market.csgo.com/en/?sort=price&order=asc&search={quote(type)}%20%7C%20{quote(name)}%20&priceMax=1000000&categories=any_stickers{"&categories=StatTrak™" if is_stattrak == True else "&categories=Normal"}&quality={quote(quality)}'


def parse_item(
    db_client, driver, actions,
    link, display_name,
    weapon_uuid, weapon_config, weapons_prices, stickers_dict
):
    for_replace_front, for_replace_back = 'background-image: url("https://steamcdn-a.akamaihd.net/apps/730/icons/econ/stickers/', '.png");'
    logging.info(f'Trying to find {display_name}')
    driver.get(link)
    time.sleep(8)
    elements_index = None

    driver.implicitly_wait(10)
    item_url = driver.find_elements(By.XPATH, "//a[contains(@href, '/en/')]")[2:]

    if len(item_url) == 0:
        logging.info(f'No weapons found for {display_name}')
        return

    driver.implicitly_wait(5)

    logging.info(f'Parsing weapon {display_name}')
    while len(item_url) != 0 and elements_index != item_url[-1]:
        logging.info(f'Found {len(item_url)} weapons {display_name}')
        elements_index = item_url[-1]
        for index, i in enumerate(item_url):
            try:
                if i.is_displayed() and len(i.text.splitlines()) <= 2:
                    continue
            except WebDriverException:
                try:
                    if index == len(item_url) - 1:
                        i = driver.find_element(By.XPATH, f"//a[contains(@href, '/en/')][{2 + index}]")
                        elements_index = i
                    else:
                        continue
                except NoSuchElementException:
                    continue
            try:
                key_price = max(i.text.splitlines(), key=len)
                if key_price not in weapons_prices:
                    continue
                market_csgo_item_price = float(i.text.split()[2][1:])
                market_csgo_item_link = i.get_attribute('href')
                sticker_data = i.find_elements(By.XPATH, './/*[starts-with(@class, "stickers")]//*[starts-with(@class, "sticker ")]//*[starts-with(@class, "sticker-img")]')
                stickers_keys = [
                    sticker.get_attribute('style').replace(for_replace_front, '').replace(for_replace_back, '').split('.')[0]
                    for sticker in sticker_data[0:(len(sticker_data)//2)]
                ]
            except:
                continue

            actually_price = weapons_prices[key_price]
            matched_stickers = [stickers_dict[key] for key in stickers_keys if key in stickers_dict]

            if market_csgo_item_price == 0 or len(stickers_keys) == 0 or len(matched_stickers) == 0:
                continue

            sticker_count = {}
            for sticker in matched_stickers:
                key = sticker[2]
                if key in sticker_count:
                    sticker_count[key] += 1
                else:
                    sticker_count[key] = 1

            num_stickers = len(sticker_count)
            sticker_patern = 'other'

            if num_stickers == 1 and max(sticker_count.values()) == 4:
                sticker_patern = 'full-set'
                sticker_overprice = matched_stickers[0][0] * 0.5
            elif num_stickers == 2 and max(sticker_count.values()) == 3:
                sticker_patern = '3-equal'
                equal_sticker_key = max(sticker_count, key=sticker_count.get)
                equal_sticker_price = [sticker[0] for sticker in matched_stickers if sticker[2] == equal_sticker_key][0]
                unequal_sticker_price = [sticker[0] for sticker in matched_stickers if sticker[2] != equal_sticker_key][0] if min(sticker_count.values()) == 1 else 0
                sticker_overprice = equal_sticker_price * 0.25 + unequal_sticker_price * 0.1
            elif num_stickers == 2 and (sorted(sticker_count.values()) == [2, 2] or sorted(sticker_count.values()) == 2):
                sticker_patern = '2-equal'
                equal_sticker_keys = [key for key, count in sticker_count.items() if count == 2]
                equal_sticker_prices = [sticker[0] for sticker in matched_stickers if sticker[2] in equal_sticker_keys[0]][0]
                unequal_sticker_prices = [sticker[0] for sticker in matched_stickers if sticker[2] not in equal_sticker_keys[0]] if min(sticker_count.values()) == 2 else [0]
                sticker_overprice = equal_sticker_prices * 0.15 + sum(unequal_sticker_prices) * 0.15
            elif num_stickers == 3 and max(sticker_count.values()) == 2:
                sticker_patern = '2-equal'
                equal_sticker_keys = [key for key, count in sticker_count.items() if count == 2]
                equal_sticker_prices = [sticker[0] for sticker in matched_stickers if sticker[2] in equal_sticker_keys[0]][0]
                unequal_sticker_prices = [sticker[0] for sticker in matched_stickers if sticker[2] not in equal_sticker_keys[0]] if min(sticker_count.values()) == 2 else [0]
                sticker_overprice = equal_sticker_prices * 0.15 + sum(unequal_sticker_prices) * 0.1
            else:
                sticker_patern = 'other'
                sticker_overprice = sum([sticker[0] for sticker in matched_stickers]) * 0.1

            sticker_sum = sum([sticker[0] for sticker in matched_stickers])
            stickers_names_string = ', '.join([sticker[1] for sticker in matched_stickers])
            future_profit_percentages = (sticker_overprice + actually_price - market_csgo_item_price) / market_csgo_item_price * 100

            if future_profit_percentages > weapon_config.profit_threshold and sticker_sum > weapon_config.sticker_sum:
                query = '''
                    INSERT INTO skins(
                        link, stickers_price, price, profit, skin_id, stickers_patern, amount_of_stickers_distinct, amount_of_stickers, stickers
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (link) DO UPDATE SET
                    stickers_price = EXCLUDED.stickers_price,
                    price = EXCLUDED.price,
                    profit = EXCLUDED.profit,
                    skin_id = EXCLUDED.skin_id,
                    stickers_patern = EXCLUDED.stickers_patern,
                    amount_of_stickers_distinct = EXCLUDED.amount_of_stickers_distinct,
                    amount_of_stickers = EXCLUDED.amount_of_stickers,
                    stickers = EXCLUDED.stickers
                '''
                db_client.execute(query, (
                    market_csgo_item_link,
                    sticker_sum, market_csgo_item_price,
                    future_profit_percentages,
                    weapon_uuid, sticker_patern, num_stickers, len(matched_stickers),
                    [sticker[3] for sticker in matched_stickers]
                ))
                logging.info(
                    f'Found new item:\n\n'
                    f'Link: {market_csgo_item_link}\n'
                    f'Name - price: {key_price} - {market_csgo_item_price:.2f} $\n'
                    f'Steam item price: {actually_price} $\n'
                    f'Found stickers: {stickers_names_string}\n'
                    f'Total stickers price: {sticker_sum:.2f} $, parsed stickers: {len(matched_stickers)}/{len(stickers_keys)}, stickers pattern: {sticker_patern}\n'
                    f'Stickers overprice: {sticker_overprice} $\n'
                    f'Profit: {future_profit_percentages:.2f} %\n\n'
                )

        try:
            if len(item_url) == 83:
                actions.move_to_element(driver.find_element(By.XPATH, "//a[contains(@href, '/en/')][last()]")).perform()
                time.sleep(4)
                item_url = driver.find_elements(By.XPATH, "//a[contains(@href, '/en/')]")[len(item_url) + 2:]
        except:
            pass

def run_action(weapon_config):
    global parsed_items

    try:
        db_client = DBClient()
        driver_class = SeleniumDriver()
        driver = driver_class.driver
        actions = ActionChains(driver)

        stickers_dict = get_stickers_dict(db_client)
        weapons, weapons_prices = get_weapons_array_by_type(db_client, weapon_config)

        for weapon_type, weapon_name, weapon_is_stattrak, weapon_quality, weapon_uuid in weapons:
            link = generate_market_link(weapon_type, weapon_name, weapon_quality, weapon_is_stattrak)
            display_name = f'{"StatTrak™ " if weapon_is_stattrak == True else ""}{weapon_type} | {weapon_name} ({weapon_quality})'
            parse_item(
                db_client=db_client, driver=driver, actions=actions,
                link=link, display_name=display_name,
                weapon_uuid=weapon_uuid, weapon_config=weapon_config, weapons_prices=weapons_prices,
                stickers_dict=stickers_dict
            )

            logging.info(f'Parsed weapon {display_name}')
            parsed_items += 1
    except KeyboardInterrupt:
        logging.info('Closing parsing process (KeyboardInterrupt)')
    except Exception as e:
        logging.error(f'Got exception: {e}')
        logging.error(traceback.format_exc())
        parsed_items += 1
    finally:
        logging.info('End parsing process')

@hydra.main(config_path=str((Path(repo_path()) / 'conf').resolve()), config_name='market_csgo_parser')
def main(cfg: DictConfig):
    while True:
        weapon_type = os.environ.get("WEAPON_TYPE")
        weapon = next((w for w in cfg.weapons if w.type == weapon_type), None)

        if weapon is not None:
            run_action(weapon)
        else:
            logging.info("Weapon not found")

        time.sleep(1)


if __name__ == "__main__":
    load_dotenv()
    main()