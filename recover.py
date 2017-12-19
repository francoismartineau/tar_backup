from util import path_remove_drive, change_drive, switch_path_slashes
import subprocess, os, sys, optparse

"""
To recover an archive file, run this scripts with arguments as follows:
    -archive file path
    -destination folder. For example an external drive.
To run this script you need Python3 and Tar for windows.

Options
    -a path to archive file
    -d path to recovery folder
    -l specify alone if you want to recover the latest version of the specified archive file
"""

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

def get_most_recent_archive(archive):
    folder = os.path.dirname(archive)
    biggest_num = -1
    if os.path.isdir(folder):
        for f in os.listdir(folder):
            num = get_archive_file_number(f)
            if num > biggest_num:
                biggest_num = num
                archive = f
    return archive

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-a", "--archive", action="store", dest="archive", help="Path to the targeted archive file.")
    parser.add_option("-d", "--dest", action="store", dest="dest", help="Path to the folder where to store recovered files.")
    parser.add_option("-l", "--latest", action="store_true", dest="recover_latest", default=False, help="Specify if you want to recover the latest version of the specified target file.")
    opts = parser.parse_args(sys.argv[1:])[0]
    return opts.archive, opts.dest, opts.recover_latest


if __name__ == "__main__":
    archive, dest, recover_latest = get_arguments()
    if recover_latest:
        archive = get_most_recent_archive(archive)
    if os.path.isfile(archive) and os.path.isdir(os.path.dirname(dest)):
        change_drive(archive)
        archive = path_remove_drive(archive)
        dest = switch_path_slashes(dest)
        create_dest_folder(dest)
        save = os.path.join(os.path.dirname(archive), "save")
        for i in range(get_archive_file_number(archive) + 1):
            archive = get_archive_by_number(archive, i)
            subprocess.call(['tar', '-xvpz', '--listed-incremental=' + save, '-f', archive, '-C', dest])
    else:
        print("Arguments are: archive_path dest_folder")


