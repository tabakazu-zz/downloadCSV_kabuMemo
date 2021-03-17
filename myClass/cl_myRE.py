import re

class MyRE():
    def set_Pattern(self,pattern):
        self.myPattern = re.compile ( pattern )

    def Match(self,source,groupNum=0):
        #先頭のみ抽出
        m=re.match(self.myPattern,source)
        if m:
            return m.group(groupNum)
        else:
            return None

    def Search(self,source,groupNum=0):
        m=re.search(self.myPattern,source)
        if not m:
            return None
        else:
            return m.group(groupNum)

    def FindAll(self,source):
        m=re.findall(self.myPattern,source)
        if m:
            return m
        else:
            return []

    def Split(self,source):
        m=re.split(self.myPattern,source)
        return m

    def Sub(self,source,repalecWord):
        m=re.sub(self.myPattern,repalecWord,source)