# ****************************************************
# run pip install -r requirements.txt for dependencies 
# ****************************************************

import os
import json
import pickle
from tqdm import tqdm
import traceback
from utils.scga import SCGA

# buffer file object
# .log, .json, .pkl files
__new = 1
__add = 2

class SCGAs():

    def __init__(self, rootPath, selection=1, info=None , log_suffix=None):
        if not os.path.isdir(rootPath):
            print("Invalid Path")
            raise ValueError
        self.rootPath = rootPath
        # buffer file object
        # .log, .json, .pkl files
        self.scga_log_f = None
        self.scga_json = None
        self.scga_pickle = None
        self.selection = selection
       
        self.info = info
        self.SCGAs = []
        self.all_scga_function_list = []
        scga_log_path = ''
        scgas_json_path = ''
        scga_pickle_path = ''
        if log_suffix:
            scga_log_path = os.path.join(rootPath + rf'/scga_log_{log_suffix}.txt')
            scgas_json_path = os.path.join(rootPath + rf'/scga_{log_suffix}.json')
            scga_pickle_path = os.path.join(rootPath + rf'/scga_{log_suffix}.pkl')
        else:
            scga_log_path = os.path.join(rootPath + r'/scgas_log.txt')
            scgas_json_path = os.path.join(rootPath + r'/scgas.json')
            scga_pickle_path = os.path.join(rootPath + r'/scgas.pkl')
        if int(selection) == __new: # new parser
            self.scga_log_f = open(scga_log_path, 'w', encoding='UTF-8')
            self.scga_json = open(scgas_json_path, 'w', encoding='UTF-8')
            self.scga_pickle = open(scga_pickle_path, 'wb')
        elif int(selection) == __add: # append based on existence
            self.scga_log_f = open(scga_log_path, 'a', encoding='UTF-8')
            self.scgas_json = open(scgas_json_path, 'a', encoding='UTF-8')
            self.scga_pickle = open(scga_pickle_path, 'ab')
        else:
            print('Invalid Selection')
            raise ValueError


    # def create_buffer(self, rootPath, selection, log_suffix=None):
    #     # global scga_log_f
    #     # outputPath = os.path.join(rootPath, r'Output')
    #     # outputPath.mkdir(parents=True, exist_ok=True)
    #     if log_suffix:
    #         # scga_log_path = os.path.join(rootPath + rf'/scga_log_{log_suffix}.txt')
    #         scgas_json_path = os.path.join(rootPath + rf'/scga_{log_suffix}.json')
    #         scga_pickle_path = os.path.join(rootPath + rf'/scga_{log_suffix}.pkl')
    #     else:
    #         # scga_log_path = os.path.join(rootPath + r'/scgas_log.txt')
    #         scgas_json_path = os.path.join(rootPath + r'/scgas.json')
    #         scga_pickle_path = os.path.join(rootPath + r'/scgas.pkl')
    #     if int(selection) == 1: # new parser
    #         # scga_log_f = open(scga_log_path, 'w', encoding='UTF-8')
    #         scga_json = open(scgas_json_path, 'w', encoding='UTF-8')
    #         scga_pickle = open(scga_pickle_path, 'wb')
    #     else: # append based on existence
    #         # scga_log_f = open(scga_log_path, 'a', encoding='UTF-8')
    #         scgas_json_path = open(scgas_json_path, 'a', encoding='UTF-8')
    #         scga_pickle = open(scga_pickle_path, 'ab')

    # def output_log(str_=None):
    #     print(str_, file=scga_log_f)

    def parser_SCGAs(self):
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
        sizecounter = 0
        for root, dirs, files in os.walk(self.rootPath):
            # progress bar
            for scga_f in files:
                if scga_f.endswith('xlsm') and '~' not in str(scga_f) and 'SCGA' in str(scga_f):
                    sizecounter += 1
            for scga_f in tqdm(files, desc="Extracting SCGA files", total=sizecounter, unit="files"):
                # only handle 'SCGA' excel file, and ignore not 'xlsm' file and excel buffer file
                if scga_f.endswith('xlsm') and '~' not in str(scga_f) and 'SCGA' in str(scga_f):
                
                    # write down frist
                    self.scga_log_f.flush()
                    scga_fp = os.path.join(root, scga_f)
                    scga = SCGA(scga_fp, self.info)
                    scga.read_scga()
                    self.SCGAs.append(scga.scga_dict)
                    self.all_scga_function_list.append(scga.scga_function_list)
                    # point to file end
                    self.scga_log_f.seek(0, 2)
                
        json.dump(self.SCGAs, self.scga_json, indent=4, default=str)
        pickle.dump(self.SCGAs, self.scga_pickle, protocol=pickle.HIGHEST_PROTOCOL)


    def post_SCGAs(self, outputFunctionList = False):
        if os.path.isdir(self.rootPath):
            # outputPath = os.path.join(rootPath, r'Output')
            # outputPath.mkdir(parents=True, exist_ok=True)
            # self.create_buffer(rootPath, selection)
            try:
                # read all SCGA excel from rootpath and output SCGAs dataset
                self.parser_SCGAs()
                # output function list of each SCGA as excel sheet
                # if outputFunctionList:
                #     output_all_functions_as_sheet(rootPath, scgas_functions_list)
                return {"result": "success", "detail": "parser completed"}
            except Exception as err:
                # print(repr(keyerr))
                import pdb; pdb.set_trace()
                print(traceback.print_exc())
                return {"result": "error", "detail": traceback.print_exc()}
            finally:
                self.scga_log_f.close()
                self.scga_json.close()
                self.scga_pickle.close()
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
                SCGAs_process = SCGAs(rootPath, selection)
                SCGAs_process.post_SCGAs()
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