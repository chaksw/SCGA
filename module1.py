import xlwings as xw
import pandas as pd
import re
import os
import traceback

SCGAs = []

def read_plan(testPlanSheet, rows):
    modules = []
    modules_name_list = []
    total_function = 0
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
    for curRow in range(7, rows + 2):
        range_ = f"{'A' + str(curRow)}:{'U' + str(curRow)}"
        info = testPlanSheet.range(range_).options(transpose=True).value
        if info[1] is None:
            if info[0] == 'Level Total':
                level_total_coverage['precentCoverageMCDC'] = info[7]
                level_total_coverage['precentCoverageAnalysis'] = info[8]
                level_total_coverage['totalCoverage'] = info[9]
                continue
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
        # see if info a new module line
        if module['name'] != info[1]:
            
            if module['name'] is not None and module['name'] not in modules_name_list:
                modules_name_list.append(module['name'])
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
        
        # see if info a new module line
        if info[1] not in modules_name_list or len(modules) == 0:
            module = {
                'name': None,
                'functions': []
            }
            module['process'] = info[0]
            module['name'] = info[1]
            module['functions'].append(function)
            total_function = total_function + 1
            modules.append(module)
            modules_name_list.append(module['name'])
        # in case module already exist, add function to corresponding module
        else: 
            for index, moduleName in enumerate(modules_name_list):
                if moduleName == str(module['name']):
                    (modules[index])['functions'].append(function)
                    total_function = total_function + 1

    
    print(f"Total functions of {testPlanSheet.name} is: {total_function}")
    print(f"total module shows as below ({len(modules_name_list)}): ")
    print(modules_name_list)
    # write into log file
    with open(scga_log, 'a', encoding='UTF-8') as f:
        print(f"Total functions of {testPlanSheet.name} is: {total_function}", file=f)
        print(f"total module shows as below ({len(modules_name_list)}): ", file=f)
        print(modules_name_list, file=f)
    return modules, level_total_coverage
        

