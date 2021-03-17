from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlAlchemy.base_engine import BaseEngine
from sqlalchemy.types import DateTime

Base = declarative_base()
Base.metadata.bind=BaseEngine().engine

class table_Stock_Code(Base):
    """
    if use Datetime,need to write "from sqlalchemy.types import Datetime"
    """
    __tablename__="stockCode"
    id = Column('id',Integer, primary_key=True)
    created=Column('created',DateTime)
    codeNum=Column('codeNum',Integer)
    codeName=Column('codeName',String(128))
    stockSection=Column('stockSection',String(128))
    tiCode_33=Column('tiCode_33',Integer) #33業種コード
    tiSection_33=Column('tiSection_33',String(20)) #33業種区分
    tiCode_17=Column('tiCode_17',Integer) #17業種コード
    tiSection_17=Column('tiSection_17',String(20)) #17業種区分
    scaleCode=Column('scaleCode',Integer) #規模コード
    scaleSection=Column('scaleSection',String(20)) #規模区分


