from pprint import pprint
from dataclass_csv import DataclassWriter
import os
import csv
import pathlib
import pandas as pd


class dataOutput ():
    def __init__(self):
        self.outPutPath = ''
        self.writeMode = ''
        self.source = ''

    def chkFileExists(self, tPath):
        p = pathlib.Path ( tPath )
        if p.exists ():
            return True
        else:
            return False

    def ListWriteCSV(self):
        """
        self.source->csv
        :return:
        """
        with open ( self.outPutPath, self.writeMode ) as f:
            writer = csv.writer ( f )
            if not type(self.source[0]) is list:
                writer.writerow(self.source)
            else:
                writer.writerows(self.source)
    def DictWriteCSV(self):
        if self.writeMode == 'w':
            with open ( self.outPutPath, self.writeMode, newline='' ) as f:
                writer = csv.DictWriter ( f, fieldnames=self.dictHeader )
                writer.writeheader ()
                for el in self.sourcelist:
                    writer.writerow ( el )
        elif self.writeMode == 'a':
            # 追記の場合
            # ファイル存在判定->存在しない場合はHeadr付きファイルを作成
            if not self.chkFileExists ( csvPath ):
                with open ( csvPath, 'w', newline='' ) as f:
                    writer = csv.DictWriter ( f, fieldnames=labels )
                    writer.writeheader ()

            with open ( csvPath, writeMode, newline='' ) as f:
                writer = csv.DictWriter ( f, fieldnames=labels )
                for source in sourceList:
                    writer.writerow ( source )

    def DClassWriteCSV(self):
        pass

    def outPutCSV_DF(self, df, writeMode="a", header=True):
        """
        dataFrmaをcsvに書き出し
        :param writeMode: a=add,w=overwrite
        :param header: true=headerを追加、folase=header無し
        :param df: 書き込むdataframe
        :return:
        """
        if header:
            df.to_csv ( self.outPutPath, mode=writeMode )
        else:
            df.to_csv ( self.outPutPath, mode=writeMode, header=False )

    def outPutCSV_Dict(self, source, csvPath, writeMode="a"):
        """
        dict->csv dictwritterを利用->sourceがdictなら[]で囲む
        :param source:書き込み対象辞書(dict or dictのlist）
        {A:1,B,1,...} or [{A:1,B:2...},{A:2,B:4....}]
        :writeMode:書き込み条件
        :csvPath:csvPath保存先、空欄の場合はself.csvPathを利用
        :return:
        """

        if type ( source ) is dict:
            labels = source.keys ()
            sourceList = [source]
        elif type ( source ) is list:
            labels = source[0].keys ()
            sourceList = source

        # 上書きの場合
        if writeMode == 'w':
            with open ( csvPath, writeMode, newline='' ) as f:
                writer = csv.DictWriter ( f, fieldnames=labels )
                writer.writeheader ()
                for source in sourceList:
                    writer.writerow ( source )

        elif writeMode == 'a':
            # 追記の場合
            # ファイル存在判定->存在しない場合はHeadr付きファイルを作成
            if not self.chkFileExists ( csvPath ):
                with open ( csvPath, 'w', newline='' ) as f:
                    writer = csv.DictWriter ( f, fieldnames=labels )
                    writer.writeheader ()

            with open ( csvPath, writeMode, newline='' ) as f:
                writer = csv.DictWriter ( f, fieldnames=labels )
                for source in sourceList:
                    writer.writerow ( source )

    def outPutCSV_list(self, myData, csvPath, writeMode="a+", header=True):
        """
        output csv
        :param outPutPath:
        :param writeMode: "a"=Add or "w"=overwrite default "a"
        :param myData: inputData(type:list)
        :param csvPath:出力先CSVPath
        :param header=True->sourceの先頭がHeaderのリストの場合->True Header読み込み、False->Header読み込みせず。
        :return:
        """
        # writemode=w->create New File
        # writemode=a->
        self.outPutPath = csvPath
        self.writeMode = writeMode

        # sourceにheaderが入っている場合
        if header:
            self.source = myData
        else:
            self.source = myData[1::]

        self.ListWriteCSV()

    def outPutCSV_dataclassCSV(self, dataclass, writeMode, dataclasslist=[]):
        """
        DataClassWriterを使用してDataClassをcsv出力：need to install dataclass_csv->https://pypi.org/project/dataclass-csv/
        :param writeMode:
        :param dataclasslist:データ入力済みのデータクラスリスト
        :param dataclass:書き込むdataclass型
        :return:
        """
        if not isinstance ( dataclasslist, list ):
            eMsg = "dataclassList is not List" \
                   "processing is interrupted"
            raise Exception ( eMsg )
            return

        with open ( self.outPutPath, writeMode ) as f:
            w = DataclassWriter ( f, dataclasslist, dataclass )
            w.write ()
