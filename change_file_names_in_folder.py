#!/usr/bin/env python3
import os
import sys
from pathlib import Path


def get_count_files_in_folder():
    return len([name for name in os.listdir('.') if os.path.isfile(name)])


def get_digit_count(number):
    count = 0
    while number > 0:
        number = number // 10
        count += 1
    return count


def get_list_files_in_folder():
    path = os.getcwd()
    temp_list = []
    with os.scandir(path) as listOfEntries:
        for entry in listOfEntries:
            if entry.is_file() and entry.name.endswith(""):
                if entry.name != Path(sys.modules['__main__'].__file__).name:
                    temp_list.append(entry.name)
    return temp_list


RENM_PATH = os.getcwd()
BASE_NAME = os.path.basename(RENM_PATH)
BASE_FCNT = get_count_files_in_folder()
FMT = get_digit_count(BASE_FCNT)


def main():
    i = 0
    for old_file_name in get_list_files_in_folder():
        i += 1
        file_ext = os.path.splitext(old_file_name)[1]
        file_source = RENM_PATH + os.sep + old_file_name
        file_dest = RENM_PATH + os.sep + BASE_NAME + '-' + str(i).zfill(FMT) + file_ext
        os.rename(file_source, file_dest)
    print('Done!!!')


if __name__ == "__main__":
    sval = input('Are You Shore ?: [Y/y,N,n]')
    if sval.upper() == 'Y':
        main()
