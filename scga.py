import xlwings as xw
import pandas as pd
import os
import traceback
import json
import pickle
import datetime

def output_log(str_):
    # print(str_)
    print(str_, file=scga_log_f)


def read_plan(testPlanSheet, rows):
    modules = []
    modules_name_list = []
    functions_name_list = []
    total_function = 0
    level_total_coverage = {
        'precentCoverageMCDC': 0,
        'precentCoverageAnalysis': 0,
        'totalCoverage': 0,
    }
    module = {
        'moduleName': None,
        'process': None,
        'functions': []
    }
    for curRow in range(7, rows + 2):
        range_ = f"{f'A{curRow}'}:{f'U{curRow}'}"
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
            'functionName': None,
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
        if module['moduleName'] != info[1]:
            
            if module['moduleName'] is not None and module['moduleName'] not in modules_name_list:
                modules_name_list.append(module['moduleName'])
                modules.append(module)
            module = {
                'moduleName': None,
                'functions': []
            }
            module['process'] = info[0]
            module['moduleName'] = info[1]
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
        function['functionName'] = info[2]
        function['analyst'] = info[4]
        function['site'] = info[5]
        # strfy datetime
        if isinstance(info[6], datetime.datetime):
            function['startDate'] = info[6].strftime("%Y-%m-%d")
        else:
            function['startDate'] = info[6]
        function['coverage'] = coverage
        function['moduleStrucData'] = module_structure_data
        function['oversight'] = info[17]
        function['defectClassification'] = defect_classification
        
        # see if info a new module line
        if info[1] not in modules_name_list or len(modules) == 0:
            module = {
                'moduleName': None,
                'functions': []
            }
            module['process'] = info[0]
            module['moduleName'] = info[1]
            module['functions'].append(function)
            functions_name_list.append(function['functionName'])
            total_function = total_function + 1
            modules.append(module)
            modules_name_list.append(module['moduleName'])
        # in case module already exist, add function to corresponding module
        else: 
            for index, moduleName in enumerate(modules_name_list):
                if moduleName == str(module['moduleName']):
                    (modules[index])['functions'].append(function)
                    functions_name_list.append(function['functionName'])
                    total_function = total_function + 1

    # write into log file
    output_log(f"Total functions of {testPlanSheet.name} is: {total_function}")
    output_log(f"total functions shows as below ({len(functions_name_list)}):")
    output_log(functions_name_list)
    output_log(f"total module shows as below ({len(modules_name_list)}):")
    output_log(modules_name_list)
        
    return modules, level_total_coverage, functions_name_list


def read_exceptions(testExceptionSheet, rows):
    uncovered_modules = []
    uncovered_modules_name_list = []
    uncovered_functions_name_list = []
    uncovered_module = {
        'moduleName': None,
        'functions': []
    }
    uncovered_function = {
        'functionName': None,
        'note': None,
        'uncoverage': []
    }
    total_uncoverage = 0
    for curRow in range(6, rows + 2):
        range_ = f"{f'A{curRow}'}:{f'M{curRow}'}"
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
        uncovered_function['note'] = info[0]
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
        if info[2] not in uncovered_functions_name_list or len(uncovered_functions_name_list) == 0:
            uncovered_function = {
                'functionName': None,
                'note': None,
                'uncoverages': [],
                'uncoverageCount': 0
            }
            uncovered_function['note'] = info[0]
            uncovered_function['functionName'] = info[2]
            uncovered_function['uncoverages'].append(uncoverage)
            uncovered_function['uncoverageCount'] = uncovered_function['uncoverageCount'] + 1
            total_uncoverage = total_uncoverage + 1
            uncovered_functions_name_list.append(uncovered_function['functionName'])
            # see if info a new module line
            if info[1] not in uncovered_modules_name_list or len(uncovered_modules) == 0:
                uncovered_module = {
                    'moduleName': None,
                    'functions': []
                }
                uncovered_module['process'] = info[0]
                uncovered_module['moduleName'] = info[1]
                uncovered_module['functions'].append(uncovered_function)
                uncovered_modules.append(uncovered_module)
                uncovered_modules_name_list.append(uncovered_module['moduleName'])
            # in case module already exist, add function to corresponding module
            else: 
                for index, moduleName in enumerate(uncovered_modules_name_list):
                    if moduleName == str(uncovered_module['moduleName']):
                        (uncovered_modules[index])['functions'].append(uncovered_function)
        else: # in case function already exist, add uncoverage information to corresponding function in corresponding module
            for i, moduleName in enumerate(uncovered_modules_name_list):
                if moduleName == info[1]:
                    for j, uncovered_function in enumerate((uncovered_modules[i])['functions']):
                        if info[2] == uncovered_function['functionName']:
                            (uncovered_modules[i])['functions'][j]['uncoverages'].append(uncoverage)
                            (uncovered_modules[i])['functions'][j]['uncoverageCount'] = (uncovered_modules[i])['functions'][j]['uncoverageCount'] + 1
                            total_uncoverage = total_uncoverage + 1
    # write into log file
    output_log(f"Total uncovered situation of {testExceptionSheet.name} is: {total_uncoverage}")
    output_log(f"total functions shows as below ({len(uncovered_functions_name_list)}):")
    output_log(uncovered_functions_name_list)
    output_log(f"total module shows as below ({len(uncovered_modules_name_list)}):")
    output_log(uncovered_modules_name_list)
    
    return uncovered_modules


