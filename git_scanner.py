#Scan Git for last commit files, only this files can be used as intall script oracle objects
from dataclasses import replace
from fileinput import filename
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
    repository = git.Repo(config.root_dir)
    filtered_commit_list = list(repository.iter_commits())[:config.commit_look_depth]
    for commit in filtered_commit_list:
        for item in commit.stats.files:
            path_list = item.split('/')
            
            epic_module_name = path_parser.extract_info_from_path_list(path_list, 'epic_module_name')
            module_name = path_parser.extract_info_from_path_list(path_list, 'module_name')
            object_type = path_parser.extract_info_from_path_list(path_list, 'object_type')
            filename = check_rename(path_parser.extract_info_from_path_list(path_list, 'filename'))
            
            path_to_file = os.fspath(Path(config.root_dir, epic_module_name, module_name, object_type, filename))
            
            if (epic_module_name != 'install' or object_type.find('scripts') != -1) and path_to_file not in git_full_filename_path_list:
                git_full_filename_path_list.append(path_to_file)
    return git_full_filename_path_list