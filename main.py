#TODO：株式投資メモからcsvファイルをダウンロード
#targetURL=f'>https://kabuoji3.com/stock/{stockNum}/'
from myClass.cl_getDriver import GetDriver_Selenium
import time
import logging.config

logging.config.fileConfig ( './logging.conf' )
logger = logging.getLogger ()

from pprint import pprint


targetURL='https://kabuoji3.com/stock/1308/'
logging.debug(f'start_Process->{targetURL}')
myDriver=GetDriver_Selenium()
myDriver.getdriver(targetURL)

domlist=myDriver.get_domList_XPath("//div[@id='base_box']/div[@class='base_box_body']/ul[@class='stock_yselect mt_10']/li/a")

urllist=[elem.get_attribute("href") for elem in domlist]

for tUrl in urllist:
    """
    要素のクリックができなかったので、urlを取得し新規タブを開いていく形に変更
    """
    try:
        myDriver.newTab(tUrl)
        #//*[@id="base_box"]/div/div[3]/form/button
        myDriver.clickxpath('//*[@id="base_box"]/div/div[3]/form/button')
        time.sleep(2)
        #// *[ @ id = "base_box"] / div / div[3] / form / button
        myDriver.clickxpath ( '//*[@id="base_box"]/div/div[3]/form/button' )

        myDriver.closeTab()

    except Exception as e:
        eMes=f'type:{str(type(e))}\nargs:{str(e.args)}\nmes:{str(e.message)}\n{str(e)}'
        logging.error(eMes)

myDriver.QuitDriver()
logging.debug(f'finished Process->{targetURL}')

