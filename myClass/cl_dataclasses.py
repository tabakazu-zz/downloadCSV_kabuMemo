import dataclasses
from myClass.cl_myRE import MyRE
import datetime


@dataclasses.dataclass
class ItemData:
    """
    AmazonのitemData
    """
    name: str
    url: str
    strPrice: str
    strRate: str
    price: int = dataclasses.field ( init=False )
    sendfee: str = dataclasses.field ( init=False )
    rateCount: int = dataclasses.field ( init=False )
    ratePeople: int = dataclasses.field ( init=False )
    quantity: str = dataclasses.field ( init=False )
    unit: str = dataclasses.field ( init=False )

    def __post_init__(self):
        myRE = MyRE ()

        myRE.set_Pattern ( r'(.*)?円' )
        self.price = myRE.Search ( self.strPrice, 1 )

        myRE.set_Pattern ( r'送料(.*)' )
        ans = myRE.Search ( self.strPrice, 1 ).strip ().replace ( '円', '' )
        self.sendfee = 0 if ans == '無料' else ans

        myRE.set_Pattern ( r'(\d.*)\((.*)件' )
        self.rateCount = myRE.Search ( self.strRate, 1 )
        self.ratePeople = myRE.Search ( self.strRate, 2 )

        myRE.set_Pattern ( r'(\d*)(g|kg)' )
        self.quantity = myRE.Search ( self.name, 1 )
        self.unit = myRE.Search ( self.name, 2 )


@dataclasses.dataclass
class Data_C_Aachivement:
    """
    symbol:株価コード
    fiscal_term:決算期
    a_Date：発表日
    sales:売上高
    ordinary_incom：経常益
    net_income：最終益
    EPS：１株益
    dividends_per_share：１株配

    """
    Symbol: str
    fiscal_term: datetime.datetime
    a_Date: datetime.datetime
    sales: int
    ordinary_incom: int
    net_income: int
    EPS: int
    dividends_per_share: int


@dataclasses.dataclass
class data_stockPrice:
    """
    symbol:銘柄コード
    Date:取得日時
    Open:始値
    Close:終値
    High:高値
    Low:安値
    Volume:出来高
    AdjClose:調整終値
    """

    Symbol: str=dataclasses.field ( init=False )
    Date: datetime.datetime=dataclasses.field ( init=False )
    Open: int=dataclasses.field ( init=False )
    Close: int=dataclasses.field ( init=False )
    High: int=dataclasses.field ( init=False )
    Low: int=dataclasses.field ( init=False )
    Volume: int=dataclasses.field ( init=False )
    AdjClose: int=dataclasses.field ( init=False )


@dataclasses.dataclass
class data_Sinyou:
    """
    Symbol:銘柄コード
    Date:日時
    msb:margin selling balance->信用売り残
    mbb:margin buying balance->信用買い残
    m_rate:倍率
    """
    Symbol: str
    Date: datetime.datetime
    msb: float
    mbb: float
    m_rate: float

    def __post_init__(self):
        if self.m_rate=="-":
            self.m_rate=0
@dataclasses.dataclass
class data_dayBefore:
    """
    取得字価格、前日比、前日比（％）のdataclass
    symbol:銘柄コード
    Date:日付
    Price:当日価格
    rate:前日比
    rate_P:前日比（％）
    """
    Symbol:str
    Date:datetime.datetime
    Price:int
    rate:float
    rate_P:float
@dataclasses.dataclass
class data_cCompany:
    """
    比較会社のdataClqss
    symbol:銘柄コード
    unit:単位
    c_Company:比較会社
    """
    Symbol:str
    Unit:int
    c_Company:str


