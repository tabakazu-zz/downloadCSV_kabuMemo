from pprint import pprint
from dataclass_csv import DataclassWriter
import os
import csv
import pandas as pd

class dataOutput():
    def printData(self):
        pprint(self.myData)

    def outPutCSV_DF(self,outPutPath,writeMode="a",header=true,df):
        if header:
            df.to_csv(outPutPath,mode=writeMode)
        else:
            df.to_csv(outPutPath,mode=writeMode,header=False)


    def outPutCSV_list(self,outPutPath,writeMode="a",myData):
        """
        output csv
        :param outPutPath:
        :param writeMode: "a"=Add or "w"=overwrite default "a"
        :param myData: inputData(type:list)
        :return:
        """
        if isinstance(myData[0],list) :
            with open ( outPutPath, writeMode ) as f:
                writer = csv.writer ( f )
                writer.writerows (myData)
        else:
            with open(outPutPath,writeMode) as f:
                writer=csv.writer(f)
                writer.writerow(myData)

    def outPutCSV_dataclassCSV(self,outPutPath,writeMode,dataclasslist,dataclass):
        with open(outPutPath,writeMode) as f:
            w=DataclassWriter(f,dataclasslist,dataclass)
            w.write()
