# Данный скрипт будет получаеть на вход список словарей с оракловыми объектами, разбивать их в зависимости от схемы и сервера на списки, которые будет передавть скрипту, 
# который будет формировать из них файлы. Функции скрипта, сортировка и фильтрация.
import pprint
from script_writer import create_install_file, create_error_log_file

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

# def sort_and_filter_by_mode_object_list (tcs_oracle_object_list):
#     tmp_oracle_object_list = []
#     for object in 

    
    # return tcs_oracle_object_list

def split_oracle_object_list(tcs_oracle_object_list):
    core_vtbs_list, hpffm_vtbs_list, hpffm_vtbs_adesk_list, hpffm_vtbs_x_alaris_list, hpffm_vtbs_bi_list, undef_schema_list, undef_object_type_list = [],[],[],[],[],[],[]
    splited_oracle_object_list = []
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
    
    if len(core_vtbs_list) != 0:
        splited_oracle_object_list.append({"filename"     : '10_VTBS_CORE.sql',
                                          "object_list"   : core_vtbs_list}) 
    if len(hpffm_vtbs_list) != 0:
        splited_oracle_object_list.append({"filename"     : '20_VTBS_HPFFM.sql',
                                           "object_list"  : hpffm_vtbs_list})
    if len(hpffm_vtbs_adesk_list) != 0:
        splited_oracle_object_list.append({"filename"     : '30_VTBS_ADESK_HPFFM.sql',
                                           "object_list"  : hpffm_vtbs_adesk_list})
    if len(hpffm_vtbs_x_alaris_list) != 0:
        splited_oracle_object_list.append({"filename"     : '40_VTBS_X_ALARIS_HPFFM.sql',
                                           "object_list"  : hpffm_vtbs_x_alaris_list})
    if len(hpffm_vtbs_bi_list) != 0:
        splited_oracle_object_list.append( {"filename"     : '50_VTBS_BI_HPFFM.sql',
                                            "object_list"  : hpffm_vtbs_bi_list})

    return splited_oracle_object_list, undef_object_type_list, undef_schema_list

def send_data_to_script_writer(tcs_oracle_object_list, install_dir, root_dir, drop_existing):
    print(install_dir)
    splited_oracle_object_list, undef_object_type_list, undef_schema_list = split_oracle_object_list(tcs_oracle_object_list)

    file_created = create_error_log_file(undef_schema_list, undef_object_type_list, install_dir, 'error_log.txt', True)

    for splited_item in splited_oracle_object_list:
        file_created = create_install_file(splited_item["object_list"], install_dir, root_dir, splited_item["filename"], drop_existing) or file_created
    
    return file_created