from pprint import pprint
from dataclass_csv import DataclassWriter
import os
import csv
import pathlib
import pandas as pd

class dataOutput():
    def chkFileExists(self,tPath):
        p=pathlib.Path(tPath)
        if p.exists():
            return True
        else:
            return False
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

    def outPutCSV_Dict(self,source,csvPath,writeMode="a"):
        """
        dict->csv dictwritterを利用->sourceがdictなら[]で囲む
        :param source:書き込み対象辞書(dict or dictのlist）
        {A:1,B,1,...} or [{A:1,B:2...},{A:2,B:4....}]
        :writeMode:書き込み条件
        :csvPath:csvPath保存先、空欄の場合はself.csvPathを利用
        :return:
        """

        if type(source) is dict:
            labels=source.keys()
            sourceList=[source]
        elif type(source) is list:
            labels=source[0].keys()
            sourceList=source

        #上書きの場合
        if writeMode=='w':
            with open(csvPath,writeMode,newline='') as f:
                writer=csv.DictWriter(f,fieldnames=labels)
                writer.writeheader()
                for source in sourceList:
                    writer.writerow(source)

        elif writeMode=='a':
            #追記の場合
            #ファイル存在判定->存在しない場合はHeadr付きファイルを作成
            if not self.chkFileExists(csvPath):
                with open(csvPath,'w',newline='') as f:
                    writer=csv.DictWriter(f,fieldnames=labels)
                    writer.writeheader()

            with open(csvPath,writeMode,newline='') as f:
                writer=csv.DictWriter(f,fieldnames=labels)
                for source in sourceList:
                    writer.writerow(source)

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

