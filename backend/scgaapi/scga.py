import xlwings as xw
import pandas as pd
import os
import traceback
import json
import pickle
import datetime
from tqdm import tqdm

NULL = ''
# scga class
INCOMPLETE_TESTS = 'INCOMPLETE_TESTS'
REQUIREMENTS_CODE_MISMATCH = 'REQUIREMENTS_CODE_MISMATCH'
DEACTIVATED_CODE = 'DEACTIVATED_CODE'
DEFENSIVE_CODE = 'DEFENSIVE_CODE'
TEST_ENVIRONMENT_LIMITATIONS = 'TEST_ENVIRONMENT_LIMITATIONS'
PREVIOUSLY_ANALYZED_SOFTWARE = 'PREVIOUSLY_ANALYZED_SOFTWARE'
OTHER = 'OTHER'
CHOICES_CLASS = (
    (NULL, ''),
    (INCOMPLETE_TESTS, "Incomplete Tests"),
    (REQUIREMENTS_CODE_MISMATCH, "Requirements-Code Mismatch"),
    (DEACTIVATED_CODE, "Deactivated Code"),
    (DEFENSIVE_CODE, "Defensive Code"),
    (TEST_ENVIRONMENT_LIMITATIONS, "Test Environment Limitations"),
    (PREVIOUSLY_ANALYZED_SOFTWARE, "Previously Analyzed Software"),
    (OTHER, "Other"),
)


def set_class(value):
    choice_map = {v: k for k, v in CHOICES_CLASS}
    class_choice = None
    if value in choice_map:
        class_choice = choice_map[value]
    else:
        class_choice = ''
    return class_choice


def output_log(str_=None):
    # print(str_)
    print(str_, file=scga_log_f)


def read_plan(test_plan_sheet, rows):
    """Read test plan inforamtions of scga sheet

    Args:
        test_plan_sheet (xlwings sheet): test plan sheet of a scga excel
        rows (int): row numbers of test plan sheet

    Raises:
        ValueError: None

    Returns:
        dict list -- module: dict list of all files involved in scga  
        dict -- level_total_coverage: coverage condition of scga 
        list -- functions_name_list: functions involed in scga
    """
    modules = []
    modules_name_list = []
    functions_name_list = []
    total_function = 0
    level_total_coverage = {
        'percent_coverage_MCDC': 0,
        'percent_coverage_Analysis': 0,
        'total_coverage': 0,
    }
    module = {
        'module_name': None,
        'process': None,
        'functions': []
    }
    for curRow in range(7, rows + 2):
        range_ = f"{f'A{curRow}'}:{f'U{curRow}'}"
        info = test_plan_sheet.range(range_).options(transpose=True).value
        if info[1] is None:
            if info[0] == 'Level Total':
                level_total_coverage['percent_coverage_MCDC'] = info[7]
                level_total_coverage['percent_coverage_Analysis'] = info[8]
                level_total_coverage['total_coverage'] = info[9]
                continue
            else:
                continue
        function = {
            'function_name': None,
            'analyst': None,
            'site': None,
            'start_date': None,
            'coverage': {},
            'covered': {},
            'total': {},
            # 'moduleStrucData': {},
            'oversight': None,
            'defect_classification': {}
        }
        coverage = {
            'percent_coverage_MCDC': 0,
            'percent_coverage_Analysis': 0,
            'total_coverage': 0,
        }
        # module_structure_data = {
        #     'covered': {},
        #     'total': {},
        # }
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
            'non_tech': None,
            'process': None,
        }
        # see if info a new module line
        if module['module_name'] != info[1]:

            if module['module_name'] is not None and module['module_name'] not in modules_name_list:
                modules_name_list.append(module['module_name'])
                modules.append(module)
            module = {
                'module_name': None,
                'functions': []
            }
            module['process'] = info[0]
            module['module_name'] = info[1]
        # oversight
        function['oversight'] = info[17]
        # defect _classification
        defect_classification['tech'] = info[18]
        defect_classification['non_tech'] = info[19]
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
        function['total'] = total
        function['covered'] = covered
        # coverage
        coverage['percent_coverage_MCDC'] = info[7]
        coverage['percent_coverage_Analysis'] = info[8]
        coverage['total_coverage'] = info[9]
        # function
        function['function_name'] = info[2]
        function['analyst'] = info[4]
        function['site'] = info[5]
        # strfy datetime
        if isinstance(info[6], datetime.datetime):
            function['start_date'] = info[6].strftime("%Y-%m-%d")
        else:
            function['start_date'] = info[6]
        function['coverage'] = coverage
        # function['moduleStrucData'] = module_structure_data
        function['oversight'] = info[17]
        function['defect_classification'] = defect_classification

        # see if info a new module line
        if info[1] not in modules_name_list or len(modules) == 0:
            module = {
                'module_name': None,
                'functions': []
            }
            module['process'] = info[0]
            module['module_name'] = info[1]
            module['functions'].append(function)
            functions_name_list.append(function['function_name'])
            total_function = total_function + 1
            modules.append(module)
            modules_name_list.append(module['module_name'])
        # in case module already exist, add function to corresponding module
        else:
            for index, module_name in enumerate(modules_name_list):
                if module_name == str(module['module_name']):
                    (modules[index])['functions'].append(function)
                    functions_name_list.append(function['function_name'])
                    total_function = total_function + 1

    # write into log file
    output_log(
        f"Total functions of {test_plan_sheet.name} is: {total_function}")
    output_log(f"total functions shows as below ({len(functions_name_list)}):")
    output_log(functions_name_list)
    output_log(f"total module shows as below ({len(modules_name_list)}):")
    output_log(modules_name_list)

    return modules, level_total_coverage, functions_name_list


