#!/usr/bin/python3

import hashlib
import os
import mimetypes
import sys


files_dict = {}
duped = []
ignored_files = [
    ".DS_Store",
    ".directory",
    "desktop.ini",
    "folder.htt",
    "no-data.txt",
    "message_1.json",
    "dovecot-uidlist",
]
ignored_dir = "@eaDir"


def fast_check(file_path, file_size) -> str:
    """
    Check files equal by names and size.
    """
    return f"{os.path.basename(file_path)}_{file_size}"


def deep_check(file_path, file_size) -> str:
    """
    Check files equal by md5 hash  and size.
    """
    hash_md5 = hashlib.md5()

    fobj = open(os.path.join(file_path), "rb")
    chunk_data = fobj.read(4096)
    fobj.close()

    hash_md5.update(chunk_data)

    return f"{hash_md5.hexdigest()}_{file_size}"


def xml_output():
    # generate xml struct
    print('<?xml version="1.0" encoding="UTF-8"?>')
    print("<root>")
    for dkey in set(duped):
        data_key = "_".join(dkey.split("_")[:-1])
        file_size = dkey.split("_")[-1]
        file_name = files_dict.get(dkey, [])[0]
        file_mime_type = mimetypes.guess_type(file_name)[0]
        print(
            f'\t<file data-key="{data_key}" mime-type="{file_mime_type}" size="{file_size}">'
        )
        for fpath in files_dict.get(dkey, []):
            print(f'\t\t<dup path="{fpath}"/>')
        print(f"\t</file>")
    print("</root>")


def main(start_path, scan_type):
    if scan_type == "deep":
        check_key_getter = deep_check
    else:
        check_key_getter = fast_check

    for path, _, files in os.walk(start_path):
        for f in files:
            if f in ignored_files:
                continue

            file_path = os.path.join(path, f)
            if ignored_dir in file_path:
                continue
            try:
                size = os.path.getsize(file_path)
            except FileNotFoundError:
                continue
            except Exception:
                raise Exception

            if size == 0:
                continue

            check_key = check_key_getter(file_path, size)
            if check_key not in files_dict:
                files_dict[check_key] = [file_path]
            else:
                files_dict[check_key].append(file_path)
                duped.append(check_key)
    xml_output()
    return


if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print(
            "Wrong number of arguments. Use: python3 dup_find.py <start_path> <scan_type>. scan_type can be 'fast' or 'deep'"
        )
