import xlwings as xw
import pandas as pd
import re
import os


BaseLine = "EDSGGF_GS_GCOM_00_002"
SCGA = BaseLine + '_SCGA.xlsm'

def read_plan():
    pass

def read_exceptions():
    pass


def read_SCGA(app, scga_path):
    scga_sheets = app.books.open(scga_path)
    sheet_name_list = [sheet.name for sheet in scga_sheets.sheets]
    for currentSheet in scga_sheets.sheets:
        if 'Level A' in currentSheet.name:
            if 'Plan' in currentSheet.name:
                read_plan()
            elif 'Exceptions' in currentSheet.name:
                read_exceptions()


def main():
    excelApp = xw.App(visible=False, add_book=False)

