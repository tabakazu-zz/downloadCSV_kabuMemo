from bs4 import BeautifulSoup
import requests
import lxml
class Mybs4():
    #def __init__(self,html):
        #self.soup = BeautifulSoup ( html, "html.parser" )
    def setURL(self,target_url):
        res=requests.get(target_url)
        try:
            self.soup=BeautifulSoup(res.text,'lxml')
        except:
            self.soup=BeautifulSoup(res.text,'html5lib')

    def set_html(self,html):
        self.soup=BeautifulSoup(html,"html.parser")

    def selectCSS(self,CSS):
        self._selectedItems=[n for n in self.soup.select(CSS)]
        return self._selectedItems

    def select_text(self, elem, CSS):
        ans = elem.select( CSS )
        if not ans is None:
            ans=ans.get_text()
            return ans
        else:
            return 'None'

    def select_one_text(self,elem,CSS):
        try:
            ans=elem.select_one(CSS)
            if ans is not None:
                ans=ans.get_text()
                return ans
            else:
                return 'None'
        except AttributeError:
            return 'None'

    def select_one_getAttribute(self,elem,CSS,attr):
        ans=elem.select_one(CSS)
        if not ans is None:
            ans=ans.get(attr)
            return ans
        else:
            return 'None'