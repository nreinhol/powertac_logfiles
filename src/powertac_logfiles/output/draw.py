import click as c
import datetime

from powertac_logfiles import build as b
from powertac_logfiles import data


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


def print_processing_info(index, file, all_files):
    c.secho('◼', fg='blue')
    c.secho('├── ', nl=False)
    c.secho('[{} of {}]'.format(index, len(all_files)), fg='green')
    c.secho('├── ', nl=False)
    c.secho('file: ', fg='green', nl=False)
    c.secho('{}'.format(file))


def print_web_intro():
    c.secho('\nstart processing web log-files', fg='green')
    c.secho('└── executed: {}'.format(datetime.datetime.now()))


def print_local_intro():
    c.secho('\nstart processing local log-files', fg='green')
    c.secho('└── executed: {}'.format(datetime.datetime.now()))


def print_cli_intro():
    print_intro_header()
    c.secho('A small cli program which build csv log-files of the PowerTAC\n', fg='green')
    c.secho('choose between option [a] and [b]')
    c.secho('├── [a]: process your local log-files')
    c.secho('├── [b]: process the final log-files from web')
    c.secho('└── [c]: show info\n')


def print_no_file_found():
    c.secho('\nNo file found in data dir!', fg='red', bold=True)
    c.secho('For processing local files put state/trace files into:')
    c.secho('└──' + data.LOCAL_LOG_DATA_PATH)


def print_intro_header():
    img = """
    ____                         ______              __            _____ __    
   / __ \____ _      _____  ____/_  __/___ ______   / /___  ____ _/ __(_) /__  _____
  / /_/ / __ \ | /| / / _ \/ ___// / / __ `/ ___/  / / __ \/ __ `/ /_/ / / _ \/ ___/
 / ____/ /_/ / |/ |/ /  __/ /   / / / /_/ / /__   / / /_/ / /_/ / __/ / /  __(__  ) 
/_/    \____/|__/|__/\___/_/   /_/  \__,_/\___/  /_/\____/\__, /_/ /_/_/\___/____/  
                                                         /____/                                                                              
"""
    c.secho(img, bold=True, fg='green')


def print_help():
    print_help_header()
    print_help_info()
    img = """
.
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
    c.secho(img)


def print_help_header():
    img = """                  
    _       ____    
   (_)___  / __/___ 
  / / __ \/ /_/ __ \\
 / / / / / __/ /_/ /
/_/_/ /_/_/  \____/ 
                                  
"""
    c.secho(img, bold=True, fg='green')


def print_help_info():
    c.secho('◼ Game numbers of final games: {}.'.format(b.GAME_NUMBERS))
    c.secho('◼ Download url: {}{}{}{}'.format(data.URL, data.FILE_NAME_, '<number>', data.FILE_TYPE))
    c.secho('◼ Processing create following log types:')
    for key, value in b.LOG_FILES.items():
        c.secho('  - ' + key)

def print_end():
    img = """
    _____       _      __  
   / __(_)___  (_)____/ /_ 
  / /_/ / __ \/ / ___/ __ \\
 / __/ / / / / (__  ) / / /
/_/ /_/_/ /_/_/____/_/ /_/ 
                           
    """
    c.secho(img, fg='green')
