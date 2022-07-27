#Scan Git for last commit files, only this files can be used as intall script oracle objects
import git
import os
from pathlib import Path
import config
import path_parser

def check_rename(filename):
    if filename.find('=>') != -1:
        return filename.split('=>')[1].replace('}', '').replace(' ','')
    else:
        return filename   

def scan_git_for_changed_objects():
    git_full_filename_path_list = []
     
    repository = git.Repo(config.obj_root_dir)
    commit_id = config.mode_params["commit_id"]

    if commit_id == '':
        commit_id = repository.head.commit
        config.mode_params["commit_id"] = commit_id
    
    filtered_commit_list = filter(lambda x: x.committed_datetime >= repository.commit(commit_id).committed_datetime, list(repository.iter_commits()))

    for commit in filtered_commit_list:
        if commit.message.startswith('Merged PR'):
            continue
        else:
            commit_msg = commit.message 
         
        for item in commit.stats.files:
            path_list = item.split('/') 
            
            
            epic_module_name = path_parser.extract_info_from_path_list(path_list, 'epic_module_name')
            module_name = path_parser.extract_info_from_path_list(path_list, 'module_name')
            object_type = path_parser.extract_info_from_path_list(path_list, 'object_type')
            filename = check_rename(path_parser.extract_info_from_path_list(path_list, 'filename'))
            
            path_to_file = os.fspath(Path(config.obj_root_dir, epic_module_name, module_name, object_type, filename))
            
            if (epic_module_name != 'install' or object_type.find('scripts') != -1) and path_to_file not in git_full_filename_path_list:
                git_full_filename_path_list.append(path_to_file)
    return git_full_filename_path_list, commit_msg