import os
import pprint
import sys
from folder_scanner import object_scan
from oracle_object_middleware import split_oracle_object_list
from pathlib import Path

gen_mode = ''
install_dir = ''
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
else:
   object_type_skip_set = {'install'
                          ,'tables'
                          ,'rows'}

tcs_oracle_object_list, err = object_scan(root_dir, epic_module_skip_set, object_type_skip_set) 

if err == '':
    split_oracle_object_list(tcs_oracle_object_list, install_dir)
    if len(tcs_oracle_object_list) == 0:
        print('Nothing done')
    else:
        print('Operation successfully finished')
else:
    print(err)