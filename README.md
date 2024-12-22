# cli_template

Cleanly organized template for a command-line Python script

## Sample Output

```bash
$ python main.py -h
usage: main.py [-h] [--files [FILES ...]] [--required-files REQUIRED_FILES [REQUIRED_FILES ...]] [-v] [-m {auto,manual}] [-s SIZE] source [optional_destination]

Template demonstrating common argparse features.

Run with -h or --help to see all options, i.e.:

    python main.py -h

positional arguments:
  source                Required positional argument (default: None)
  optional_destination  Optional positional argument with default (default: default_value).

options:
  -h, --help            show this help message and exit
  --files [FILES ...]   Zero or more arguments (default: [])
  --required-files REQUIRED_FILES [REQUIRED_FILES ...]
                        One or more arguments (default: None)
  -v, --verbose         Flag argument (default: False)
  -m {auto,manual}, --mode {auto,manual}
                        Choice argument (default: auto)
  -s SIZE, --size SIZE  Size argument (e.g., 500KB, 1.5MB) (default: 1MB)
```

```bash
$ python validators.py -h
usage: validators.py [-h] source_directory files [files ...]

Template demonstrating various argparse features. Run with -h or --help to see all options.

positional arguments:
  source_directory  This directory will be scanned recursively
  files             One or more files to process

options:
  -h, --help        show this help message and exit
```
