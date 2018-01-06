from util import change_cwd_drive, make_destination_folder, remove_drive_letter
import subprocess, os, sys

ARCHIVE_FOLDER = "Z:\\"
DESTINATION_FOLDER = "C:\\Users\\ffran\\Desktop\\recover"


def get_archive_file_number(archive):
    num = ""
    for c in os.path.basename(archive):
        if c.isdigit():
            num += c
    if not num:
        num = -1
    return int(num)

def get_archive_by_number(archive, i):
    new_archive = ""
    put_i = False
    for c in archive:
        if not c.isdigit():
            new_archive += c
        elif not put_i:
            new_archive += str(i)
            put_i = True
    return new_archive


def create_dest_folder(dest):
    if not os.path.isdir(dest):
        os.makedirs(dest)

def get_most_recent_archive(archive_folder):
    biggest_num = -1
    for f in os.listdir(archive_folder):
        num = get_archive_file_number(f)
        if num > biggest_num:
            biggest_num = num
            archive = f
    return archive

def split_destination_for_command(destination):
    if destination[0].isalpha() and destination[1] == ':' and destination[2] == '\\':
        destination_drive = "/" + destination[0]
        destination = './' + destination[3:].replace('\\', '/')
        return destination_drive, destination
    else:
        print("Destination path must respect the format C:\\path")

def get_save_folder(archive):
    return os.path.join(os.path.dirname(archive), 'save')


def create_tar_command(archive, destination):
    destination_drive, destination = split_destination_for_command(destination)
    save_folder = get_save_folder(archive)
    #en ce moment le save_folder c'est folder
    #est-ce que ça devrait être ./folder ?
    return ['tar', '-xvpz', '--listed-incremental=' + save_folder, '-f', archive, '-C', destination_drive, destination]


###############################################################################
if __name__ == "__main__":
    os.chdir(ARCHIVE_FOLDER)
    archive = get_most_recent_archive(ARCHIVE_FOLDER)
    save_folder = os.path.join(ARCHIVE_FOLDER, "save")
    archive_folder_no_drive = remove_drive_letter(ARCHIVE_FOLDER)
    for i in range(get_archive_file_number(archive) + 1):
        archive = get_archive_by_number(archive, i)
        print(create_tar_command(archive, DESTINATION_FOLDER))
        #subprocess.call()
