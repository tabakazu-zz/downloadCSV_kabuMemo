import configparser
import logging.config
import pathlib
from logging import Formatter, handlers, StreamHandler, getLogger, DEBUG

def root_logger():
    #myclass内にlogging.confがある場合
    confPath='./logging.conf'
    p=pathlib.Path(confPath)
    if p.exists():
        logging.config.fileConfig('./logging.conf')
        logger=getLogger(__name__)
        return logger
    else:
        # root loggerを取得
        logger = getLogger ()

        # formatterを作成
        formatter = Formatter ( '%(asctime)s %(name)s %(funcName)s [%(levelname)s]: %(message)s' )

        # handlerを作成しフォーマッターを設定
        handler = StreamHandler ()
        handler.setFormatter ( formatter )

        # loggerにhandlerを設定、イベント捕捉のためのレベルを設定
        logger.addHandler ( handler )
        # log levelを設定
        logger.setLevel ( DEBUG )

        return logger

def chkFileExists(chkPath):
    p=pathlib.Path(chkPath)
    if p.exists():
        return True
    else:
        return False
