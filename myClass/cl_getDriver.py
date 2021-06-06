"""
use Selenium
need to Path "chromeDriver"
"""
import os
import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import re
import logging.config
from pathlib import Path


class GetDriver_Selenium ():

    def __init__(self):
        self.logger = logging.getLogger ( __name__ )
        self.options = webdriver.ChromeOptions ()
        # setting_options
        #download_path
        dldir_name='./download'
        dldir_Path=Path(dldir_name)
        dldir_Path.mkdir(exist_ok=True)
        download_path=str(dldir_Path.resolve())
        #headless
        #self.options.add_argument ( '--headless' )

        #保存先を毎回確認しない+選択した保存先を保持
        prefs = {}
        prefs['download.prompt_for_download'] = False
        prefs['download.directory_upgrade'] = True
        self.options.add_experimental_option('prefs', prefs)

        #
        """
        if osVersion == "win":
            self.dPath = r'./driver/win/chromedriver.exe'
        elif osVersion == "mac":
            self.dPath = r'./driver/mac/chromedriver'
        p=pathlib.Path(self.dPath)

        self.dPath=p.resolve()
        logging.debug(self.dPath)
        """
    def getdriver(self, url):
        self.driver = webdriver.Chrome (options=self.options)
        self.driver.get ( url )
        logging.debug(f'getURL={url}')

    def driver_sendCommand(self):
        #ダウンロード有効化
        self.driver.command_executor._commands["send_command"] = (
            'POST',
            '/session/$sessionId/chromium/send_command'
        )

        self.driver.execute(
            "send_command",
            params={
                'cmd': 'Page.setDownloadBehavior',
                'params': {'behavior': 'allow', 'downloadPath': download_path}
            }
        )
    def newTab(self, url):
        self.driver.execute_script ( "window.open()" )
        #ウィンドウハンドルの取得
        handle_array = self.driver.window_handles
        #最終のウィンドウハンドルを取得->最初0
        self.driver.switch_to.window ( handle_array[-1] )
        logging.debug(f'Open NewTab->{url}')
        self.driver.get ( url )
        self.html=self.driver.page_source

    def closeTab(self):
        """
        現在いるタブを閉じて最初のタブ_handle_array[0]に移動
        :return:
        """
        self.driver.close()
        handle_array = self.driver.window_handles
        self.driver.switch_to.window((handle_array[0]))

    def get_dom_xpath(self,query):
        logging.debug(f'getQuery{query}')
        dom = WebDriverWait (self.driver, 10 ).until ( EC.presence_of_element_located ( (By.XPATH, query) ) )
        return dom

    def get_domList_XPath(self,query):
        """
        return dom's list
        :param query:set xpath
        :return:
        """
        WebDriverWait ( self.driver, 10 ).until ( EC.presence_of_all_elements_located )
        doms=self.driver.find_elements_by_xpath(query)
        return doms

    def get_domList_CSS(self,query):
        """
        domのリストを返す
        :param query: CSS
        :return:
        """
        WebDriverWait ( self.driver, 10 ).until ( EC.presence_of_all_elements_located )
        doms=self.driver.find_elements_by_css_selector(query)
        return doms


    def driverWait(self):
        WebDriverWait ( self.driver, 10 ).until ( EC.presence_of_all_elements_located )

    def get_dom_CSS(self,query):
        dom = WebDriverWait (self.driver, 10 ).until ( EC.presence_of_element_located ( (By.CSS_SELECTOR, query) ) )
        logging.debug ( f'getQuery{query}' )
        return dom

    def clickxpath(self, xpath):
        # xpath要素をクリック
        #self.driver.implicitly_wait ( 10 )
        WebDriverWait ( self.driver, 10 ).until ( EC.presence_of_all_elements_located )
        #c = self.driver.find_elements_by_xpath ( xpath )

        try:
            self.driver.find_element_by_xpath ( xpath ).click ()
            logging.debug(f"click_Success->{xpath}")
            return True
        except NoSuchElementException:
            logging.error(f'Not Found->{xpath}')
            return False


        """
        if len ( c ) == 0:
            time.sleep ( 5 )
        else:
            self.driver.find_element_by_xpath ( xpath ).click ()
            logging.debug(f"{xpath}->click_Success")
        """

    def getdriverhandle(self):
        # ドライバハンドル取得
        self.handle_array = self.driver.window_handles
        logging.debug ( f'driverHandle is {self.handle_array}' )
        return self.handle_array

    def changedriverhandle(self, windowNum):
        self.driver.switch_to.window ( self.handle_array[windowNum] )
        logging.debug(f'changeTab->{self.handle_array[windowNum]}')

    def sendkey_xpath(self,xpath,key):
        WebDriverWait ( self.driver, 10 ).until ( EC.presence_of_all_elements_located )
        self.logger.debug(f'send key->{xpath}')
        c=self.driver.find_elements_by_xpath(xpath)
        if len(c)==0:
            self.logger.error(f'selected xpath{xpath} is none')
        else:
            input_box=self.driver.find_element_by_xpath(xpath)
            input_box.send_keys(key)

    def sendlist_xpath(self, xpath_list, keys_list):
        # sendkeys
        #self.driver.implicitly_wait ( 10 )
        WebDriverWait ( self.driver, 10 ).until ( EC.presence_of_all_elements_located )
        self.logger.debug ( xpath )
        for eXpath, eKeys in zip ( xpath_list, keys_list ):
            c = self.driver.find_elements_by_xpath ( eXpath )
            self.logger.debug ( len ( c ) )
            input_box = self.driver.find_element_by_xpath ( eXpath )
            input_box.send_keys ( eKeys )

    def sendkey_id(self, id, key):
        #idにキーを送信
        #self.driver.implicitly_wait ( 10 )
        WebDriverWait ( self.driver, 10 ).until ( EC.presence_of_all_elements_located )
        input_box = self.driver.find_element_by_id ( id )
        input_box.send_keys ( key )

    def sendKey(self, sortValue, typeValue, key):
        # typeValueがlistならfor使用

        if type ( typeValue ) == list:
            multipile = True
        else:
            multipile = False

        if sortValue == "xpath":
            print ( "xpath" )
            pass
        elif sortValue == "id":
            print ( "id" )
            pass
    def get_currentURL(self):
        return self.driver.current_url

    def get_PageSources(self):
        #pagesourceを取得
        return self.driver.page_source

    def QuitDriver(self):
        #seleniumを閉じる
        self.driver.quit ()