def read_exceptions(testExceptionSheet, rows):
    modules = []
    modules_name_list = []
    functions_name_list = []
    module = {
        'name': None,
        'functions': []
    }
    function = {
        'name': None,
        'note': None,
        'uncoverage': []
    }
    total_uncoverage = 0
    for curRow in range(6, rows + 2):
        range_ = f"{'A' + str(curRow)}:{'M' + str(curRow)}"
        info = testExceptionSheet.range(range_).options(transpose=True).value
        if info[1] is None:
            continue
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
        # see if info has new function
        if info[2] not in functions_name_list or len(functions_name_list) == 0:
            function = {
                'name': None,
                'note': None,
                'uncoverages': []
            }
            function['note'] = info[0]
            function['name'] = info[2]
            function['uncoverages'].append(uncoverage)
            total_uncoverage = total_uncoverage + 1
            functions_name_list.append(function['name'])
            # see if info a new module line
            if info[1] not in modules_name_list or len(modules) == 0:
                module = {
                    'name': None,
                    'functions': []
                }
                module['process'] = info[0]
                module['name'] = info[1]
                module['functions'].append(function)
                modules.append(module)
                modules_name_list.append(module['name'])
            # in case module already exist, add function to corresponding module
            else: 
                for index, moduleName in enumerate(modules_name_list):
                    if moduleName == str(module['name']):
                        (modules[index])['functions'].append(function)
        else: # in case function already exist, add uncoverage information to corresponding function in corresponding module
            for i, moduleName in enumerate(modules_name_list):
                if moduleName == info[1]:
                    for j, function in enumerate((modules[i])['functions']):
                        if info[2] == function['name']:
                            (modules[i])['functions'][j]['uncoverages'].append(uncoverage)
                            total_uncoverage = total_uncoverage + 1
    print(f"Total uncovered situation of {testExceptionSheet.name} is: {total_uncoverage}")
    print(f"total functions shows as below ({len(functions_name_list)}): ")
    print(functions_name_list)
    print(f"total module shows as below ({len(modules_name_list)}): ")
    print(modules_name_list)
     # write into log file
    with open(scga_log, 'a', encoding='UTF-8') as f:
        print(f"Total uncovered situation of {testExceptionSheet.name} is: {total_uncoverage}", file=f)
        print(f"total functions shows as below ({len(functions_name_list)}): ", file=f)
        print(functions_name_list, file=f)
        print(f"total module shows as below ({len(modules_name_list)}): ", file=f)
        print(modules_name_list, file=f)
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
            print(f'='*60)
            print(f'extration of {currentSheet.name}')
            with open(scga_log, 'a', encoding='UTF-8') as f:
                # point to file end
                f.seek(0, 2)
                print(f'='*60, file=f)
                print(f'extration of {currentSheet.name}', file=f)
            if 'Plan' in currentSheet.name:
                test_plan = {
                    'sheetName': None,
                    'modules': [],
                    'lvTotalCoverage': {}
                }
                rows = len(pd.read_excel(scga_path, currentSheet.name))
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
                else:
                    with open(scga_log, 'a', encoding='UTF-8') as f:
                        # point to file end
                        f.seek(0, 2)
                        print(f'* SCGA information not found in {currentSheet.name}')
                        print(f'* SCGA information not found in {currentSheet.name}', file=f)
            elif 'Exceptions' in currentSheet.name:
                test_exception = {
                    'sheetName': None,
                    'level': None,
                    'modules': [],
                }
                rows = len(pd.read_excel(scga_path, currentSheet.name))
                if rows - 5 != 0:
                    test_exception['sheetName'] = currentSheet.name
                    test_exception['level'] = str(currentSheet.name).split(' ')[1]
                    test_exception['modules'] = read_exceptions(currentSheet, rows)
                    if test_exception['level'] == 'A':
                        SCGA['levelATest']['testException'] = test_exception
                    elif test_exception['level'] == 'B':
                        SCGA['levelBTest']['testException'] = test_exception
                    elif test_exception['level'] == 'C':
                        SCGA['levelCTest']['testException'] = test_exception
                else:
                    with open(scga_log, 'a', encoding='UTF-8') as f:
                        # point to file end
                        f.seek(0, 2)
                        print(f'* SCGA information not found in {currentSheet.name}')
                        print(f'* SCGA information not found in {currentSheet.name}', file=f)
    return SCGA

                

def output_as_db():
    pass

def read_db():
    pass

def search_func():
    pass

scga_log = None
def main():
    global scga_log
    rootPath = input("Please enter the root path: ")
    if os.path.isdir(rootPath):
        try:
            scga_log = os.path.join(rootPath + r'\scga_log.txt')
            excelApp = xw.App(visible=False, add_book=False)
            with open(scga_log, 'w', encoding='UTF-8') as f:
                for root, dirs, files in os.walk(rootPath):
                    for scga_f in files:
                        # ignore not 'xlsm' file and excel buffer file
                        if scga_f.endswith('xlsm') and '~' not in str(scga_f):
                            print(f'='*80)
                            print(f"extracting {scga_f}...")
                            print(f'='*80, file=f)
                            print(f"extracting {scga_f}...", file=f)
                            # write down frist
                            f.flush()
                            SCGA = read_SCGA(excelApp, os.path.join(root, scga_f))
                            SCGAs.append(SCGA)
                            # point to file end
                            f.seek(0, 2)
                            print(f'='*60)
                            print(f'extraction done !')
                            print(f'='*80)
                            print(f'='*60, file=f)
                            print(f'extraction done !', file=f)
                            print(f'='*80, file=f)
                            print('', file=f)
        except BaseException as err:
            # print(repr(keyerr))
            print(traceback.print_exc())
        finally:
            excelApp.quit()

if __name__ == '__main__':
    main()