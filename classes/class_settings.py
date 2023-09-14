import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains as ac
from selenium.webdriver.common.keys import Keys
import json
import os
import time
from .logger import logger

class Settings:
    def __init__(
            self, cookie: dict = None, subs: tuple = None, grps_amount: int = None, region: str = None,
            verify: bool = None, keyword: str = None, outp_file: str = 'json', runmode: str = None, filename: str
            = None):

        #cookie
        if self.__check_cookie('cookies/cookies.json'):
            logger.info('Cookies found')
            self.__cookie = self.__open_json('cookies/cookies.json')
        else:
            logger.warning('Cookies not found')
            logger.info('Scrapping for cookies...')
            logger.info('You have to login with telegram and then press continue')
            self.__scrap_cookie()

        #scrap options
        self.keyword = keyword
        self.subs = subs  # (min | max)
        self.grps_amount = grps_amount
        self.region = region
        self.verify = verify
        self.outp_file = outp_file
        self.runmode = runmode
        self.filename = filename

    def __scrap_cookie(self):
        with webdriver.Chrome() as browser:
            browser.get('https://tgstat.com/')
            browser.set_window_size(900, 550)
            browser.find_element(By.LINK_TEXT, 'Sign In').click()
            time.sleep(0.5)
            browser.find_element(By.LINK_TEXT, 'Sign in with Telegram').click()
            a = int(input('Have you logged in with telegram?\n1 - Yes\n0 - No\n'))
            time.sleep(2)
            if a == 1:
                browser.switch_to.window(browser.window_handles[0])
                action = ac(browser)
                action.send_keys(Keys.ESCAPE)
                action.send_keys(Keys.F5).perform()
                cookies = browser.get_cookies()
                self.__cookie = cookies
                logger.info('Cookies set')
                with open('cookies/cookies.json', 'w') as file:
                    json.dump(cookies, file, indent=4, ensure_ascii=False)
                logger.info('Cookies saved in cookies/"cookies.json"')
            else:
                sys.exit()

    def get_cookie(self):
        return self.__cookie


    @staticmethod
    def __open_json(path):
        with open(path) as file:
            cookies = json.load(file)
            return cookies

    @staticmethod
    def __check_cookie(path):
        return os.path.exists(path)
