import xlwings as xw
import pandas as pd
import re
import os

SCGA = {
    'baseLine': '',
    'Load':  '',
    'lvA': {},
    'lvB': {},
    'lvC': {},
}

test_plan = []
test_exception = []
BaseLine = "EDSGGF_GS_GCOM_00_002"
SCGAxlsm = BaseLine + '_SCGA.xlsm'

def read_plan(testPlanSheet, rows):
    curRow = 8
    files = []
    baseLine = None
    process = None
    
    level_total_coverage = {
        'precentCoverageMCDC': 0,
        'precentCoverageAnalysis': 0,
        'totalCoverage': 0,
    }
    file_ = {
        'name': None,
        'functions': []
    }
    while curRow <= rows + 1:
        range_ = f"{'A' + str(curRow)}:{'U' + str(curRow)}"
        info = testPlanSheet.range(range_).options(transpose=True).value
        print(info)
        # collect level total coverage
        if info[1] is None:
            if info[0] == 'Level Total':
                level_total_coverage['precentCoverageMCDC'] = info[7]
                level_total_coverage['precentCoverageAnalysis'] = info[8]
                level_total_coverage['totalCoverage'] = info[9]
            else:
                continue
        if curRow == 8:
            baseLine = info[3]
            process = info[0]
        function = {
            'name': None,
            'analyst': None,
            'site': None,
            'startDate': None,
            'coverage': {},
            'moduleStrucData': {},
            'oversight': None,
            'defectClassification': {}
        }
        coverage = {
            'precentCoverageMCDC': 0,
            'precentCoverageAnalysis': 0,
            'totalCoverage': 0,
        }

        module_structure_data = {
            'covered': {},
            'total': {},
        }
        covered = {
            'branches': 0,
            'pairs': 0,
            'statement': 0
        }
        total = {
            'branches': 0,
            'pairs': 0,
            'statement': 0
        }

        defect_classification = {
            'tech': None,
            'nonTech': None,
            'process': None,
        }
        if file_['name'] != info[1]:
            if file_['name'] is not None:
                files.append(file_)
            file_ = {
                'name': None,
                'functions': []
            }
            file_['name'] = info[1]
        # oversight
        function['oversight'] = info[17]
        # defect classification
        defect_classification['tech'] = info[18]
        defect_classification['nonTech'] = info[19]
        defect_classification['process'] = info[20]
        # total module strcuture data
        total['branches'] = info[14]
        total['pairs'] = info[15]
        total['statement'] = info[16]
        # covered module strcuture data
        covered['branches'] = info[11]
        covered['pairs'] = info[12]
        covered['statement'] = info[13]
        # module strcuture data
        module_structure_data['total'] = total
        module_structure_data['covered'] = covered
        # coverage
        coverage['precentCoverageMCDC'] = info[7]
        coverage['precentCoverageAnalysis'] = info[8]
        coverage['totalCoverage'] = info[9]
        # function
        function['name'] = info[2]
        function['analyst'] = info[4]
        function['site'] = info[5]
        function['startDate'] = info[6]
        function['coverage'] = coverage
        function['moduleStrucData'] = module_structure_data
        function['oversight'] = info[17]
        function['defectClassification'] = defect_classification
        file_['functions'].append(function)
        
        curRow = curRow + 1
    return baseLine, process, files, level_total_coverage
        



def read_exceptions():
    pass


def read_SCGA(app, scga_path):
    test_plan = {
        'sheetName': None,
        'baseLine': None,
        'process': None,
        'level': None,
        'files': [],
        'lvTotalCoverage': {}
    }
    test_plan['baseLine'] = str(scga_path).split('\\')[-1].split('_SCGA')[0]
    test_exception = []
    scga_sheets = app.books.open(scga_path)
    sheet_name_list = [sheet.name for sheet in scga_sheets.sheets]
    for currentSheet in scga_sheets.sheets:
        if 'Level' in currentSheet.name:
            if 'Plan' in currentSheet.name:
                rows = len(pd.read_excel(scga_path, currentSheet.name))
                print(f"Total functions of {currentSheet} is: {rows - 7}")
                test_plan['sheetName'] = currentSheet.name
                test_plan['level'] = 'Level ' + str(currentSheet.name).split(' ')[1]
                test_plan['baseLine'], test_plan['process'], test_plan['files'], test_plan['lvTotalCoverage'] = read_plan(currentSheet, rows)
            elif 'Exceptions' in currentSheet.name:
                rows = len(pd.read_excel(scga_path, currentSheet.name))
                print(f"Total uncovered situation of {currentSheet} is: {rows - 5}")
                read_exceptions()

def output_as_buffer():
    pass

def main():
    try:
        excelApp = xw.App(visible=False, add_book=False)
        read_SCGA(excelApp, r'C:\Users\H471967\Documents\4_SelfDev\SCGA\testExcel\EDSGGF_GS_G9CM_00_003_SCGA_1.xlsm')
    except:
        pass
    finally:
        excelApp.quit()

if __name__ == '__main__':
    main()