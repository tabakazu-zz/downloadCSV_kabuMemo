from base_engine import BaseEngine
from models import table_Stock_Code,Base

#databaseを作成
class Migration(object):
    def __init__(self):
        self.e = BaseEngine().engine

    def createTables(self):
        Base.metadata.create_all(self.e)

if __name__ == '__main__':
    Migration().createTables()
