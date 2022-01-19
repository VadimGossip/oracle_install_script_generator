from folder_scanner import object_scan
from oracle_object_middleware import send_data_to_script_writer
import config
import git_scanner
result  = False

if config.gen_mode in ['full', 'patch']:
    
    if config.gen_mode == 'full':
        epic_module_skip_set = {'install'
                              ,'useful_scripts' 
                               }
        object_type_skip_set = {'install'} 
        drop_existing = True
    elif config.gen_mode == 'patch': 
        epic_module_skip_set = set()
        object_type_skip_set = {'install'
                               ,'tables'
                               ,'rows'
                               ,'roles'}
        drop_existing = False

    tcs_oracle_object_list, err = object_scan(epic_module_skip_set, object_type_skip_set)
    if err == '':
        result = send_data_to_script_writer(tcs_oracle_object_list, drop_existing)
        if result:
            print('Operation successfully finished')
        else:
            print('Nothing done')        
    else:
        print(err)    
else:
    print('Unknown script mode, only full\\patch mode allowed')