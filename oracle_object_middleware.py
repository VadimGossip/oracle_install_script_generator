# Данный скрипт будет получаеть на вход список словарей с оракловыми объектами, разбивать их в зависимости от схемы и сервера на списки, которые будет передавть скрипту, 
# который будет формировать из них файлы. Функции скрипта, сортировка и фильтрация.
from script_writer import create_install_file, create_error_log_file
import git_scanner
import config

allowed_object_type_sort_mask = {"tablespaces"      : 0
                                ,"directories"      : 1
                                ,"dblinks"          : 2
                                ,"users"            : 3
                                ,"synonyms"         : 4
                                ,"scripts_before"   : 5
                                ,"contexts"         : 6
                                ,"sequences"        : 7
                                ,"types"            : 8
                                ,"tables"           : 9
                                ,"mlogs"            : 10
                                ,"mviews"           : 11
                                ,"types"            : 12
                                ,"packages"         : 13
                                ,"views"            : 14 
                                ,"triggers"         : 15
                                ,"vtbs_tasks"       : 16
                                ,"rows"             : 17
                                ,"roles"            : 18
                                ,"functions"        : 19
                                ,"vtbs_clogs"       : 20
                                ,"scripts_after"    : 21
                                ,"scripts_migration": 22}

def install_script_object_cost(object_type):
    if object_type == 'scripts_before':
        return 0
    elif object_type == 'scripts_after':
        return 2
    else:
        return 1  

def filename_cost(object_type, object_filename):
    def check_object_filename_ending(object_filename, mask):
        return object_filename.split('.')[0][-len(mask):] == mask
    if object_type == 'packages':
        if check_object_filename_ending(object_filename, 'read'):
            return 0
        if check_object_filename_ending(object_filename, 'digests'):
            return 1
        elif check_object_filename_ending(object_filename, 'utils'):
            return 2
        elif check_object_filename_ending(object_filename, 'ri'):
            return 3
        elif check_object_filename_ending(object_filename, 'ui'):
            return 4
        else:
            return 100
    elif object_type == 'types':
        return len(object_filename)

def module_object_type_cost(object_type):
    try:             
        return allowed_object_type_sort_mask[object_type]   
    except KeyError:
        return 100

def sort_object_list (tcs_oracle_object_list):
    return sorted(tcs_oracle_object_list, key = lambda item: (install_script_object_cost(item['object_type']), item['epic_module_name'], item['module_name'], module_object_type_cost(item['object_type']), filename_cost(item['object_type'], item['filename'])))

