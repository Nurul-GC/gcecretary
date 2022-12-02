"""
This a utility script to help users organize their files without stress.
It goes through a folder and check all files and organize them per type.
Modules Used:

- shutil: provides utilities and functions for copying,
  archiving files and directory's tree.
- os: allows us to work with directories, files and so on.
- sys: This module provides access to some objects and functions
  used by the interpreter and to interact with the system.
"""

from getpass import getuser
from os import path, getcwd, makedirs, listdir, chdir, unlink
from shutil import move
from winreg import OpenKeyEx, KEY_ALL_ACCESS, REG_SZ, \
    CloseKey, SetValue, HKEY_CLASSES_ROOT, CreateKey, \
    DeleteKey, ConnectRegistry, KEY_READ

import extensions as exts

main_folder = "GCecretary"
extensions = exts.get_all()

folders_name = [
    "Music",
    "Images",
    "Videos",
    "Documents",
    "Zippers",
    "Programs",
    "Others"
]
folder_exceptions = [
    "C:/",
    "C:/Windows",
    "C:/Windows/System32",
    "C:/Program Files",
    "C:/Program Files (x86)",
    "C:/Users",
    f"C:/Users/{getuser()}",
    f"C:/Users/{getuser()}/Desktop"
]


def create_root_key():
    try:
        new_key = OpenKeyEx(HKEY_CLASSES_ROOT, "Directory/Background/shell", 0, KEY_ALL_ACCESS)
        key = CreateKey(new_key, r"gcecretary")
        SetValue(key, "", REG_SZ, "Organize with GCecretary")
        sub_key = CreateKey(key, r"command")
        SetValue(sub_key, "", REG_SZ, path.join(path.curdir, "gcecretary.exe"))
        CloseKey(new_key)
        CloseKey(key)
        CloseKey(sub_key)
    except Exception as syserror:
        print(f"\nOps! While we tried to process your order, the next error happened:\n[!!!] - {syserror}")


def delete_root_key(value=None, key=r"gcecretary"):
    reg_connector = ConnectRegistry(None, HKEY_CLASSES_ROOT)
    reg_key = OpenKeyEx(reg_connector, 'Directory/Background/shell', 0, KEY_READ)
    with reg_key:
        try:
            if value is None:
                DeleteKey(reg_key, key)
                CloseKey(reg_key)
            unlink(path.join("C:", "Program Files", "PowFu - File Organizer"))
        except WindowsError as we:
            print(f"Something went wrong!\n{we}")


def create_extdir(_ext_found: list):
    for ext in _ext_found:
        if exts.is_music(ext):
            makedirs(folders_name[0], exist_ok=True)
        elif exts.is_image(ext):
            makedirs(folders_name[1], exist_ok=True)
        elif exts.is_video(ext):
            makedirs(folders_name[2], exist_ok=True)
        elif exts.is_doc(ext):
            makedirs(folders_name[3], exist_ok=True)
        elif exts.is_compacted(ext):
            makedirs(folders_name[4], exist_ok=True)
        elif exts.is_executable(ext):
            makedirs(folders_name[5], exist_ok=True)
        else:
            makedirs(folders_name[6], exist_ok=True)


def create_mainfolder():
    """
        This is the function that creates a new main folder
        if the script was never ran in the context folder.

        If the script has already ran into this folder or there are no files except "the program",
        it will inform the user that there are no files to organize.
    """
    msg = "All good.."
    totalfiles = 0
    current_path = getcwd()
    extensions_found = []

    if current_path not in folder_exceptions:
        for i in listdir(current_path):
            if path.isfile(i):
                if exts.get_exts(i) not in extensions_found:
                    extensions_found.append(exts.get_exts(i))
                totalfiles += 1
        if totalfiles > 0:
            makedirs(main_folder, exist_ok=True)
            chdir(path.join(current_path, main_folder))
            create_extdir(extensions_found)
        else:
            msg = "[!!!] - No files to organize!"
    else:
        msg = "[!!!] - Access denied - You can not organize this folder!"
    return msg


def move_files(_file: str, _destination: str):
    """
    This is the function that move the files into their apropriate folder.
    It also replaces duplicated files.

    :param _file: The file to be copied as a string type.
    :param _destination: The name of the folder where the file must be copied, as string.

    - Return: This function does not return any value.
    """

    msg = create_mainfolder()
    destin = path.join(getcwd(), main_folder, _destination)
    source = path.join(getcwd(), _file)

    if _file in listdir(destin):
        msg = f"The file {_file} already exists in the destination folder!\nPassing..."
        pass
    else:
        move(source, destin)
    return msg
