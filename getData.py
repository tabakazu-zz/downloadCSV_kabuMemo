#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from myClass.cl_Parse import Mybs4
import pandas as pd
import numpy as np

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
        for table in tables:
            cell = ins_Soup.get_rowFromTable ( table, False )
            return cell

    def listToDict(keylist,valuelsit):
        ansdict=dict(zip(keylist,valuelist))
        return ansdict

    def convertDatetime(target):
        from datetime import datetime as dt
        ans=dt.fromisoformat(target)
        #ans=dt.strptime ( target,"%Y-%m-%dT%H:%M:%S.%f%z")
        return ans

    ins_Soup.set_html(res.text)
    con1=ins_Soup.selectCSS("#stockinfo_i1") #社名、前日比,
    #現在値
    n_Price=ins_Soup.selectCSS(".kabuka")
    n_Price=ins_Soup.getAttr(n_Price)
    print(n_Price)

    #前日比
    dayBefore=ins_Soup.selectCSS(".si_i1_dl1")
    dayBefore=ins_Soup.selectCSSfromElem(dayBefore,"span")
    dayBefore=ins_Soup.getAttr(dayBefore)
    print(dayBefore)

    #取得日
    time=ins_Soup.find_all("time")
    s=convertDatetime(time[0]['datetime'])
    print(s.date())

    con2 = ins_Soup.selectCSS("#stockinfo_i2")#業績、単位株数
    con3 = ins_Soup.selectCSS("#stockinfo_i3")#PER,PBR,利回り,信用倍率、時価総額
    print(con1)

    ans=ins_Soup.selectCSSfromElem(con1,"dd")
    #print(ans)

    #per,pbr,利回り,信用倍率
    cell=getCell(con3)
    keylist=cell[0]
    valuelist=cell[1]
    perdict=listToDict(keylist,valuelist)
    perdict[cell[2][0]]=cell[2][1]
    perdict["stockCode"]=code
    #print(perdict)

    #チャート画像
    chr=ins_Soup.selectCSS("#chc_3_1>a")

    #個別株価
    kobetsu1=ins_Soup.selectCSS("#kobetsu_left")
    print(kobetsu1)
    kobetsu2=ins_Soup.selectCSS("#kobetsu_right")

    #株価
    kabuka=ins_Soup.selectCSSfromElem(con1[0],"span.kabuka")
    #print(kabuka)


    #単位
    unit=ins_Soup.selectCSSfromElem(con2[0],"dl dd")
    unit=unit[1].text



    #業績
    gyouseki=ins_Soup.selectCSSfromElem(kobetsu2[0],"div.gyouseki_block table")
    cell=getCell(gyouseki)
    print(cell)

    #PER,PBR,利回り、信用倍率,時価総額
    tables=ins_Soup.get_tablesfromElem(con3[0],False)
    cell=getCell(tables)
    #print(cell)

    #始値、高値、安値、終値
    tables=ins_Soup.get_tablesfromElem(kobetsu1[0])
    cell=getCell(tables)
    print(cell)

    #5日線、25日線、75日線、200日線
    tables=ins_Soup.get_tablesfromElem(kobetsu2[0])
    cell=getCell(tables)
    #print(cell)

    gaiyouHead=['コード','日付','会社名','始値','高値','安値','終値','出来高','売買代金','VWAP','約定回数','売買最低代金','単元株数','時価総額','発行済株式数']
    gyousekiHead=['コード',"発表日",'決算期','費目','結果']
    sinyouHead=['コード','日付','売り残','買い残','倍率']

if __name__=="__main__":
    getDataFromKabuTan(3990)