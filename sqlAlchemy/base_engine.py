from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#TODO:initでurlを設定している部分をうまく設定できるようにしたい。

class BaseEngine(object):
    def __init__(self):
        """
        dialect = "mysql"
        driver = "mysqldb"
        username = "root"
        password = "xxxxxxxx"
        host = "192.168.30.30"
        port = "3306"
        database = "sample_db"
        charset_type = "utf8"
        db_url = f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}?charset={charset_type}"
        """
        db_url = "sqlite:///./stock.db"
        self.engine = create_engine(db_url, echo=True)

class BaseSession ( BaseEngine ):
    def __init__(self):
        super ().__init__ ()
        Session = sessionmaker ( bind=self.engine )
        self.session = Session ()