def read_SCGA(app, scga_path):
    SCGA = {
        'SCGAName': os.path.basename(scga_path),
        'baseLine': str(os.path.basename(scga_path)).split('_SCGA')[0],
        'levelATest': {},
        'levelBTest': {},
        'levelCTest': {}
    }
    scga_function_list = {
        'baseLine': str(os.path.basename(scga_path)).split('_SCGA')[0],
        'levelAFunctions': [],
        'levelBFunctions': [],
        'levelCFunctions': []
    }
    scga_sheets = app.books.open(scga_path)
    sheet_name_list = [sheet.name for sheet in scga_sheets.sheets]
    for currentSheet in scga_sheets.sheets:
        if 'Level' in currentSheet.name:
            # point to file end
            scga_log_f.seek(0, 2)
            output_log(f'='*60)
            output_log(f'extration of {currentSheet.name}')
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
                    test_plan['modules'], test_plan['lvTotalCoverage'], function_list = read_plan(currentSheet, rows)
                    if test_plan['level'] == 'A':
                        SCGA['levelATest']['testPlan'] = test_plan
                        scga_function_list['levelAFunctions'] = function_list
                    elif test_plan['level'] == 'B':
                        SCGA['levelBTest']['testPlan'] = test_plan
                        scga_function_list['levelBFunctions'] = function_list
                    elif test_plan['level'] == 'C':
                        SCGA['levelCTest']['testPlan'] = test_plan
                        scga_function_list['levelCFunctions'] = function_list
                else:
                    scga_log_f.seek(0, 2)
                    output_log(f'* SCGA Test Plan information not found in {currentSheet.name}')
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
                    scga_log_f.seek(0, 2)
                    output_log(f'* SCGA Test Execptions information not found in {currentSheet.name}')
    return SCGA, scga_function_list


def read_SCGAs(app, scga_root_path):
    SCGAs = []
    all_scga_function_list = []
    for root, dirs, files in os.walk(scga_root_path):
        for scga_f in files:
            # only handle 'SCGA' excel file, and ignore not 'xlsm' file and excel buffer file
            if scga_f.endswith('xlsm') and '~' not in str(scga_f) and 'SCGA' in str(scga_f):
                output_log(f'='*80)
                output_log(f"extracting {scga_f}...")
                # write down frist
                scga_log_f.flush()
                SCGA, scga_function_list= read_SCGA(app, os.path.join(root, scga_f))
                SCGAs.append(SCGA)
                
                all_scga_function_list.append(scga_function_list)
                # point to file end
                scga_log_f.seek(0, 2)
                output_log(f'='*60)
                output_log(f'extraction done !')
                output_log(f'='*80)
                print()
        json.dump(SCGAs, scga_json, indent=4, default=str)
        pickle.dump(SCGAs, scga_pickle, protocol=pickle.HIGHEST_PROTOCOL)
    return SCGAs, all_scga_function_list

def generate_alphabet_list(n):
    if n < 1 or n > 26:
        raise ValueError("The number must be between 1 and 26 inclusive.")
    return [chr(i) for i in range(65, 65 + n)]


def output_all_functions_as_sheet(rootPath, scgaList):
    excelApp = xw.App(visible=False, add_book=False)
    wb = excelApp.books.add()
    ws = wb.sheets[0]
    ws.name = 'SCGA Fcuntion List'
    column_range = generate_alphabet_list(len(scgaList))
    for idx, value in enumerate(scgaList):
        start_pos = f'{column_range[idx]}2'
        ws.range(f'{column_range[idx]}1').value = value['baseLine']
        ws.range(start_pos).options(transpose=True).value = value['levelAFunctions']
        
    wb.save(os.path.join(rootPath, 'all_functions.xlsm'))
    wb.close()
    excelApp.quit()

def output_as_db():
    pass

def read_db():
    pass

def search_function_in_list(scga_list, search_func):
    for funcIdx, item in enumerate(scga_list):
        if item.get('functionName') == search_func:
            return funcIdx, item
    return None

