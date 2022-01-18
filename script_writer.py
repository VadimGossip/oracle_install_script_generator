#Данный скрипт получает на вход список словарей объектов и имя файла, который необходимо создать, а также параметр, в зависимости от которого будут удаляться существующие файлы с таким именем или создаваться новые копии. 
import os
from pathlib import Path

def remove_file(full_path):
    try:
         os.remove(full_path)
    except OSError as e:
        None

def get_schema_by_server_schema(server, schema):
    if server == 'core' and schema == 'vtbs':
        return 'core'
    elif server == 'hpffm' and schema == 'vtbs':   
        return 'hpffm'
    elif server == 'hpffm' and schema == 'vtbs_bi':   
        return 'vtbs_bi'
    elif server == 'hpffm' and schema == 'vtbs_x_alaris':   
        return 'xalaris'
    elif server == 'hpffm' and schema == 'vtbs_adesk':   
        return 'adesk'
    else:
        return ''

def create_error_log_file(undef_schema_list, undef_object_type_list, install_dir, install_filename, drop_existing):
    full_err_path = Path(install_dir, install_filename)

    if drop_existing == True:
        remove_file(full_err_path)
    
    error_script_text = ''
    create_err_file = False
    
    for item in undef_schema_list:
        create_err_file = True
        if error_script_text.find('No Server\Schema') == -1:
            error_script_text += 'No Server\Schema \n'
        error_script_text += item["path_to_file"] + '\n'
    
    if create_err_file:
        error_script_text += '\n'

    for item in undef_object_type_list:
        create_err_file = True
        if error_script_text.find('Unknow object type') == -1:
            error_script_text += 'Unknow object type or file in root of module \n'
        
        error_script_text += item['object_type'] + '    ' + item["path_to_file"] + '\n'
    
    if create_err_file:
        f = open(full_err_path, 'a+')
        f.write(error_script_text)
        f.close()
    
    return create_err_file

def create_install_file(object_list, install_dir, root_dir, install_filename, drop_existing):
    full_path = Path(install_dir, install_filename)
        
    if drop_existing == True:
        remove_file(full_path)
  
    install_script_text = ''
    object_type_header = ''
    module_header = ''
    create_file = False

    for item in object_list:
        create_file = True

        if install_script_text == '':
            install_script_text =  '-- Schema: ' + get_schema_by_server_schema(item["server"], item["schema"]).upper() + ' \nprompt install '+ install_filename + ' \nset define off spool ' + install_filename.split('.')[0] + '.log append \n \n'
        
        if item["object_type"].find('scripts') == -1:
            cur_module_header = '-------------------------'+ item['epic_module_name'] + '/' + item['module_name'] + '-------------------------'
            main_path = root_dir
        else:
            cur_module_header = '-------------------------'+ item['epic_module_name'] + '/' + item["object_type"] + '-------------------------'
            main_path = install_dir
        
        cur_object_type_header = 'prompt '+ item["object_type"]
         
        if module_header != cur_module_header:
            install_script_text += '\n' + cur_module_header + '\n'
            module_header = cur_module_header
            object_type_header = ''
        if object_type_header != cur_object_type_header:
            install_script_text += '\n' + cur_object_type_header + '\n'
            object_type_header = cur_object_type_header 
        
        install_script_text += 'prompt ' + item["path_to_file"].replace(main_path, '').replace('\\','/') + '\n'
        if item["object_type"].find('scripts') == -1:
            install_script_text += item["path_to_file"].replace(main_path, '@ ../..').replace('\\','/') + '\n'
        else:
            install_script_text += item["path_to_file"].replace(main_path, '@     .').replace('\\','/') + '\n'
    
    if create_file:
       install_script_text += '\n' + 'spool off'
       f = open(full_path, 'a+')
       f.write(install_script_text)
       f.close()   
    
    return create_file
