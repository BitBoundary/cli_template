#!/usr/bin/env python3
"""
Template demonstrating common argparse features.

Run with -h or --help to see all options, i.e.:

    python main.py -h
"""
import argparse
from typing import Optional, Literal


# This is the data structure that our information parsed from
# the command line will follow. This gives us autocomplete in
# IDEs and text editors.
class FileProcessorNamespace:
    source: str
    optional_destination: Optional[str]
    files: Optional[list[str]]
    required_files: Optional[list[str]]
    verbose: bool
    mode: Literal['auto'] | Literal['manual']
    size: int


def setup_parser() -> type[FileProcessorNamespace]:
    # `__doc__` refers to the multi-line comment at the top of this file.
    parser = argparse.ArgumentParser(
        description=__doc__,

        # * RawDescriptionHelpFormatter: Help messages for individual arguments
        #   will be pretty-formatted on multiple lines with added indentation.
        # * RawTextHelpFormatter: Help text for each argument is treated as a long
        #   string that wraps around the screen without added indentation.

        # I picked RawDescriptionHelpFormatter because it looks nice to me.
        # Feel free to experiment and see which you prefer.
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )



    ### Required positional argument
    parser.add_argument(
        'source',
        help='Required positional argument (default: %(default)s)',
    )

    ## Following are example calls and outputs to the program.
    # `pargs` is `parsed arguments`, the object that contains the results of
    # parsing the command-line arguments.

    # python main.py
    # error: the following arguments are required: source

    # python main.py my_source_directory
    # pargs.source 'my_source_directory'



    ### Optional positional with default
    parser.add_argument(
        'optional_destination',
        nargs='?',  # Makes argument optional; '?' means "zero or one"
        default='default_value',
        help='Optional positional argument with default (default: %(default)s).',
    )

    # python main.py my_source_directory
    # pargs.optional_destination 'default_value'

    # python main.py my_source_directory my_destination_directory
    # pargs.optional_destination 'my_destination_directory'



    ### Optional positional, no default
    # Don't use this at the same time as "Optional positional with default"
    # above, otherwise the parser won't be able to tell which option is which.
    # parser.add_argument(
    #     'optional_destination',
    #     nargs='?',  # Makes argument optional; '?' means "zero or one"
    #     help='Optional positional argument with default (default: %(default)s)',
    # )

    # python main.py my_source_directory
    # pargs.optional_destination None

    # python main.py my_source_directory my_destination_directory
    # pargs.optional_destination 'my_destination_directory'



    ### Any number of arguments, also known as "Zero or more arguments" (*)
    parser.add_argument(
        '--files',
        nargs='*',

        # no default set
        # python main.py my_source_directory
        # pargs.files None

        default=[],
        # python main.py my_source_directory
        # pargs.files []

        # default=['a', 'b', 'c'],
        # python main.py my_source_directory
        # pargs.files ['a', 'b', 'c']

        help='Zero or more arguments (default: %(default)s)',
    )

    # python main.py my_source_directory
    # pargs.files []

    # python main.py my_source_directory --files a.txt b.txt c.txt
    # pargs.files ['a.txt', 'b.txt', 'c.txt']



    ### One or more arguments (+)
    parser.add_argument(
        '--required-files',
        nargs='+',
        help='One or more arguments (default: %(default)s)',
    )
    # `nargs='+'` means "one or more", and the result will be a list that
    # contains at least one value.

    # python main.py my_source_directory --required-files
    # error: argument --required-files: expected at least one argument

    # python main.py my_source_directory --required-files a.txt
    # pargs.required_files ['a.txt']

    # python main.py my_source_directory --required-files a.txt b.txt c.txt
    # pargs.required_files ['a.txt', 'b.txt', 'c.txt']



    ### On/off settings (also known as "Flags")
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Flag argument (default: %(default)s)',
    )

    # python main.py my_source_directory
    # pargs.verbose False

    # python main.py my_source_directory -v
    # pargs.verbose True

    # python main.py my_source_directory --verbose
    # pargs.verbose True



    ### Choice from predefined options
    parser.add_argument(
        '-m',
        '--mode',
        choices=['auto', 'manual'],
        default='auto',
        help='Choice argument (default: %(default)s)',
    )

    # python main.py my_source_directory --mode manual
    # error: argument -m/--mode: invalid choice: 'm' (choose from 'auto', 'manual')

    # python main.py my_source_directory --mode manual
    # pargs.mode 'manual'



    ### Custom type conversion
    # See validators.py for more
    # Commonly used values for `type` include int, float.
    parser.add_argument(
        '-s',
        '--size',
        type=parse_size,  # see the definition of parse_size below
        default='1MB',
        help='Size argument (e.g., 500KB, 1.5MB) (default: %(default)s)',
    )

    # python main.py --size invalid
    # error: argument -s/--size: invalid parse_size value: 'invalid'

    # python main.py --size 5g
    # error: argument -s/--size: invalid parse_size value: '5g'
    # `parse_size` could be enhanced with more flexibility to support inputs
    # such as `5g` and `8m`, but programming is always a balance between
    # flexibility/convenience, and stability / bug reduction.

    # python main.py my_source_directory --size 500KB
    # pargs.size 512000


    # `namespace=FileProcessorNamespace` tells our linter and IDE the data and data types
    # that the result will contain; for example, we can type `pargs.req` and then hit
    # tab-tab and it will autocomplete `pargs.required_files`
    pargs = parser.parse_args(namespace=FileProcessorNamespace)

    return pargs


## While this example converts a human-friendly value such as "5MB" to an integer
## number of bytes, we could write a function which takes any string-based
## command-line argument and validate it (for example checking if a file with the
## given path exists), and even optionally transform the value into something else.
## For example, we could make it convert a string file/directory path into an
## actual python pathlib.Path object.
def parse_size(size_str: str) -> int:
    """Convert strings such as '5MB' or '10GB' to number of bytes"""
    units: dict[str, int] = {'B': 1, 'KB': 1024, 'MB': 1024*1024, 'GB': 1024*1024*1024}
    size: float = float(size_str[:-2].strip())
    unit = size_str[-2:].upper()
    return int(size * units[unit])


def main():
    # This is named `pargs` instead of `args` because `args` tends
    # to be a reserved word, for example in command-line debuggers.
    pargs: type[FileProcessorNamespace] = setup_parser()

    # Now that we have received the arguments from the user, we can
    # start doing our program logic.
    
    # Normally we'd access arguments directly such as `pargs.source`, but
    # this allows us to iterate through all of the arguments dynamically,
    # even if new ones are added.
    from pprint import pprint
    pprint({k: v for k, v in pargs.__dict__.items() if not k.startswith('_')})

    # python main.py . some_destination --files main.py validators.py --mode manual -v
    # {'files': ['main.py', 'validators.py'],
    #  'mode': 'manual',
    #  'optional_destination': 'some_destination',
    #  'required_files': None,
    #  'size': 1048576,
    #  'source': '.',
    #  'verbose': True}

if __name__ == '__main__':
    main()

