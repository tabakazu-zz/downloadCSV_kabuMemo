import xlwings as xw
def lastExcelRow(sheet,col):
    """
    指定したシートの最終セルを取得
    :param sheet:
    :param col:
    :return:
    """
    lwr_r_cell=sheet.cells.last_cell #lower right cell
    lwr_row=lwr_r_cell.row #row of the lower right cell
    lwr_cell=sheet.range((lwr_row,col)) # change to your specified column

    if lwr_cell.value is None:
        lwr_cell=lwr_cell.end('up')

    return  lwr_cell.row

def lastExcelColumn(sheet,row):
    """
    expandを使用:
    mode (str, default 'table') -- 'table' (=downとright)、 'down' 、 'right' のいずれか。
    :param sheet:xlwings_sheetObject
    :param row:
    :return:
    """


def lastExcelCell(sheet,col):
    """
    最終行のセルの値を取得
    :param sheet:
    :param col: int or alfarbet
    :return: value of lastCell
    """
    return sheet.range((lastExcelRow(sheet,col),col))