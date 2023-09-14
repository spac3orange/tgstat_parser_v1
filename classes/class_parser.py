import csv
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains as ac
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time
import json
from .logger import logger


class Parser:
    def __init__(self, settings):
        self.__settings = settings
        self.__data = None

    def __check_filters(self, browser, search_filters):
        inp = browser.find_element(By.ID, 'q')
        inp.send_keys(search_filters['keyword'])
        if search_filters['region'] and search_filters['region'] != 'Russia':
            inp = browser.find_element(By.XPATH, '//span[@class="select2-selection__choice__remove"]')
            inp.click()
            action = ac(browser)
            action.send_keys(search_filters['region'])
            action.send_keys(Keys.ENTER).perform()
            logger.info(f'Set search region to {search_filters["region"]}')
        else:
            logger.info('Set search region to Russia')

        if search_filters['subs']:
            browser.find_element(By.ID, 'participantscountfrom').send_keys(search_filters['subs'][0])
            browser.find_element(By.ID, 'participantscountto').send_keys(search_filters['subs'][1])
            logger.info(f'Subs set to {search_filters["subs"][0]} - {search_filters["subs"][1]}')

        # if search_filters['verified']:
        #     browser.find_element(By.LINK_TEXT, 'Verified ').click()
        #     logger.info('Only Verified = True')

        WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.ID, 'search-form-submit-btn')))
        browser.find_element(By.ID, 'search-form-submit-btn').click()
        time.sleep(5)

        if not self.__check_res(browser):
            sys.exit()

        WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, '//i[@class="uil-list-ul"]')))
        browser.find_element(By.XPATH, '//i[@class="uil-list-ul"]').click()

        WebDriverWait(browser, 100).until(EC.presence_of_element_located(
            (By.XPATH, '//button[@class="btn btn-light border lm-button py-1 min-width-220px"]')))

        shmore = browser.find_element(By.XPATH, '//button[@class="btn btn-light border lm-button py-1 min-width-220px"]')

        try:
            if search_filters['amount']:
                divs = browser.find_elements(By.XPATH, '//div[@class="card peer-item-row mb-2 ribbon-box border"]')
                while len(divs) < search_filters['amount']:
                    shmore.click()
                    WebDriverWait(browser, 5).until(EC.element_to_be_clickable(
                        (By.XPATH, '//button[@class="btn btn-light border lm-button py-1 min-width-220px"]')))
                    divs = browser.find_elements(By.XPATH, '//div[@class="card peer-item-row mb-2 ribbon-box border"]')
            else:
                while shmore:
                    shmore.click()
                    WebDriverWait(browser, 5).until(EC.element_to_be_clickable(
                        (By.XPATH, '//button[@class="btn btn-light border lm-button py-1 min-width-220px"]')))
        except Exception:
            pass

        divs = browser.find_elements(By.XPATH, '//div[@class="card peer-item-row mb-2 ribbon-box border"]')
        return divs

    def scrap_data(self):

        search_filters = {
            'amount': self.__settings.grps_amount,
            'region': self.__settings.region,
            'verified': self.__settings.verify,
            'subs': self.__settings.subs,
            'keyword': self.__settings.keyword,
            'runmode': self.__settings.runmode
        }

        logger.info(f'Scrapping data for <{search_filters["keyword"]}>...')

        options = Options()

        if search_filters['runmode'] == 'headless':
            options.add_argument('--headless')

        with webdriver.Chrome(options=options) as browser:
            browser.get('https://tgstat.com/')
            for i in self.__settings.get_cookie():
                browser.add_cookie(i)
            time.sleep(0.5)
            browser.get('https://tgstat.com/en/channels/search')

            divs = self.__check_filters(browser, search_filters)
            result = []
            for i in divs:
                title = i.find_element(By.XPATH, './/div[@class="text-truncate font-16 text-dark mt-n1"]').text
                subs = i.find_element(By.XPATH, './/div[@class="text-truncate font-14 text-dark mt-n1"]').text
                # avg_seen = i.find_element(By.XPATH, './/div[@class="text_center"]').find_element(By.TAG_NAME, 'h4').text
                link = i.find_element(By.XPATH, './/div[@class="col col-12 col-sm-5 col-md-5 col-lg-4"]').find_element(
                    By.XPATH, './/a')
                # print(title.text, subs.text, avg_seen.text, link)
                link = 'https://t.me/' + link.get_attribute('href').split('/')[-2].lstrip('@')
                # print(title, subs, )
                result.append([title, subs, str(link)])
            logger.info('Data scrapped')
            self.__data = result

    def save_data(self):
        lst = self.__data
        kw = self.__settings.keyword
        filename = self.__settings.filename
        logger.info(f'Scrapped {len(lst)} groups for keyword {kw}')
        save_format = self.__settings.outp_file
        if save_format == 'json':
            self.__write_json(lst, filename)
        elif save_format == 'csv':
            self.__write_csv(lst, filename)

    @staticmethod
    def __write_json(data, filename):
        logger.info('Writing data to json...')
        with open(f'results/{filename}.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            logger.info(f'Data saved in results/"{filename}.json"')

    @staticmethod
    def __write_csv(data, filename):
        logger.info('Writing data to csv...')
        with open(f'results/{filename}.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            for i in data:
                writer.writerow(i)
            logger.info(f'Data saved in results/"{filename}.csv"')

    @staticmethod
    def __check_res(browser):
        try:
            nores = browser.find_element(By.XPATH, '//p[@class="lead"]')
            if nores:
                logger.warning('No results found')
                logger.info('Program stopped')
                return False
        except Exception:
            return True