def split_oracle_object_list(tcs_oracle_object_list):
    core_vtbs_list, hpffm_vtbs_list, hpffm_vtbs_adesk_list, hpffm_vtbs_x_alaris_list, hpffm_vtbs_bi_list = [],[],[],[],[]
    core_vtbs_migration_list, hpffm_vtbs_migration_list, hpffm_vtbs_adesk_migration_list, hpffm_vtbs_x_alaris_migration_list, hpffm_vtbs_bi_migration_list = [],[],[],[],[]
    undef_schema_list, undef_object_type_list = [],[]
    splited_oracle_object_list = []
    git_full_filename_path_list = git_scanner.scan_git_for_changed_objects()
    for object in tcs_oracle_object_list:
        if  (object["path_to_file"] in git_full_filename_path_list or config.mode_params["scan_mode_name"] == 'full') and object["object_type"] in allowed_object_type_sort_mask:
            if object["schema"] == 'vtbs' and object["server"] == 'core' :
                if object["object_type"] == 'scripts_migration':
                    core_vtbs_migration_list.append(object)
                else:
                    core_vtbs_list.append(object)
            elif object["schema"] == 'vtbs' and object["server"] == 'hpffm':
                if object["object_type"] == 'scripts_migration':
                    hpffm_vtbs_migration_list.append(object)
                else:
                    hpffm_vtbs_list.append(object)
            elif object["schema"] == 'vtbs_adesk' and object["server"] == 'hpffm':
                if object["object_type"] == 'scripts_migration':
                    hpffm_vtbs_adesk_migration_list.append(object)
                else:
                    hpffm_vtbs_adesk_list.append(object)
            elif object["schema"] == 'vtbs_x_alaris' and object["server"] == 'hpffm':
                if object["object_type"] == 'scripts_migration':
                    hpffm_vtbs_x_alaris_migration_list.append(object)
                else:
                    hpffm_vtbs_x_alaris_list.append(object)
            elif object["schema"] == 'vtbs_bi' and object["server"] == 'hpffm':
                if object["object_type"] == 'scripts_migration':
                    hpffm_vtbs_bi_migration_list.append(object)
                else:
                    hpffm_vtbs_bi_list.append(object)
            else:
                undef_schema_list.append(object)
        
            if object["object_type"] not in allowed_object_type_sort_mask:
                undef_object_type_list.append(object)
    
    if len(core_vtbs_list) != 0:
        splited_oracle_object_list.append({"filename"     : '10_VTBS_CORE.sql',
                                          "object_list"   : sort_object_list(core_vtbs_list)}) 
    if len(hpffm_vtbs_list) != 0:
        splited_oracle_object_list.append({"filename"     : '20_VTBS_HPFFM.sql',
                                           "object_list"  : sort_object_list(hpffm_vtbs_list)})
    if len(hpffm_vtbs_adesk_list) != 0:
        splited_oracle_object_list.append({"filename"     : '30_VTBS_ADESK_HPFFM.sql',
                                           "object_list"  : sort_object_list(hpffm_vtbs_adesk_list)})
    if len(hpffm_vtbs_x_alaris_list) != 0:
        splited_oracle_object_list.append({"filename"     : '40_VTBS_X_ALARIS_HPFFM.sql',
                                           "object_list"  : sort_object_list(hpffm_vtbs_x_alaris_list)})
    if len(hpffm_vtbs_bi_list) != 0:
        splited_oracle_object_list.append( {"filename"     : '50_VTBS_BI_HPFFM.sql',
                                            "object_list"  : sort_object_list(hpffm_vtbs_bi_list)})
    
    if len(core_vtbs_migration_list) != 0:
        splited_oracle_object_list.append({"filename"     : '90_VTBS_CORE_MIGRATION.sql',
                                          "object_list"   : sort_object_list(core_vtbs_migration_list)}) 
    if len(hpffm_vtbs_migration_list) != 0:
        splited_oracle_object_list.append({"filename"     : '91_VTBS_HPFFM_MIGRATION.sql',
                                           "object_list"  : sort_object_list(hpffm_vtbs_migration_list)})
    if len(hpffm_vtbs_adesk_migration_list) != 0:
        splited_oracle_object_list.append({"filename"     : '92_VTBS_ADESK_HPFFM_MIGRATION.sql',
                                           "object_list"  : sort_object_list(hpffm_vtbs_adesk_migration_list)})
    if len(hpffm_vtbs_x_alaris_migration_list) != 0:
        splited_oracle_object_list.append({"filename"     : '93_VTBS_X_ALARIS_HPFFM_MIGRATION.sql',
                                           "object_list"  : sort_object_list(hpffm_vtbs_x_alaris_migration_list)})
    if len(hpffm_vtbs_bi_migration_list) != 0:
        splited_oracle_object_list.append( {"filename"     : '94_VTBS_BI_HPFFM_MIGRATION.sql',
                                            "object_list"  : sort_object_list(hpffm_vtbs_bi_migration_list)})
    return splited_oracle_object_list, undef_object_type_list, undef_schema_list

def send_data_to_script_writer(tcs_oracle_object_list):
    splited_oracle_object_list, undef_object_type_list, undef_schema_list = split_oracle_object_list(tcs_oracle_object_list)

    file_created = create_error_log_file(undef_schema_list, undef_object_type_list, 'error_log.txt')
    for splited_item in splited_oracle_object_list:
        file_created = create_install_file(splited_item["object_list"], splited_item["filename"]) or file_created
    return file_created