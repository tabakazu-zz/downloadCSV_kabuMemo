import pandas as pd
from sqlalchemy import create_engine
from sqlAlchemy.models import table_Stock_Code
"""
読み込んだExcelファイルをDBに追加
"""
df=pd.read_excel('./data_j_1.xls',index_col=0)

engine=create_engine("sqlite:///stock.db")

df.to_sql('stockCode',con=engine,if_exists='append',index=False)