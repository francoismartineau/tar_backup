import os, sys


def switch_path_slashes(path):
    return path.replace('\\', '/')

def path_remove_drive(path):
    path = path.replace('\\', '/')
    if path[0].isalpha() and path[1] == ':':
        path = path[2:]
    return path

def change_drive(path):
    if path[0].isalpha() and path[1] == ':':
        os.chdir(path[:2])


def get_arguments():
    arg1 = sys.argv[1:][0]
    arg2 = sys.argv[1:][1]
    return arg1, arg2
