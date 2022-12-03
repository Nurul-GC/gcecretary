"""
This a utility script to help users organize their files easily.
It goes through a folder and check all the files and organize them per type.
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


def move_files(_destination: str):
    extensions_found = []
    for file in listdir(_destination):
        if path.isfile(file):
            if exts.get_exts(file) not in extensions_found:
                extensions_found.append(exts.get_exts(file))
        makedirs(path.join(_destination, main_folder), exist_ok=True)
        create_extdir(extensions_found)

        if exts.is_music(file):
            move(f"{_destination}/{file}", f"{_destination}/{main_folder}/{folders_name[0]}")
        if exts.is_image(file):
            move(f"{_destination}/{file}", f"{_destination}/{main_folder}/{folders_name[1]}")
        if exts.is_video(file):
            move(f"{_destination}/{file}", f"{_destination}/{main_folder}/{folders_name[2]}")
        if exts.is_doc(file):
            move(f"{_destination}/{file}", f"{_destination}/{main_folder}/{folders_name[3]}")
        if exts.is_compacted(file):
            move(f"{_destination}/{file}", f"{_destination}/{main_folder}/{folders_name[4]}")
        if exts.is_executable(file):
            move(f"{_destination}/{file}", f"{_destination}/{main_folder}/{folders_name[5]}")
        else:
            move(f"{_destination}/{file}", f"{_destination}/{main_folder}/{folders_name[6]}")
