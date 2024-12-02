import os
import pickle
import traceback


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