# src/utils/path_utils.py

import os

def get_current_directory():
    return os.getcwd()

def list_directory_contents(path='.'):
    try:
        return os.listdir(path)
    except FileNotFoundError:
        return []

def change_directory(path):
    try:
        os.chdir(path)
        return True
    except FileNotFoundError:
        return False

def print_working_directory():
    return os.getcwd()
