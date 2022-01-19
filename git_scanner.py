#Scan Git for last commit files, only this files can be used as intall script oracle objects
from dataclasses import replace
import git
import os
from pathlib import Path
import config
import path_parser

def scan_git_for_changed_objects():
    git_full_filename_path_list = []
    repository = git.Repo(config.root_dir)
    commits_list = list(repository.iter_commits())
    commit = commits_list[0] ## вынести параметр, какой коммит брать в конфиг
    for item in commit.stats.files:
        path_list = item.split('/')
        epic_module_name = path_parser.extract_info_from_path_list(path_list, 'epic_module_name')
        module_name = path_parser.extract_info_from_path_list(path_list, 'module_name')
        if epic_module_name != 'install' or module_name == 'scripts':
            git_full_filename_path_list.append(os.fspath(Path(config.root_dir, item)))
    return git_full_filename_path_li