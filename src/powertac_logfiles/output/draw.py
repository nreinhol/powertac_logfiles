import click as c
import datetime

from powertac_logfiles import build as b


def print_download_info(index, url, size, local=True):
    c.secho('◼', fg='blue')
    c.secho('├── ', nl=False)
    c.secho('[{} of {}]'.format(index, len(b.GAME_NUMBERS)), fg='green')
    c.secho('├── ', nl=False)
    c.secho('url: ', fg='green', nl=False)
    c.secho('{}'.format(url), nl=False)
    c.secho('  size: ', fg='green', nl=False)
    c.secho('{} mb'.format(size))
    c.secho('└── ', nl=False)
    c.secho('download and extract...', fg='white', nl=False)


def print_processing_info(index, file, all_files, size):
    c.secho('◼', fg='blue')
    c.secho('├── ', nl=False)
    c.secho('[{} of {}]'.format(index, len(all_files)), fg='green')
    c.secho('├── ', nl=False)
    c.secho('file: ', fg='green', nl=False)
    c.secho('{}'.format(file), nl=False)
    c.secho('  size: ', fg='green', nl=False)
    c.secho('{} mb'.format(size))


def print_web_intro():
    c.secho('\nstart processing web log-files', fg='green')
    c.secho('└── executed: {}'.format(datetime.datetime.now()))


def print_local_intro():
    c.secho('\nstart processing local log-files', fg='green')
    c.secho('└── executed: {}'.format(datetime.datetime.now()))


def print_cli_intro():
    c.secho('\nPowerTAC log-files', fg='green', bold=True, underline=True)
    c.secho('A small cli program which build csv log-files of the PowerTAC\n', fg='green')
    c.secho('choose between option [a] and [b]')
    c.secho('├── [a]: process your local log-files')
    c.secho('└── [b]: process the final log-files from web\n')


def print_help():
    tree = """
◼
├── data		    - dir and subdirs are needed to run program succesful
│   ├── local		    - put in your custom state/trace files
│   ├── processed	    - contains the created csv-files
│   └── web		    - dir and subdirs contain the loaded web logfiles
│       ├── extracted
│       │   └── log
│       └── raw
├── env
├── powertac-tools	    - clone https://github.com/powertac/powertac-tools.git
└── src
    └── powertac_logfiles
        ├── build	    - contain type of created logfiles in __init__
        ├── cli
        ├── data	    - contain variables for web processing in __init__
        └── output
"""
    print(tree)
