#Parse path to oracle object info details

def extract_info_from_path_list(path_list, object_type):
    result = ''
    try:
        if object_type == 'epic_module_name':
            result = path_list[0]
        elif object_type == 'module_name':
            result = path_list[1]
        elif object_type == 'object_type':
            result = path_list[2] 
        elif object_type == 'filename':
            result = path_list[3]
             
    except Exception:
        result = ''
    return result 