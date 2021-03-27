def df_to_Sql():
    import pandas as pd
    from sqlalchemy import create_engine
    from sqlAlchemy.base_engine import BaseEngine
    from sqlAlchemy.models import table_Stock_Code
    """
    読み込んだExcelファイルをDBに追加
    """
    df=pd.read_excel('./data_j_1.xls',index_col=0)

    dialect = "mysql"
    driver = "pymysql"
    username = "stockUser"
    password = "jaundice-exit-paddle-genii"
    host = "192.168.1.240"
    port = "3306"
    database = "stock_db"
    charset_type = "utf8mb4"
    db_url = f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}?charset={charset_type}"
    engine=create_engine(db_url,echo=True)

    df.to_sql('stockCode_jp',con=engine,if_exists='append',index=False)
class Csv_to_Sql():
    from tqdm import tqdm

    def __init__(self):
        import logging.config
        self.targetlists = []
        logging.config.fileConfig('./logging.conf')
        self.logger = logging.getLogger()


    def set_Csvmodel_USStock_toList(self,targetPath):
        import pathlib
        import csv
        from sqlAlchemy.models import table_US_Stock_Price
        from sqlAlchemy.curd import cli_sql
        #targetPath="./testData/A.csv"

        self.logger.info(f'Process Start->{targetPath}')
        p_file=pathlib.Path(targetPath)
        csvTitle=str(p_file.stem)
        targetlist=[]

        #session作成
        mysql = cli_sql()
        session = mysql.get_session()

        with open(targetPath,'r') as f:
            reader=csv.reader(f)
            header=next(reader)

            for row in reader:
                targetTable=table_US_Stock_Price(
                    symbol=csvTitle,
                    date=row[0],

                    high=row[1],
                    low=row[2],
                    open=row[3],
                    close=row[4],
                    volume=row[5],
                    adj_Close=row[6]
                )
                targetlist.append(targetTable)
        try:
            session.bulk_save_objects(targetlist)
            session.flush()
            session.commit()
            self.logger.info(f'commit successed')
        except Exception as e:
            eMes = f'type:{str(type(e))}\nargs:{str(e.args)}\n{str(e)}'
            self.logger.error(eMes)
            session.rollback()
        finally:
            session.close()


    def set_Csvmodel_JPStock_toList(self,targetPath):
        import pathlib
        import csv
        from sqlAlchemy.models import table_JP_Stock_Price
        from sqlAlchemy.curd import cli_sql
        import re
        #targetPath="./testData/A.csv"

        self.logger.info(f'Process Start->{targetPath}')
        p_file=pathlib.Path(targetPath)
        csvTitle=str(p_file.stem)
        pattern = re.compile(r'(\d*)_\d*')
        code=pattern.match(csvTitle)
        codeNum=code.group(1)

        targetlist=[]

        #session作成
        mysql = cli_sql()
        session = mysql.get_session()

        with open(targetPath,'r') as f:
            reader=csv.reader(f)
            header=next(reader)

            for i,row in enumerate(reader):
                if i>0:
                    targetTable=table_JP_Stock_Price(
                        symbol=codeNum,
                        date=row[0],
                        high=row[2],
                        low=row[3],
                        open=row[1],
                        close=row[4],
                        volume=row[5],
                        adj_Close=row[6]
                    )
                    targetlist.append(targetTable)
        try:
            session.bulk_save_objects(targetlist)
            session.flush()
            session.commit()
            self.logger.info(f'commit successed')
            return True
        except Exception as e:
            eMes = f'type:{str(type(e))}\nargs:{str(e.args)}\n{str(e)}'
            self.logger.error(eMes)
            session.rollback()
            return False
        finally:
            session.close()


if __name__ == '__main__':
    import pathlib
    from tqdm import tqdm
    from pprint import pprint
    #csv_to_Sql()
    from sqlAlchemy.models import table_US_Stock_Price
    from sqlAlchemy.curd import cli_sql
    from sqlalchemy import func
    import shutil


    #df_to_Sql()

    p_Fol=pathlib.Path(r'Y:\$Stock\JP_Stock_Csv')
    pathlist=[p for p in p_Fol.glob('*.csv')]

    cl_csvToSql=Csv_to_Sql()


    for elem in tqdm(pathlist):
        p_file = pathlib.Path(elem)
        csvTitle = str(p_file.stem)
        pDir=str(p_file.parent)
        dstFolder_Success=r'{}\Arcive'.format(pDir)
        dstFolder_Failed=r'{}\failed'.format(pDir)
        #  filtered = session.query(table_US_Stock_Price) \
        #              .filter(table_US_Stock_Price.symbol == csvTitle) \
        #              .first()
        # print(filtered)
        # filtered_count = (session.query(table_US_Stock_Price)
        #                   .filter(table_US_Stock_Price.symbol == csvTitle)
        #                   .count())
        if cl_csvToSql.set_Csvmodel_JPStock_toList(elem):
            shutil.move(elem,dstFolder_Success)
        else:
            shutil.move(elem,dstFolder_Failed)

