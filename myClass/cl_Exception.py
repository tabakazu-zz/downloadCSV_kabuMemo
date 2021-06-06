import d_Common
class pythonTradeSystemError(Exception):
    #自作株システムの基底クラス
    def __init__(self,arg=""):
        self.arg=arg

class getDataError(pythonTradeSystemError):
    def __str__(self):
        return(
            f"{self.arg}でエラーが発生しました。"
        )
