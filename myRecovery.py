import subprocess

"""
    -l to get the latest backup. You can remove it and precise exactly the desired file after -a
    The program will ask the path of the recovery folder or "where you want the archive to be unarchived".
"""

subprocess.call(["C:\\Users\\ffran\\Anaconda3\\python.exe", "C:\\_util\\tar_backup\\recover.py", "-a", "Z:\\backup0.tar.gz", "-d", input("Recover backup at this path: "), "-l"])
