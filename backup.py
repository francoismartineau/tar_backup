from util import path_remove_drive, change_drive, get_arguments, switch_path_slashes
import subprocess, os, sys, shutil, optparse

"""
To perform a backup run this script with arguments as follows:
    path for a folder to backup. This could be an entire drive (ex: C:)
    path for a folder where to pu the resulting archive file. For example on an external drive.
To run this script you need Python3 and Tar for Windows

Options
"""

BACKUPNAME = "backup"

def get_save_file_path(archive_folder):
    save_folder = os.path.join(archive_folder, "save")
    if not os.path.isdir(save_folder):
        os.makedirs(save_folder)
    num = 0
    for f in os.listdir(save_folder):
        if f.startswith("save.list-"):
            if f[10:].isdigit():
                p_num = int(f[10:])
                if p_num > num:
                    num = p_num
    save_file_path = os.path.join(save_folder, "save.list-" + str(num)) 
    if os.path.isfile(save_file_path):
        old_save_file_path = save_file_path
        save_file_path = os.path.join(save_folder, "save.list-" + str(num + 1)) 
        shutil.copyfile(old_save_file_path, save_file_path)
    return save_file_path
    

def get_archive_path(archive_folder):
    num = -1
    for archive_file in os.listdir(archive_folder):
        if archive_file.startswith(BACKUPNAME) and archive_file[len(BACKUPNAME)].isdigit():
            archive_number = ""
            for c in archive_file[len(BACKUPNAME):]:
                if c.isdigit():
                    archive_number += c
            if int(archive_number) > num:
                num = int(archive_number)
    return os.path.join(archive_folder, BACKUPNAME + str(num + 1) + ".tar.gz")

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-s", "--source", action="store", dest="source", help="Path to the targeted directory to backup.")
    parser.add_option("-d", "--dest", action="store", dest="dest", help="Path to the folder where to store the archive file.")
    opts = parser.parse_args(sys.argv[1:])[0]
    return opts.source, opts.dest




if __name__ == "__main__":
    source, dest = get_arguments()
    source = switch_path_slashes(source) 
    change_drive(dest)
    archive = path_remove_drive(get_archive_path(dest))
    save = path_remove_drive(get_save_file_path(dest))
    subprocess.call(['tar','-cvpzf',  archive , '--listed-incremental=' + save, '-C', source, '.'])
    
