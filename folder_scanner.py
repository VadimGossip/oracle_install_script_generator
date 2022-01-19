# Скрипт принимает на вход каталог, в который сложит результат своей работы - ораловые скрипты инсталяции
# Сканнер поднимается на 3 шага вверх относительно указанной папки и после этого сканирует все файлы лежащие ниже, превращая их в список словарей.
import os
from pathlib import Path
import config
import path_parser

tcs_oracle_object_list = []

def get_server_schema_by_tag(item):
    server_schema_dict = {
                            "server" : '', 
                            "schema" : ''
                         }
    if item == 'core':
        server_schema_dict["server"] = 'core'
        server_schema_dict["schema"] = 'vtbs'
    elif item == 'charger' or item == 'hpffm':
        server_schema_dict["server"] = 'hpffm'
        server_schema_dict["schema"] = 'vtbs'
    elif item == 'vtbs_bi':
        server_schema_dict["server"] = 'hpffm'
        server_schema_dict["schema"] = 'vtbs_bi'
    elif item == 'vtbs_x_alaris' or item == 'xalaris':
        server_schema_dict["server"] = 'hpffm'
        server_schema_dict["schema"] = 'vtbs_x_alaris'
    elif item == 'adesk' or item == 'vtbs_adesk' or item == 'reporter':
        server_schema_dict["server"] = 'hpffm'
        server_schema_dict["schema"] = 'vtbs_adesk'
    return server_schema_dict

def extract_schema_server_from_file(path):
     error = ''
     server_schema_list = []
     try:
        f = open(path,'r')
        lines = f.readlines()
        for line in lines:
            if line.lower().find("schema") != - 1:
                item_list = line.lower().replace('schema', '').replace(':', '').replace(' ', '') \
                                           .replace('--', '').replace('п»ї', '').replace('/', ',').replace('\\', ',').strip().split(',')
                for item in item_list:
                    dict_item = get_server_schema_by_tag(item)
                    if dict_item not in server_schema_list:
                       server_schema_list.append(dict_item)
                break
        if len(server_schema_list) == 0:
            server_schema_list.append(get_server_schema_by_tag(''))
        f.close()        
     except Exception:
         f.close()
         error = 'Error on extracting server and schema from Path_value = ' + os.fspath(path)   
     return server_schema_list, error

def convert_path_to_tcs_oracle_object(tcs_path, dirpath, filename, epic_module_skip_set, object_type_skip_set):
    error = ''
    path = Path(dirpath, filename)
    try:
        path_wo_tcs_path = (os.fspath((path)).split(tcs_path)[1])[1:]
        path_list = path_wo_tcs_path.split(os.sep)
        epic_module_name = path_parser.extract_info_from_path_list(path_list, 'epic_module_name')
        module_name = path_parser.extract_info_from_path_list(path_list, 'module_name')
        object_type = path_parser.extract_info_from_path_list(path_list, 'object_type')
        
        if object_type == 'tables' and filename.split('.')[1] != 'sql':
            object_type = 'triggers'
        
        if epic_module_name not in epic_module_skip_set and object_type not in object_type_skip_set:
            server_schema_list, error = extract_schema_server_from_file(path)
            for item in server_schema_list:
                tcs_oracle_object = { 
                                        "epic_module_name" : epic_module_name,
                                        "module_name"      : module_name,
                                        "object_type"      : object_type,
                                        "schema"           : item["schema"],
                                        "server"           : item["server"],
                                        "filename"         : filename,
                                        "path_to_file"     : os.fspath(path)
                                    }
                tcs_oracle_object_list.append(tcs_oracle_object)
    except Exception:
        error = 'Error on parsing Path to object of dict. Path_value =' + os.fspath(path) 
    return error

def object_scan(epic_module_skip_set, object_type_skip_set):
    error = ''
    for dirpath, _, filenames in os.walk(config.root_dir): 
        for filename in filenames:
            if filename.find('.') != -1:
                if filename[-len('sql'):] == 'sql':
                    error = convert_path_to_tcs_oracle_object(config.root_dir, dirpath, filename, epic_module_skip_set, object_type_skip_set) 
    return tcs_oracle_object_list, error