import os
import pprint
import sys
from folder_scanner import object_scan
from oracle_object_middleware import send_data_to_script_writer
from pathlib import Path

gen_mode = ''
install_dir = ''
result  = False

try:
    install_dir = sys.argv[1]
    gen_mode = sys.argv[2]
except IndexError:

    print('''You must specify additional parameters: install folder path and operation mode(full\incr)''')
    exit

root_dir = os.path.dirname(os.path.dirname((os.path.dirname(install_dir))))

if gen_mode == 'full':
    epic_module_skip_set = {'install'
                          ,'useful_scripts' 
                          }
    object_type_skip_set = {'install'} 
    drop_existing = True
else:
    object_type_skip_set = {'install'
                          ,'tables'
                          ,'rows'
                          ,'roles'}
    drop_existing = False

tcs_oracle_object_list, err = object_scan(root_dir, epic_module_skip_set, object_type_skip_set) 

if err == '':
    result = send_data_to_script_writer(tcs_oracle_object_list, install_dir, root_dir, drop_existing)
    if result:
        print('Operation successfully finished')
    else:
        print('Nothing done')
       
else:
    print(err)