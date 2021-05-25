from bs4 import BeautifulSoup
import requests
import lxml


class Mybs4 ():
    # def __init__(self,html):
    # self.soup = BeautifulSoup ( html, "html.parser" )
    def setURL(self, target_url):
        res = requests.get ( target_url )
        try:
            self.soup = BeautifulSoup ( res.text, 'lxml' )
        except:
            self.soup = BeautifulSoup ( res.text, 'html5lib' )

    def set_html(self, html):
        self.soup = BeautifulSoup ( html, "html.parser" )

    def find_all(self, keyword):
        answers = self.soup.findAll ( keyword )
        ansCount = len ( answers )
        if ansCount == 0:
            eMsg = "Not Found."
            raise Exception ( eMsg )
        return answers

    def find(self, keyword):
        answer = self.soup.find ( keyword )
        ansCount = len ( answer )
        if ansCount == 0:
            eMsg = "Not Found."
            raise Exception ( eMsg )
        return answer

    def selectCSS(self, CSS):
        self._selectedItems = [n for n in self.soup.select ( CSS )]
        return self._selectedItems

    def selectCSSfromElem(self, elem, CSS):
        if type ( elem ) == list:
            ans = []
            for e in elem:
                ans_e = [n for n in e.select ( CSS )]
                if len ( elem ) == 1:
                    ans = ans_e
                else:
                    ans.append ( ans_e )
        else:
            ans = [n for n in elem.select ( CSS )]

        return ans

    def getAttr(self, elem, t_attr="text"):
        ans = []
        if type ( elem ) is list:
            if t_attr == "text":
                for e in elem:
                    if type ( e ) is list:
                        self.getAttr(e,t_attr)
                    else:
                        ans_e = e.get_text ()
                    if len ( elem ) == 1:
                        ans = ans_e
                    else:
                        ans.append ( ans_e )
        return ans

    def select_text(self, elem, CSS):
        ans = elem.select ( CSS )
        if not ans is None:
            ans = ans.get_text ()
            return ans
        else:
            return 'None'

    def select_one(self, elem, CSS):
        """

        :param elem:soup
        :param CSS:CSS
        :return: selected css soupObject
        """
        try:
            ans = elem.select_one ( CSS )
        except AttributeError:
            return 'None'

    def select_one_text(self, elem, CSS):
        try:
            ans = elem.select_one ( CSS )
            if ans is not None:
                ans = ans.get_text ()
                return ans
            else:
                return 'None'
        except AttributeError:
            return 'None'

    def select_one_getAttribute(self, elem, CSS, attr):
        """

        :param elem:
        :param CSS:CSS
        :param attr:取得したい要素　href
        :return:
        """
        ans = elem.select_one ( CSS )
        if not ans is None:
            ans = ans.get ( attr )
            return ans
        else:
            return 'None'

    def get_tables(self, is_Talkable=True):
        tables = self.soup.findAll ( "table" )
        n_tables = len ( tables )
        if n_tables == 0:
            eMsg = "table not found."
            raise Exception ( eMsg )
        if is_Talkable:
            print ( f'{n_tables} table tags found' )
        return tables

    def get_tablesfromElem(self, elem, is_talkable=True):
        tables = elem.findAll ( "table" )
        n_tables = len ( tables )
        if n_tables == 0:
            eMsg = "table not found"
            raise Exception ( eMsg )
        if is_talkable:
            print ( f'{n_tables}table tags found' )
        return tables

    def get_rowFromTable(self, table, is_talkable=True):
        """
        テーブルタグからth,tdを抜き出してlistに追加
        :param table:
        :param is_talkable:
        :return:
        """
        rows = table.findAll ( "tr" )
        n_rows = len ( rows )
        if n_rows == 0:
            eMsg = "row not found"
            raise Exception ( eMsg )
        if is_talkable:
            print ( f'{n_rows}row tag found' )

        ans = []

        for row in rows:
            cellList = []
            for cell in row.findAll ( ["td", "th"] ):
                cellList.append ( cell.text )
            ans.append ( cellList )
        return ans
