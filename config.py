# Storage of init params and global_variables
import sys
import os

install_dir = ''
gen_mode = 'patch'
commit_look_depth = 1

def init_command_line_params():
    def init_install_dir():
        try:    
             return sys.argv[1]
        except IndexError:
            print ('You should specify install folder path')
            sys.exit()
    def init_gen_mode():
        try:    
             return sys.argv[2]
        except IndexError:
            return gen_mode
    def init_commit_look_depth():
        try:    
             return int(sys.argv[3])
        except IndexError:
            return commit_look_depth
    return init_install_dir(), init_gen_mode(), init_commit_look_depth()

install_dir, gen_mode, commit_look_depth = init_command_line_params()
root_dir = os.path.dirname(os.path.dirname((os.path.dirname(install_dir))))
print(install_dir, gen_mode, commit_look_depth)