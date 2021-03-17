import dataclasses
from myClass.cl_myRE import MyRE

@dataclasses.dataclass
class ItemData:
    name:str
    url:str
    strPrice:str
    strRate:str
    price:int=dataclasses.field(init=False)
    sendfee:str=dataclasses.field(init=False)
    rateCount:int=dataclasses.field(init=False)
    ratePeople:int=dataclasses.field(init=False)
    quantity:str=dataclasses.field(init=False)
    unit:str=dataclasses.field(init=False)


    def __post_init__(self):
        myRE=MyRE()

        myRE.set_Pattern ( r'(.*)?円' )
        self.price = myRE.Search ( self.strPrice, 1 )

        myRE.set_Pattern ( r'送料(.*)' )
        ans=myRE.Search ( self.strPrice, 1 ).strip().replace('円','')
        self.sendfee =0 if ans=='無料' else ans

        myRE.set_Pattern(r'(\d.*)\((.*)件')
        self.rateCount=myRE.Search(self.strRate,1)
        self.ratePeople=myRE.Search(self.strRate,2)

        myRE.set_Pattern(r'(\d*)(g|kg)')
        self.quantity=myRE.Search(self.name,1)
        self.unit=myRE.Search(self.name,2)