def read_exceptions(test_exeception_sheet, rows):
    """Read test exception informations of scga

    Args:
        test_exeception_sheet (xlwing test exception sheet): xlwing test exception sheet
        rows (int): row number of test exception sheet

    Raises:
        ValueError: None

    Returns:
        dict list -- uncovered_modules: dataset of all uncovered file involved in scga
    """
    uncovered_modules = []
    uncovered_modules_name_list = []
    uncovered_functions_name_list = []
    uncovered_module = {
        'module_name': None,
        'functions': []
    }
    uncovered_function = {
        'function_name': None,
        'note': None,
        'uncoverage': []
    }
    total_uncoverage = 0
    for curRow in range(6, rows + 2):
        range_ = f"{f'A{curRow}'}:{f'M{curRow}'}"
        info = test_exeception_sheet.range(
            range_).options(transpose=True).value
        if info[1] is None:
            continue
        uncoverage = {
            'uncovered_sw_line': [],
            'uncovered_instrument_sw_line': [],
            'requirement_id': '',
            'analyst': None,
            '_class': None,
            '_class_str': None,
            'analysis_summary': None,
            'correction_summary': None,
            'issue': None,
            'PAR_SCR': None,
            'comment': None,
            # 'applicable': {}
        }
        # applicable = {
        #     'PAR_SCR': None,
        #     'comment': None
        # }
        uncovered_function['note'] = info[0]
        # uncovered software line
        uncoverage['uncovered_sw_line'] = info[3]
        # uncovered software code
        uncoverage['uncovered_instrument_sw_line'] = info[4]
        # requirements
        if info[5] is not None:
            # uncoverage['requirement_id'] = str(info[5]).split('\n')
            uncoverage['requirement_id'] = info[5]
        uncoverage['analyst'] = info[6]
        uncoverage['_class_str'] = str(info[7]).replace('\\', '')
        uncoverage['_class'] = set_class(info[7])
        uncoverage['correction_summary'] = info[9]
        uncoverage['issue'] = info[10]
        uncoverage['PAR_SCR'] = info[11]
        uncoverage['comment'] = info[12]
        # applicable['PAR_SCR'] = info[11]
        # applicable['comment'] = info[12]
        # uncoverage['applicable'] = applicable
        # see if info has new function
        if info[2] not in uncovered_functions_name_list or len(uncovered_functions_name_list) == 0:
            uncovered_function = {
                'function_name': None,
                'note': None,
                'uncoverages': [],
                'uncoverage_count': 0
            }
            uncovered_function['note'] = info[0]
            uncovered_function['function_name'] = info[2]
            uncovered_function['uncoverages'].append(uncoverage)
            uncovered_function['uncoverage_count'] = uncovered_function['uncoverage_count'] + 1
            total_uncoverage = total_uncoverage + 1
            uncovered_functions_name_list.append(
                uncovered_function['function_name'])
            # see if info a new module line
            if info[1] not in uncovered_modules_name_list or len(uncovered_modules) == 0:
                uncovered_module = {
                    'module_name': None,
                    'functions': []
                }
                uncovered_module['process'] = info[0]
                uncovered_module['module_name'] = info[1]
                uncovered_module['functions'].append(uncovered_function)
                uncovered_modules.append(uncovered_module)
                uncovered_modules_name_list.append(
                    uncovered_module['module_name'])
            # in case module already exist, add function to corresponding module
            else:
                for index, module_name in enumerate(uncovered_modules_name_list):
                    if module_name == str(uncovered_module['module_name']):
                        (uncovered_modules[index])[
                            'functions'].append(uncovered_function)
        else:  # in case function already exist, add uncoverage information to corresponding function in corresponding module
            for i, module_name in enumerate(uncovered_modules_name_list):
                if module_name == info[1]:
                    for j, uncovered_function in enumerate((uncovered_modules[i])['functions']):
                        if info[2] == uncovered_function['function_name']:
                            (uncovered_modules[i])[
                                'functions'][j]['uncoverages'].append(uncoverage)
                            (uncovered_modules[i])['functions'][j]['uncoverage_count'] = (
                                uncovered_modules[i])['functions'][j]['uncoverage_count'] + 1
                            total_uncoverage = total_uncoverage + 1
    # write into log file
    output_log(
        f"Total uncovered situation of {test_exeception_sheet.name} is: {total_uncoverage}")
    output_log(
        f"total functions shows as below ({len(uncovered_functions_name_list)}):")
    output_log(uncovered_functions_name_list)
    output_log(
        f"total module shows as below ({len(uncovered_modules_name_list)}):")
    output_log(uncovered_modules_name_list)

    return uncovered_modules


