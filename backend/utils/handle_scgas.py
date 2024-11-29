import os
import json
import pickle
from tqdm import tqdm
import traceback
from scga import SCGA

# buffer file object
# .log, .json, .pkl files
# scga_log_f = None
scga_json = None
scga_pickle = None

def create_buffer(rootPath, selection, log_suffix=None):
    # global scga_log_f
    global scga_json, scga_pickle
    # outputPath = os.path.join(rootPath, r'Output')
    # outputPath.mkdir(parents=True, exist_ok=True)
    if log_suffix:
        # scga_log_path = os.path.join(rootPath + rf'/scga_log_{log_suffix}.txt')
        scgas_json_path = os.path.join(rootPath + rf'/scga_{log_suffix}.json')
        scga_pickle_path = os.path.join(rootPath + rf'/scga_{log_suffix}.pkl')
    else:
        # scga_log_path = os.path.join(rootPath + r'/scgas_log.txt')
        scgas_json_path = os.path.join(rootPath + r'/scgas.json')
        scga_pickle_path = os.path.join(rootPath + r'/scgas.pkl')
    if int(selection) == 1: # new parser
        # scga_log_f = open(scga_log_path, 'w', encoding='UTF-8')
        scga_json = open(scgas_json_path, 'w', encoding='UTF-8')
        scga_pickle = open(scga_pickle_path, 'wb')
    else: # append based on existence
        # scga_log_f = open(scga_log_path, 'a', encoding='UTF-8')
        scgas_json_path = open(scgas_json_path, 'a', encoding='UTF-8')
        scga_pickle = open(scga_pickle_path, 'ab')

# def output_log(str_=None):
#     print(str_, file=scga_log_f)

def parser_SCGAs(scga_rootpath, info=None):
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
        for scga_f in tqdm(files, desc="Extracting SCGA files", total=sizecounter, unit="files"):
            # only handle 'SCGA' excel file, and ignore not 'xlsm' file and excel buffer file
            if scga_f.endswith('xlsm') and '~' not in str(scga_f) and 'SCGA' in str(scga_f):
              
                # write down frist
                # scga_log_f.flush()
                scga_fp = os.path.join(scga_rootpath, scga_f)
                scga = SCGA(scga_fp, info)
                scga.read_scga()
                SCGAs.append(scga.scga_dict)
                all_scga_function_list.append(scga.scga_function_list)
                # point to file end
                # scga_log_f.seek(0, 2)
               
    json.dump(SCGAs, scga_json, indent=4, default=str)
    pickle.dump(SCGAs, scga_pickle, protocol=pickle.HIGHEST_PROTOCOL)
    return SCGAs, all_scga_function_list

def post_SCGAs(rootPath, selection=2, info=None, outputFunctionList = False):
    if os.path.isdir(rootPath) or os.path.isfile(rootPath):
        # outputPath = os.path.join(rootPath, r'Output')
        # outputPath.mkdir(parents=True, exist_ok=True)
        create_buffer(rootPath, selection)
        try:
            # read all SCGA excel from rootpath and output SCGAs dataset
            SCGAs, scgas_functions_list = parser_SCGAs(rootPath, info)
            # output function list of each SCGA as excel sheet
            # if outputFunctionList:
                # output_all_functions_as_sheet(rootPath, scgas_functions_list)
            return {"result": "success", "detail": "parser completed", "data": SCGAs}
        except Exception as err:
            # print(repr(keyerr))
            import pdb; pdb.set_trace()
            print(traceback.print_exc())
            return {"result": "error", "detail": traceback.print_exc()}
        finally:
            # scga_log_f.close()
            scga_json.close()
            scga_pickle.close()
    else:
        return {"result": "error", "detail": 'the input root path is not a valid file or path'}


def main():
    print(f'='*80)
    selection = input(
        "Welcom to SCGA extration:\n" +
        "\t1. Extract new SCGA data group\n" +
        "\t2. Add new SCGA data group\n" +
        "\t3. Search function from existing SCGA data group\n" +
        "Choose your operation: ")
    print(f'='*80)
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
            while not os.path.isdir(rootPath):
                rootPath = input(
                    "Can not found this location, please enter the root path again: ")
            else:
                post_SCGAs(rootPath, selection)
        elif int(selection) == 3:
            rootPath = input("Please enter the root path of pickle file: ")
            while not os.path.isdir(rootPath):
                rootPath = input(
                    "Can not found this location, please enter the root path again: ")
            else:
                func = input("Input the function name: ")
                # search_func(rootPath, func)


if __name__ == '__main__':
    main()