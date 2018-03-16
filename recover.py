from util import change_cwd_drive, make_destination_folder, remove_drive_letter, sleep_settings
import subprocess, os, sys




ARCHIVE_FOLDER = "E:\\"
DESTINATION_FOLDER = "C:\\test_dest"





######################################################
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

def adjust_destination_path(destination):
    if destination[0].isalpha() and destination[1] == ':' and destination[2] == '\\':
        return "/" + destination[0] + '/' + destination[3:].replace('\\', '/')
    else:
        print("Destination path must respect the format C:\\path")

def get_save_folder(archive):
    return os.path.join(os.path.dirname(archive), 'save').replace('\\', '/')


def create_tar_command(archive, destination):
    destination = adjust_destination_path(destination)
    save_folder = get_save_folder(archive)
    return ['tar', '-xvpz', '--listed-incremental=' + save_folder, '-f', archive, '-C', destination, '.']




###############################################################################
if __name__ == "__main__":
    try:
        sleep_settings(False)
        make_destination_folder(DESTINATION_FOLDER)
        os.chdir(ARCHIVE_FOLDER)
        archive = get_most_recent_archive(ARCHIVE_FOLDER)
        save_folder = os.path.join(ARCHIVE_FOLDER, "save")
        archive_folder_no_drive = remove_drive_letter(ARCHIVE_FOLDER)
        for i in range(get_archive_file_number(archive) + 1):
            archive = get_archive_by_number(archive, i)
            command = create_tar_command(archive, DESTINATION_FOLDER)
            subprocess.call(command)
        sleep_settings(True)
        input('Recover finished.')
    except Exception as e:
        sleep_settings(True)
        input(e)
