#TODO:data_j.xlsからデータを読み込んでstock.db->table_Stock_Codeに追加
import xlwings as xw
import xlwing.cl_xlwings as fun
from sqlAlchemy.curd import cli_sql
from sqlalchemy import text
from sqlAlchemy.models import table_Stock_Code

cli_sql=cli_sql()
session=cli_sql.get_session()

stockCodelist=session.query(table_Stock_Code.codeNum).\
    filter(table_Stock_Code.tiCode_17=="-").\
    all()

for elem in stockCodelist:
    print(elem[0])
