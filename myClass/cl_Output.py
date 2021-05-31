from pprint import pprint
from dataclass_csv import DataclassWriter
import os
import csv
import pandas as pd

class dataOutput():
    def set_OutPutPath(self,csvPath):
        self.outPutPath=csvPath
    def printData(self):
        pprint(self.myData)

    def outPutCSV_DF(self,df,writeMode="a",header=True):
        """
        dataFrmaをcsvに書き出し
        :param writeMode: a=add,w=overwrite
        :param header: true=headerを追加、folase=header無し
        :param df: 書き込むdataframe
        :return:
        """
        if header:
            df.to_csv(self.outPutPath,mode=writeMode)
        else:
            df.to_csv(self.outPutPath,mode=writeMode,header=False)



    def outPutCSV_list(self,myData,writeMode="a"):
        """
        output csv
        :param outPutPath:
        :param writeMode: "a"=Add or "w"=overwrite default "a"
        :param myData: inputData(type:list)
        :return:
        """
        if isinstance(myData[0],list) :
            with open (self.outPutPath, writeMode ) as f:
                writer = csv.writer ( f )
                writer.writerows (myData)
        else:
            with open(self.outPutPath,writeMode) as f:
                writer=csv.writer(f)
                writer.writerow(myData)

    def outPutCSV_dataclassCSV(self,dataclass,writeMode,dataclasslist=[]):
        """
        DataClassWriterを使用してDataClassをcsv出力：need to install dataclass_csv->https://pypi.org/project/dataclass-csv/
        :param writeMode:
        :param dataclasslist:データ入力済みのデータクラスリスト
        :param dataclass:書き込むdataclass型
        :return:
        """
        if not isinstance(dataclasslist,list):
            eMsg="dataclassList is not List" \
                 "processing is interrupted"
            raise Exception(eMsg)
            return

        with open(self.outPutPath,writeMode) as f:
            w=DataclassWriter(f,dataclasslist,dataclass)
            w.write()
