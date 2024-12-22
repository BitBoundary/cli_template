#!/usr/bin/env python3
"""
Template demonstrating various argparse features.

Run with -h or --help to see all options.
"""
import argparse
import os
import pathlib


def file(path: str) -> pathlib.Path:
    if not os.path.exists(path):
        raise ValueError(f"Expected file, doesn't exist: '{path}'")

    if not os.path.isfile(path):
        raise ValueError(f"Expected file, received non-file: '{path}'")

    # We could also just return the string as-is.
    return pathlib.Path(path)


def directory(path: str) -> pathlib.Path:
    if not os.path.exists(path):
        raise ValueError(f"Expected directory, doesn't exist: '{path}'")

    if not os.path.isdir(path):
        raise ValueError(f"Expected directory, received non-directory: '{path}'")

    return pathlib.Path(path)


def setup_parser():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )



    ### Required positional argument
    parser.add_argument(
        'source_directory',
        type=directory,
        help='This directory will be scanned recursively',
    )

    # python main.py
    # error: the following arguments are required: source_directory

    # python main.py my_source_directory
    # pargs.source_directory 'my_source_directory'

    # python validators.py nonexistent
    # error: argument source_directory: invalid directory value: 'nonexistent'



    ### Required variable positional with default
    parser.add_argument(
        'files',
        # This `file` function is applied to each argument string individually.
        type=file,
        nargs='+',
        help='One or more files to process',
    )
    # We could also specify `type=pathlib.Path`, but then our argument parser
    # wouldn't validate that it's specifically a file or specifically a directory.

    # python validators.py my_source_directory nonexistent.txt
    # error: argument files: invalid file value: 'nonexistent.txt'

    # python validators.py my_source_directory main.py validators.py
    # pargs.files [PosixPath('main.py'), PosixPath('validators.py')]

    # `PosixPath` represents file paths on Unix-like systems (Linux, MacOS, etc) 
    # and Windows. It handles path structures such as "/home/user/docs"
    # and "C:\Users\name\Downloads" in a consistent way across operating systems.

    pargs = parser.parse_args()
    return pargs


def main():
    pargs = setup_parser()

    print(f"Received arguments: {vars(pargs)}")
    # python validators.py . main.py 
    # Received arguments: {'source_directory': PosixPath('.'), 'files': [PosixPath('main.py')]}


if __name__ == '__main__':
    main()

