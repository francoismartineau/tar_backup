import os, sys


def fix_backup_source_path(source):
    if len(source) >= 2:
        if source[0].isalpha() and source[1] == ":":
            source = "/" + source[0] + source[2:]
        source = source.replace('\\', '/')
    return source

def make_destination_folder(dest):
    if not os.path.isdir(dest):
        os.makedirs(dest)


def remove_drive_letter(path):
    path = path.replace('\\', '/')
    if path[0].isalpha() and path[1] == ':':
        path = "." + path[2:]
    return path

def change_cwd_drive(path):
    if path[0].isalpha() and path[1] == ':':
        os.chdir(path[:2])

def get_arguments():
    arg1 = sys.argv[1:][0]
    arg2 = sys.argv[1:][1]
    return arg1, arg2
