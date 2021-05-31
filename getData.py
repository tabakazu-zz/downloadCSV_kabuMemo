#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from myClass.cl_Parse import Mybs4
import pandas as pd
import numpy as np
import myClass.cl_dataclasses as dbClass
import myClass.cl_Output as output

def getDataFromKabuTan(code):
    url=f"https://kabutan.jp/stock/?code={code}"
    res=requests.get(url)
    ins_Soup=Mybs4()
    ins_SoupElem=Mybs4()

    def getCell(tables):
        """
        excecution get_rowFromTable
        :param tables:
        :return:
        """
        celllist=[]
        for table in tables:
            cell = ins_Soup.get_rowFromTable ( table, False )
            if len(tables)==1:
                celllist=cell
            else:
                celllist.append(cell)

        return celllist

    def listToDict(keylist,valuelsit):
        ansdict=dict(zip(keylist,valuelist))
        return ansdict

    def convertDatetime(target):
        from datetime import datetime as dt
        ans=dt.fromisoformat(target)
        #ans=dt.strptime ( target,"%Y-%m-%dT%H:%M:%S.%f%z")
        return ans

    ins_Soup.set_html(res.text)
    con1 = ins_Soup.selectCSS ( "#stockinfo_i1" )  # 社名、前日比,
    kobetsu1=ins_Soup.selectCSS("#kobetsu_left") #前日終値〜情報提供
    print(kobetsu1)


    #取得日
    time=ins_Soup.find_all("time")
    s=convertDatetime(time[0]['datetime'])
    date_get=s.date()

    # ————————————————————————————————————+
    # 四本足取得 SYMBOL,DATE,OPEN,Close,High,Low,Volume,AdjClose
    # ————————————————————————————————————+
    data_stockPrice=dbClass.data_stockPrice()
    data_stockPrice.Symbol=code
    data_stockPrice.Date=date_get

    def c_stockPrice(tlist):
        tValue=tlist[1]
        if tlist[0]=="始値":
            data_stockPrice.Open=int(tValue.replace(",",""))
        elif tlist[0]=="高値":
            data_stockPrice.High=int(tValue.replace(",",""))
        elif tlist[0]=="安値":
            data_stockPrice.Low=int(tValue.replace(",",""))
        elif tlist[0]=="終値":
            data_stockPrice.Close=int(tValue.replace(",",""))
            # 調整後終値->closeで代用
            data_stockPrice.AdjClose=data_stockPrice.Close

    # 始値、高値、安値、終値
    tables = ins_Soup.get_tablesfromElem ( kobetsu1[0] )
    cell = getCell ( tables )
    #print(cell)

    for elist in cell[0]:
        c_stockPrice(elist)

    #出来高
    data_stockPrice.Volume=cell[1][0]

    # ————————————————————————————————————+
    # 売買代金,VWAP,約定回数,売買最低代金,時価総額,\
    # 単元株数、時価総額、発行済株式数
    # ――――――――――――――――――――――――――――――――――――+


    # ————————————————————————————————————+
    # 信用取引:symbol date
    # ————————————————————————————————————+
    sinyouList=cell[3]
    del sinyouList[0]
    data_Sinyou=['']*len(sinyouList)

    for i,elem in enumerate(sinyouList):
        data_Sinyou[i]=dbClass.data_Sinyou
        data_Sinyou[i].Symbol=code
        data_Sinyou[i].Date=elem[0]
        data_Sinyou[i].msb=elem[1]
        data_Sinyou[i].mbb=elem[2]
        data_Sinyou[i].m_rate=elem[3]

    # ————————————————————————————————————+
    # Symbol,Date,Close,前日比,前日比(%)
    # ————————————————————————————————————+

    #現在値
    n_Price=ins_Soup.selectCSS(".kabuka")
    n_Price=ins_Soup.getAttr(n_Price)
    #print(n_Price) #->1,466円

    #前日比
    dayBefore=ins_Soup.selectCSS(".si_i1_dl1")
    dayBefore=ins_Soup.selectCSSfromElem(dayBefore,"span")
    dayBefore=ins_Soup.getAttr(dayBefore)
    #print(dayBefore)#->['-7','-0.48']


    data_dayBefore=dbClass.data_dayBefore
    data_dayBefore.Symbol=code
    data_dayBefore.Date=date_get
    data_dayBefore.Price=n_Price.replace("円","")
    data_dayBefore.rate=dayBefore[0]
    data_dayBefore.rate_P=dayBefore[1]

    #print(data_dayBefore)


    # ---------------------------------------------------------------------
    # PER,PBR,利回り、信用倍率
    # —————————————————————————
    con3 = ins_Soup.selectCSS ( "#stockinfo_i3" )  # PER,PBR,利回り,信用倍率、時価総額
    cell = getCell ( con3 )
    keylist = cell[0]
    valuelist = cell[1]
    perdict = listToDict ( keylist, valuelist )
    perdict[cell[2][0]] = cell[2][1]
    perdict["stockCode"] = code
    print(perdict)


    #チャート画像
    chr=ins_Soup.selectCSS("#chc_3_1>a")
    kobetsu2=ins_Soup.selectCSS("#kobetsu_right")


    # ---------------------------------------------------------------------
    # Symbol,単位、比較会社
    # —————————————————————————
    #単位
    con2 = ins_Soup.selectCSS("#stockinfo_i2")#業績、単位株数
    unit=ins_Soup.selectCSSfromElem(con2[0],"dl dd")
    unit=unit[1].text

    # 比較銘柄
    c_Company = ins_Soup.selectCSS ( ".si_i1_dl2" )
    c_Company = ins_Soup.selectCSSfromElem ( c_Company, "dd" )
    c_Company = ins_Soup.getAttr ( c_Company )
    c_Company=[elem.rstrip().replace(",","") for elem in c_Company]
    c_Company=",".join(c_Company)

    d_cCompany=dbClass.data_cCompany(Symbol=code,Unit=unit.replace("株",""),c_Company=c_Company)



    # ---------------------------------------------------------------------
    # 業績->
    # Symbol,決算期、売上高、経常益、最終駅、１株益、１株配、発表日
    # —————————————————————————

    #業績
    gyouseki=ins_Soup.selectCSSfromElem(kobetsu2[0],"div.gyouseki_block table")
    cell=getCell(gyouseki)
    print(cell)


    #PER,PBR,利回り、信用倍率,時価総額
    tables=ins_Soup.get_tablesfromElem(con3[0],False)
    cell=getCell(tables)
    #print(cell)

    #5日線、25日線、75日線、200日線
    tables=ins_Soup.get_tablesfromElem(kobetsu2[0])
    cell=getCell(tables)
    #print(cell)

    gaiyouHead=['コード','日付','会社名','始値','高値','安値','終値','出来高','売買代金','VWAP','約定回数','売買最低代金','単元株数','時価総額','発行済株式数']
    gyousekiHead=['コード',"発表日",'決算期','費目','結果']
    sinyouHead=['コード','日付','売り残','買い残','倍率']

    # ————————————————————————————————————+
    # csv出力
    # ――――――――――――――――――――――――――――――――――――+
    #四本足
    csvOutput=output.dataOutput()
    csvOutput.set_OutPutPath("./fourValue.csv")
    data_stockPrice=[data_stockPrice]
    csvOutput.outPutCSV_dataclassCSV(writeMode="w",dataclasslist=data_stockPrice,dataclass=dbClass.data_stockPrice)

    csvOutput.set_OutPutPath("./test.csv")
    d_cCompanys=[d_cCompany]
    #csvOutput.outPutCSV_dataclassCSV(writeMode="w",dataclasslist=d_cCompanys,dataclass=dbClass.data_cCompany)


if __name__=="__main__":
    getDataFromKabuTan(3990)