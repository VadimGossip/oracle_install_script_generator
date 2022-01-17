import os
import pprint
import sys
from folder_scanner import object_scan
from oracle_object_middleware import split_oracle_object_list
from pathlib import Path

install_dir = sys.argv[1]
root_dir = os.path.dirname(os.path.dirname((os.path.dirname(install_dir))))

epic_skip_set = {'install'
                ,'useful_scripts' 
                }


tcs_oracle_object_list, err = object_scan(root_dir, epic_skip_set) 

if err == '':
    split_oracle_object_list(tcs_oracle_object_list, install_dir)
    if len(tcs_oracle_object_list) == 0:
        print('Nothing done')
    else:
        print('Operation successfully finished')
else:
    print(err)