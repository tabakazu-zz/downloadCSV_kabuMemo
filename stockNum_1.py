def csv_to_Sql(target):
    import pandas as pd
    from sqlalchemy import create_engine
    from sqlAlchemy.models import table_Stock_Code
    """
    読み込んだExcelファイルをDBに追加
    """
    df=pd.read_excel('./data_j_1.xls',index_col=0)

    engine=create_engine("sqlite:///stock.db")

    df.to_sql('stockCode',con=engine,if_exists='append',index=False)
def from_Csv_to_Sql():
    import pathlib
    import csv
    from sqlAlchemy.models import table_US_Stock_Price
    from sqlAlchemy.curd import cli_sql
    targetPath="./testData/A.csv"

    p_file=pathlib.Path(targetPath)
    csvTitle=str(p_file.stem)
    mysql=cli_sql()
    session=mysql.get_session()
    targetlists=[]
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
                bulk_save_objects close=row[4],
                volume=row[5],
                adj_Close=row[6]
            )
            targetlists.append(targetTable)

    session.bulk_save_objects(targetlists)
    session.flush()

if __name__ == '__main__':
    from_Csv_to_Sql()