def read_SCGA(app, scga_path):
    """_summary_

    Args:
        app (xlwings app): xlwings app
        scga_path (string): path of scga excel file

    Raises:
        ValueError: None

    Returns:
        dict: scga dataset
        dict: scga funtions list of each level
    """
    READ_PLAN = False
    READ_EXCEPTION = False
    SCGA = {
        'file_name': os.path.basename(scga_path),
        'baseline': str(os.path.basename(scga_path)).split('_SCGA')[0],
        'levels': []
    }

    scga_function_list = {
        'baseline': str(os.path.basename(scga_path)).split('_SCGA')[0],
        'levelAFunctions': [],
        'levelBFunctions': [],
        'levelCFunctions': []
    }
    scga_sheets = app.books.open(scga_path)
    sheet_name_list = [sheet.name for sheet in scga_sheets.sheets]
    for currentSheet in scga_sheets.sheets:
        if 'Level' in currentSheet.name:
            if not (READ_PLAN or READ_EXCEPTION):
                Level = {
                    'level': None,
                    'test_plan': {},
                    'test_exception': {},
                }
            # point to file end
            scga_log_f.seek(0, 2)
            output_log(f'='*60)
            output_log(f'extration of {currentSheet.name}')
            Level['level'] = str(currentSheet.name).split(' ')[1]
            if 'Plan' in currentSheet.name:
                test_plan = {
                    'sheet_name': None,
                    'modules': [],
                    'lv_total_coverage': {}
                }
                rows = len(pd.read_excel(scga_path, currentSheet.name))
                if rows - 7 != 0:
                    test_plan['sheet_name'] = currentSheet.name
                    # test_plan['level'] = str(currentSheet.name).split(' ')[1]
                    test_plan['modules'], test_plan['lv_total_coverage'], function_list = read_plan(
                        currentSheet, rows)
                    if len(test_plan['modules']) != 0:
                        Level['test_plan'] = test_plan
                        if Level['level'] == 'A':
                            # SCGA['level_A']['test_plan'] = test_plan
                            scga_function_list['levelAFunctions'] = function_list
                        elif Level['level'] == 'B':
                            # SCGA['level_B']['test_plan'] = test_plan
                            scga_function_list['levelBFunctions'] = function_list
                        elif Level['level'] == 'C':
                            # SCGA['level_C']['test_plan'] = test_plan
                            scga_function_list['levelCFunctions'] = function_list

                else:
                    scga_log_f.seek(0, 2)
                    output_log(
                        f'* SCGA Test Plan information not found in {currentSheet.name}')
                READ_PLAN = True
            elif 'Exceptions' in currentSheet.name:
                test_exception = {
                    'sheet_name': None,
                    # 'level': None,
                    'modules': [],
                }
                rows = len(pd.read_excel(scga_path, currentSheet.name))
                if rows - 5 != 0:
                    test_exception['sheet_name'] = currentSheet.name
                    # test_exception['level'] = str(currentSheet.name).split(' ')[1]
                    test_exception['modules'] = read_exceptions(currentSheet, rows)
                    if len(test_exception['modules']) != 0:
                        Level['test_exception'] = test_exception

                else:
                    scga_log_f.seek(0, 2)
                    output_log(
                        f'* SCGA Test Execptions information not found in {currentSheet.name}')
                READ_EXCEPTION = True
            if READ_PLAN and READ_EXCEPTION:
                SCGA['levels'].append(Level)
                READ_PLAN = False
                READ_EXCEPTION = False
    return SCGA, scga_function_list


