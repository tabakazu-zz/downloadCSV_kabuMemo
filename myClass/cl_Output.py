from pprint import pprint
from dataclass_csv import DataclassWriter
class dataOutput():
    def setData(self,data):
        self.myData=data
    def printData(self):
        pprint(self.myData)
    def outPutCSV_dataclassCSV(self,outPutPath,writeMode,dataclasslist,dataclass):
        with open(outPutPath,writeMode) as f:
            w=DataclassWriter(f,dataclasslist,dataclass)
            w.write()
