# Данный скрипт будет получаеть на вход список словарей с оракловыми объектами, разбивать их в зависимости от схемы и сервера на списки, которые будет передавть скрипту, 
# который будет формировать из них файлы. Функции скрипта, сортировка и фильтрация.
import pprint
from script_writer import create_error_log_file

allowed_oracle_object_type_set = {'contexts'
                                 ,'mviews'
                                 ,'mlogs'   
                                 ,'packages'
                                 ,'register'
                                 ,'roles'
                                 ,'rows'
                                 ,'sequences'
                                 ,'synonyms'
                                 ,'tables'
                                 ,'types'
                                 ,'users'
                                 ,'views'
                                 ,'vtbs_tasks'
                                 ,'scripts_before'
                                 ,'scripts_after'}

def split_oracle_object_list(tcs_oracle_object_list, install_dir):
    core_vtbs_list, hpffm_vtbs_list, hpffm_vtbs_adesk_list, hpffm_vtbs_x_alaris_list, hpffm_vtbs_bi_list, undef_schema_list, undef_object_type_list = [],[],[],[],[],[],[]
    for object in tcs_oracle_object_list:
        
        if object["schema"] == 'vtbs' and object["server"] == 'core':
            core_vtbs_list.append(object)
        elif object["schema"] == 'vtbs' and object["server"] == 'hpffm': 
            hpffm_vtbs_list.append(object) 
        elif object["schema"] == 'vtbs_adesk' and object["server"] == 'hpffm': 
            hpffm_vtbs_adesk_list.append(object)
        elif object["schema"] == 'vtbs_x_alaris' and object["server"] == 'hpffm': 
            hpffm_vtbs_x_alaris_list.append(object)
        elif object["schema"] == 'vtbs_bi' and object["server"] == 'hpffm': 
            hpffm_vtbs_bi_list.append(object)
        else:
            undef_schema_list.append(object)
        
        if object["object_type"] not in allowed_oracle_object_type_set:
            undef_object_type_list.append(object)

    create_error_log_file(undef_schema_list, undef_object_type_list, install_dir, 'error_log.txt', True)
 
 