def parser_SCGAs(app, scga_rootpath):
    """Read all SCGA excel workbook from given root path

    Args:
        app (instance): xlwing excel app
        scga_root_path (_type_): root path of all scga excel to parser

    Raises:
        ValueError: None

    Returns:
        dict list: SCGAs dataset list
        list: function list of SCGAs
    """
    SCGAs = []
    all_scga_function_list = []
    sizecounter = 0
    for root, dirs, files in os.walk(scga_rootpath):
        # progress bar
        for scga_f in files:
            if scga_f.endswith('xlsm') and '~' not in str(scga_f) and 'SCGA' in str(scga_f):
                sizecounter += 1
        # with tqdm(total=sizecounter, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
        #     for scga_f in files:
        for scga_f in tqdm(files, desc="Extracting SCGA files", total=sizecounter, unit="files"):
            # only handle 'SCGA' excel file, and ignore not 'xlsm' file and excel buffer file
            if scga_f.endswith('xlsm') and '~' not in str(scga_f) and 'SCGA' in str(scga_f):
                output_log(f'='*80)
                output_log(f"extracting {scga_f}...")
                # write down frist
                scga_log_f.flush()
                SCGA, scga_function_list = read_SCGA(
                    app, os.path.join(root, scga_f))
                SCGAs.append(SCGA)

                all_scga_function_list.append(scga_function_list)
                # point to file end
                scga_log_f.seek(0, 2)
                output_log(f'='*60)
                output_log(f'extraction done !')
                output_log(f'='*80)
                output_log()
    json.dump(SCGAs, scga_json, indent=4, default=str)
    pickle.dump(SCGAs, scga_pickle, protocol=pickle.HIGHEST_PROTOCOL)
    output_log(f'all extraction done !')
    return SCGAs, all_scga_function_list


def generate_alphabet_list(n):
    """Generate a alphabet list start from 'a'

    Args:
        n (int): number alphabet needed to gerenate

    Raises:
        ValueError: None

    Returns:
        list: list of alphabet from start from 'a'
    """
    if n < 1 or n > 26:
        raise ValueError("The number must be between 1 and 26 inclusive.")
    return [chr(i) for i in range(65, 65 + n)]


def output_all_functions_as_sheet(rootpath, scga_list):
    """Output function list table of scga 

    """
    excelApp = xw.App(visible=False, add_book=False)
    wb = excelApp.books.add()
    ws = wb.sheets[0]
    ws.name = 'SCGA Fcuntion List'
    column_range = generate_alphabet_list(len(scga_list))
    for idx, value in enumerate(scga_list):
        start_pos = f'{column_range[idx]}2'
        ws.range(f'{column_range[idx]}1').value = value['baseline']
        ws.range(start_pos).options(
            transpose=True).value = value['levelAFunctions']

    wb.save(os.path.join(rootpath, r'all_functions.xlsm'))
    wb.close()
    excelApp.quit()


def search_function_in_list(scga_list, searched_func):
    """Search function in ['modules'] list of scga
    """
    for funcIdx, item in enumerate(scga_list):
        if item.get('function_name') == searched_func:
            return funcIdx, item
    return None


def search_function_in_nested_scga(scga_dict, searched_func, path=None):
    """function recursion search in a nested scga

        # cur_path is keys of function from top to bottom level of a nested dict
        # modIdx is index of module in ['modules'] list
        # funcIdx is index of function in ['functions'] list
    """
    if path is None:
        path = []
    if isinstance(scga_dict, dict):
        for key, value in scga_dict.items():
            cur_path = path + [key]
            if isinstance(value, dict):
                result = search_function_in_nested_scga(
                    value, searched_func, cur_path)
                if result is not None:
                    return result
            # in case found ['modules'] list
            elif isinstance(value, list) and (key == 'modules'):
                for modIdx, item in enumerate(value):
                    res = search_function_in_list(
                        item.get('functions'), searched_func)
                    if res:
                        funcIdx, func = res
                        return func, cur_path, modIdx, funcIdx
    return None


