from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#initでurlを設定している部分をうまく設定できるようにしたい。
class BaseEngine(object):
    def __init__(self):
        dialect = "mysql"
        driver = "pymysql"
        username = "stockUser"
        password = "jaundice-exit-paddle-genii"
        host = "192.168.1.240"
        port = "3306"
        database = "stock_db"
        charset_type = "utf8"
        db_url = f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}?charset={charset_type}"

        # db_url = "sqlite:///Y:\$Stock\stock.db"
        self.engine = create_engine(db_url, echo=True)


class BaseSession ( BaseEngine ):
    def __init__(self):
        super ().__init__ ()
        Session = sessionmaker ( bind=self.engine )
        self.session = Session ()
