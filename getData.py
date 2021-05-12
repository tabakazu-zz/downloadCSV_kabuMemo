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

    ins_Soup.set_html(res.text)
    con1=ins_Soup.selectCSS("#stockinfo_i1")
    con2 = ins_Soup.selectCSS("#stockinfo_i2")
    con3 = ins_Soup.selectCSS("#stockinfo_i3")
    #チャート画像
    chr=ins_Soup.selectCSS("#chc_3_1>a")
    #個別株価
    kobetsu1=ins_Soup.selectCSS("#kobetsu_left")
    kobetsu2=ins_Soup.selectCSS("#kobetsu_right")
    #株価
    kabuka=ins_Soup.selectCSS("span.kabuka")

    print(kobetsu2)

if __name__=="__main__":
    getDataFromKabuTan(3990)