def search_function_in_nested_scga(scga_dict, search_func, path=None):
    if path is None:
        path = []
    if isinstance(scga_dict, dict):
        for key, value in scga_dict.items():
            cur_path = path + [key]
            if isinstance(value, dict):
                result = search_function_in_nested_scga(value, search_func, cur_path)
                if result is not None:
                    return result
            # find ['modules'] and ['functions] list
            elif isinstance(value, list) and (key == 'modules'):
                for modIdx, item in enumerate(value):
                    res = search_function_in_list(item.get('functions'), search_func)
                    if res: 
                        funcIdx, func = res
                        return func, cur_path, modIdx, funcIdx
    return None

def get_output_str(scga_dict, res):
    value, path, modIdx, funcIdx = res
    mods = scga_dict
    for p in path:
        mods = mods.get(p)
    mod = mods[modIdx]
    output_str =  f"\t* {scga_dict.get('SCGAName')} -> {mod.get('moduleName')}\n"
    return output_str

def search_func(pklFilePath, funcStr):
    # deserializer scga pickle file
    result = None
    output_str = None
    try:
        scga_pickle_path = os.path.join(pklFilePath + r'\scgas.pkl')
        with open(scga_pickle_path, 'rb') as scga_pkl:
            deserialized_scga_data = pickle.load(scga_pkl)
            if isinstance(deserialized_scga_data, list):
                result = []
                for index, scga_dict in enumerate(deserialized_scga_data):
                    res = search_function_in_nested_scga(scga_dict, funcStr)
                    if res:
                        if output_str is None:
                            output_str = get_output_str(scga_dict, res)
                        else:
                            output_str = output_str + get_output_str(scga_dict, res)
                        result.append(res)
            elif isinstance(deserialized_scga_data, dict):
                result = search_function_in_nested_scga(deserialized_scga_data, funcStr)
                if result:
                    output_str = get_output_str(scga_dict, res)
            print(f"Found function '{funcStr}' at path:\n {output_str}")
    except FileNotFoundError:
        print(f'The file {scga_pkl} does not exist, you may need to extract new SCGA data group first')
    except pickle.UnpicklingError:
        print(f"Error unpickling the file {scga_pkl}.")
        print(traceback.print_exc())
    except Exception as e:
         print(f"An unexpected error occurred: {e}")
         print(traceback.print_exc())

scga_log_f = None
scga_json = None
scga_pickle = None
def main():
    global scga_log_f, scga_json, scga_pickle
    print(f'='*80)
    selection = input(
        "Welcom to SCGA extration:\n" + \
        "\t1. Extract new SCGA data group\n" + \
        "\t2. Add new SCGA data group\n" + \
        "\t3. Search function from existing SCGA data group\n" + \
        "Choose your operation: ")
    print(f'='*80)
    global scga_log
    while not(int(selection) == 1 or int(selection) == 2 or int(selection) == 3):
        print("Wrong selection..")
        selection = input(
            "\t1. Extract new SCGA data group\n" + \
            "\t2. Add new SCGA data group\n" + \
            "\t3. Search function from existing SCGA data group\n" + \
            "Choose your operation: ")
    else:
        if int(selection) == 1 or int(selection) == 2:
            SCGAs = []
            rootPath = input("Please enter the root path: ")
            excelApp = xw.App(visible=False, add_book=False)
            while not os.path.isdir(rootPath):
                rootPath = input("Can not found this location, please enter the root path again: ")
            else:
                try:
                    scga_log_path = os.path.join(rootPath + r'\scga_log.txt')
                    scgas_json_path = os.path.join(rootPath + r'\scgas.json')
                    scga_pickle_path = os.path.join(rootPath + r'\scgas.pkl')
                    if int(selection) == 1:
                        scga_log_f = open(scga_log_path, 'w', encoding='UTF-8')
                        scga_json = open(scgas_json_path, 'w', encoding='UTF-8')
                        scga_pickle = open(scga_pickle_path, 'wb')
                    else:
                        scga_log_f = open(scga_log_path, 'a', encoding='UTF-8')
                        scgas_json_path = open(scgas_json_path, 'a', encoding='UTF-8')
                        scga_pickle = open(scga_pickle_path, 'ab')
                    SCGAs, all_scga_function_list = read_SCGAs(excelApp, rootPath)
                    output_all_functions_as_sheet(rootPath, all_scga_function_list)
                except Exception as err:
                    # print(repr(keyerr))
                    print(traceback.print_exc())
                finally:
                    excelApp.quit()
                    scga_log_f.close()
                    scga_json.close()
                    scga_pickle.close()
        elif int(selection) == 3:
            rootPath = input("Please enter the root path of pickle file: ")
            while not os.path.isdir(rootPath):
                rootPath = input("Can not found this location, please enter the root path again: ")
            else:
                func = input("Input the function name: ")
                search_func(rootPath, func)


if __name__ == '__main__':
    main()