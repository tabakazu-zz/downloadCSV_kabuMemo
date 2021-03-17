#TODO：株式投資メモからcsvファイルをダウンロード
#targetURL=f'>https://kabuoji3.com/stock/{stockNum}/'
from myClass.cl_getDriver import GetDriver_Selenium
import time
import logging.config
import concurrent.futures

logging.config.fileConfig ( './logging.conf' )
logger = logging.getLogger ()
from tqdm import tqdm
from pprint import pprint

def downloadFile(target):
    targetURL=f'https://kabuoji3.com/stock/{target}/'
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

if __name__ == '__main__':
    """
    17業種コードを引数に入力
    """
    from sqlAlchemy.curd import cli_sql
    from sqlalchemy import text
    from sqlAlchemy.models import table_Stock_Code
    import sys

    args=sys.argv

    cli_sql = cli_sql()
    session = cli_sql.get_session()

    stockCodelist = session.query(table_Stock_Code.codeNum). \
        filter(table_Stock_Code.tiCode_17 == 5). \
        all()
    #print(stockCodelist)


    executor=concurrent.futures.ThreadPoolExecutor(max_workers=2)
    for elem in tqdm(stockCodelist):
        executor.submit(downloadFile,elem[0])

    session.close()
    sys.exit()