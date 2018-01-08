from util import remove_drive_letter, fix_backup_source_path, make_destination_folder, change_cwd_drive
import subprocess, os, sys, shutil



BACKUPNAME = "backup"
SOURCE = "C:\\test"
DESTINATION = "E:\\"
EXCLUDES = ["$RECYCLE.BIN", "Program Files (x86)/Steam", "_util/tar_backup"]






###############################################################################

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

def split_source_for_command(source):
    if source[0].isalpha() and source[1] == ':' and source[2] == '\\':
        source_drive = '/' + source[0]
        source = './' + source[3:]
        return source_drive, source
    else:
        print("Source path must respect the format C:\\path")


def create_tar_command(archive, save_file, source):
    source_drive, source = split_source_for_command(source)
    command = ['tar', '-cvpzf',  archive , '--listed-incremental=' + save_file, '-C', source_drive, source]
    for e in EXCLUDES:
        command.append('--exclude=' + e)
    return command


###############################################################################
if __name__ == "__main__":
    try:
        change_cwd_drive(DESTINATION)
        make_destination_folder(DESTINATION)
        archive = remove_drive_letter(get_archive_path(DESTINATION))
        save_file = remove_drive_letter(get_save_file_path(DESTINATION))
        command = create_tar_command(archive, save_file, SOURCE)
        subprocess.call(command)
        input("Backup finished.")
    except Exception as e:
        input(e)

    
