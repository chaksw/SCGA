import xlwings as xw
import pandas as pd
import re
import os

SCGAs = []

def read_plan(testPlanSheet, rows):
    curRow = 8
    modules = []
    
    level_total_coverage = {
        'precentCoverageMCDC': 0,
        'precentCoverageAnalysis': 0,
        'totalCoverage': 0,
    }
    module = {
        'name': None,
        'process': None,
        'functions': []
    }
    while curRow <= rows + 1:
        range_ = f"{'A' + str(curRow)}:{'U' + str(curRow)}"
        info = testPlanSheet.range(range_).options(transpose=True).value
        print(f'{curRow}: {info[1]} -> {info[2]}')
        # collect level total coverage
        if info[1] is None:
            if info[0] == 'Level Total':
                level_total_coverage['precentCoverageMCDC'] = info[7]
                level_total_coverage['precentCoverageAnalysis'] = info[8]
                level_total_coverage['totalCoverage'] = info[9]
            else:
                continue
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
        if module['name'] != info[1]:
            if module['name'] is not None:
                modules.append(module)
            module = {
                'name': None,
                'functions': []
            }
            module['process'] = info[0]
            module['name'] = info[1]

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
        module['functions'].append(function)
        
        curRow = curRow + 1
    return modules, level_total_coverage
        

def read_exceptions(testExceptionSheet, rows):
    curRow = 7
    modules = []

    module = {
        'name': None,
        'functions': []
    }
    function = {
        'name': None,
        'note': None,
        'uncoverage': []
    }
    total = 0
    while curRow <= rows + 1:
        range_ = f"{'A' + str(curRow)}:{'M' + str(curRow)}"
        info = testExceptionSheet.range(range_).options(transpose=True).value
        print(f'{curRow}: {info[1]} -> {info[2]}')
        if function['name'] != info[2]:
            if function['name'] is not None:
                module['functions'].append(function)
            function = {
                'name': None,
                'note': None,
                'uncoverages': []
            }
            function['name'] = info[2]
        if module['name'] != info[1]:
            if module['name'] is not None:
                modules.append(module)
            module = {
                'name': None,
                'functions': []
            }
            module['name'] = info[1]
        
        uncoverage = {
            'uncoveredSWLine': [],
            'uncoveredinstrumentedSWLine': [],
            'requirementID': [],
            'analyst': None,
            'class': None,
            'analysisSummary': None,
            'correctActionSummary': None,
            'issue': None,
            'applicable': {}
        }
        applicable = {
            'PAR_SCR': None,
            'Comments': None
        }
        function['note'] = info[0]
        # uncovered software line
        uncoverage['uncoveredSWLine'] = info[3]
        # uncovered software code
        uncoverage['uncoveredinstrumentedSWLine'] = info[4]
        # requirements
        if info[5] is not None:
            uncoverage['requirementID'] = str(info[5]).split('\n')
        uncoverage['analyst'] = info[6]
        uncoverage['class'] = info[7]
        uncoverage['correctActionSummary'] = info[9]
        uncoverage['issue'] = info[10]
        applicable['PAR_SCR'] = info[11]
        applicable['Comments'] = info[12]
        uncoverage['applicable'] = applicable
        function['uncoverages'].append(uncoverage)
        total = total + 1
        curRow = curRow + 1
    # print(f'total rows: {total}')
    return modules


def read_SCGA(app, scga_path):
    SCGA = {
        'sheetName': os.path.basename(scga_path),
        'baseLine': str(os.path.basename(scga_path)).split('_SCGA')[0],
        'levelATest': {},
        'levelBTest': {},
        'levelCTest': {}
    }
    scga_sheets = app.books.open(scga_path)
    sheet_name_list = [sheet.name for sheet in scga_sheets.sheets]
    for currentSheet in scga_sheets.sheets:
        if 'Level' in currentSheet.name:
            if 'Plan' in currentSheet.name:
                test_plan = {
                    'sheetName': None,
                    'modules': [],
                    'lvTotalCoverage': {}
                }
                # continue
                rows = len(pd.read_excel(scga_path, currentSheet.name))
                print(f"Total functions of {currentSheet} is: {rows - 7}")
                if rows - 7 != 0:
                    test_plan['sheetName'] = currentSheet.name
                    test_plan['level'] = str(currentSheet.name).split(' ')[1]
                    test_plan['modules'], test_plan['lvTotalCoverage'] = read_plan(currentSheet, rows)
                    if test_plan['level'] == 'A':
                        SCGA['levelATest']['testPlan'] = test_plan
                    elif test_plan['level'] == 'B':
                        SCGA['levelBTest']['testPlan'] = test_plan
                    elif test_plan['level'] == 'C':
                        SCGA['levelCTest']['testPlan'] = test_plan
            elif 'Exceptions' in currentSheet.name:
                test_exception = {
                    'sheetName': None,
                    'level': None,
                    'modules': [],
                }
                rows = len(pd.read_excel(scga_path, currentSheet.name))
                print(f"Total uncovered situation of {currentSheet.name} is: {rows - 5}")
                if rows - 5 != 0:
                    test_exception['sheetName'] = currentSheet.name
                    test_exception['level'] = str(currentSheet.name).split(' ')[1]
                    test_exception['modules'] = read_exceptions(currentSheet, rows)
                    if test_exception['level'] == 'A':
                        SCGA['levelATest']['testException'] = test_plan
                    elif test_exception['level'] == 'B':
                        SCGA['levelBTest']['testException'] = test_plan
                    elif test_exception['level'] == 'C':
                        SCGA['levelCTest']['testException'] = test_plan
    return SCGA
    



                

def output_as_buffer():
    pass

def main():
    try:
        excelApp = xw.App(visible=False, add_book=False)
        read_SCGA(excelApp, r'C:\Users\H471967\Documents\4_SelfDev\SCGA\testExcel\EDSGGF_GS_G9CM_00_003_SCGA_1.xlsm')
    except Exception:
         print(Exception())
    finally:
        excelApp.quit()

if __name__ == '__main__':
    main()