def get_output_str(scga_dict, res):
    #
    function, key_path, modIdx, funcIdx = res
    mods = scga_dict
    # get module with give key_path (use dict.get() to get item of each key)
    for key in key_path:
        mods = mods.get(key)
    mod = mods[modIdx]
    output_str = f"\t* {scga_dict.get('file_name')} -> {mod.get('module_name')}\n"
    return output_str


def search_func(pkl_file_path, func_str):
    """Search function in scga dataset
    """
    result = None
    output_str = None
    try:
        # deserializer scga pickle file
        scga_pickle_path = os.path.join(pkl_file_path + r'\scgas.pkl')
        with open(scga_pickle_path, 'rb') as scga_pkl:
            deserialized_scga_data = pickle.load(scga_pkl)
            # in case multiple scga dict saved in pkl
            if isinstance(deserialized_scga_data, list):
                result = []
                for index, scga_dict in enumerate(deserialized_scga_data):
                    res = search_function_in_nested_scga(scga_dict, func_str)
                    if res:
                        if output_str is None:
                            output_str = get_output_str(scga_dict, res)
                        else:
                            output_str = output_str + \
                                get_output_str(scga_dict, res)
                        result.append(res)
            # in case only one scga dict saved in pkl
            elif isinstance(deserialized_scga_data, dict):
                result = search_function_in_nested_scga(
                    deserialized_scga_data, func_str)
                if result:
                    output_str = get_output_str(scga_dict, res)
            print(f"Found function '{func_str}' at path:\n {output_str}")
    except FileNotFoundError:
        print(
            f'The file {scga_pkl} does not exist, you may need to extract new SCGA data group first')
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
        "Welcom to SCGA extration:\n" +
        "\t1. Extract new SCGA data group\n" +
        "\t2. Add new SCGA data group\n" +
        "\t3. Search function from existing SCGA data group\n" +
        "Choose your operation: ")
    print(f'='*80)
    global scga_log
    while not (int(selection) == 1 or int(selection) == 2 or int(selection) == 3):
        print("Wrong selection..")
        selection = input(
            "\t1. Extract new SCGA data group\n" +
            "\t2. Add new SCGA data group\n" +
            "\t3. Search function from existing SCGA data group\n" +
            "Choose your operation: ")
    else:
        # create/add SCGA dataset
        if int(selection) == 1 or int(selection) == 2:
            rootPath = input("Please enter the root path: ")
            excelApp = xw.App(visible=False, add_book=False)
            while not os.path.isdir(rootPath):
                rootPath = input(
                    "Can not found this location, please enter the root path again: ")
            else:
                try:
                    # outputPath = os.path.join(rootPath, r'Output')
                    # outputPath.mkdir(parents=True, exist_ok=True)
                    scga_log_path = os.path.join(rootPath + r'/scga_log.txt')
                    scgas_json_path = os.path.join(rootPath + r'/scgas.json')
                    scga_pickle_path = os.path.join(rootPath + r'/scgas.pkl')
                    if int(selection) == 1:
                        scga_log_f = open(scga_log_path, 'w', encoding='UTF-8')
                        scga_json = open(scgas_json_path, 'w', encoding='UTF-8')
                        scga_pickle = open(scga_pickle_path, 'wb')
                    else:
                        scga_log_f = open(scga_log_path, 'a', encoding='UTF-8')
                        scgas_json_path = open(
                            scgas_json_path, 'a', encoding='UTF-8')
                        scga_pickle = open(scga_pickle_path, 'ab')
                    # read all SCGA excel from rootpath and output SCGAs dataset
                    SCGAs, scgas_functions_list = parser_SCGAs(
                        excelApp, rootPath)
                    # output function list of each SCGA as excel sheet
                    output_all_functions_as_sheet(
                        rootPath, scgas_functions_list)
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
                rootPath = input(
                    "Can not found this location, please enter the root path again: ")
            else:
                func = input("Input the function name: ")
                search_func(rootPath, func)


if __name__ == '__main__':
    main()
