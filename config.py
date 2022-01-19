# Storage of init params and global_variables
import sys
import os

def init_command_line_params():
    try:
        return sys.argv[1], sys.argv[2]
    except IndexError:
        print('''You must specify additional parameters: install folder path and operation mode(full\incr)''')
        sys.exit()

install_dir, gen_mode = init_command_line_params()
root_dir = os.path.dirname(os.path.dirname((os.path.dirname(install_dir))))