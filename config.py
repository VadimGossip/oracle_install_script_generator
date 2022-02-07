# Storage of init params and global_variables
import yaml
import sys
import os
from pathlib import Path

#ToDo: Валидация конфига 
def validate_params(install_dir, obj_root_dir, mode_params):
   if install_dir == None:
      return 'Undefined install dir'
   elif not(os.path.exists(install_dir)):
      return 'Install dir does not exists'
   elif  not(os.path.exists(obj_root_dir)):
      return 'Git root dir is undefined or can''t be calculted from intall dir'
   elif mode_params["scan_mode_name"] == 'undef':
      return 'Script scan mode undefined, please check condig'
   else:
      return ''   

def init_parms_from_config():
    
    yaml_file = open(Path(os.path.dirname(__file__),"config.yaml"))
    parsed_yaml_file = yaml.load(yaml_file, Loader=yaml.FullLoader)
    install_dir = parsed_yaml_file["path"]["install_dir"]
    obj_root_dir = parsed_yaml_file["path"]["obj_root_dir"]

    if obj_root_dir == None:
       obj_root_dir = os.path.dirname((os.path.dirname(install_dir)))

       #проблема закрывающего флеша, в параметре  install dir конфига без него проваливаемся выше. Будет время найти более красиове решение
       if install_dir[-1] == os.sep: 
         obj_root_dir = os.path.dirname(obj_root_dir) 
    
    file_write_mode = {"recreate "  : False,
                       "new_file"   : False,
                       "add_to_end" : False} 
    mode_params = {
                   'scan_mode_name'      : '',
                   'commit_id'           : '',
                   'recreate_file'       : '',
                   'file_write_mode'     : file_write_mode,        
                  }
      
    if bool(parsed_yaml_file["mode"]["full_mode_props"]["enabled"]):
       mode_params["scan_mode_name"] = 'full'
    elif bool(parsed_yaml_file["mode"]["patch_mode_props"]["enabled"]):
       mode_params["scan_mode_name"] = 'patch'   
    else:
       mode_params["scan_mode_name"] = 'undef' 

    if parsed_yaml_file["mode"]["patch_mode_props"]["commit_id"] == None:
       mode_params["commit_depth"] = 1
    else:
       mode_params["commit_id"] =  parsed_yaml_file["mode"]["patch_mode_props"]["commit_id"]
    
    if bool(parsed_yaml_file["mode"]["full_mode_props"]["enabled"]):
       mode_params["file_write_mode"]["recreate"] = True
    elif bool(parsed_yaml_file["mode"]["patch_mode_props"]["enabled"]):
       if bool(parsed_yaml_file["mode"]["patch_mode_props"]["add_to_end"]):
           mode_params["file_write_mode"]["add_to_end"] = True
       else:
           mode_params["file_write_mode"]["new_file"] = True

    return install_dir, obj_root_dir, mode_params

try: 
   install_dir, obj_root_dir, mode_params = init_parms_from_config()
except yaml.YAMLError as exc:
   print ('Can''t parse config, check params')
   sys.exit()

validate_error = validate_params(install_dir, obj_root_dir, mode_params)
if validate_error != '':
   print(validate_error)
   sys.exit()   
else:
   print('Script config parsed install_dir = ' + install_dir + ' obj_root_dir = ' + obj_root_dir + ' mode_params = ' + str(mode_params))