import click as c
import datetime

from powertac_logfiles import build as b


def write_source_info(index, url):
    c.secho('\n◼', fg='blue')
    c.secho('├── ', nl=False)
    c.secho('[{} of {}]'.format(index, len(b.GAME_NUMBERS)), fg='green')
    c.secho('├── ', nl=False)
    c.secho('source: ', fg='green', nl=False)
    c.secho('{}'.format(url), nl=False)
    c.secho('  size: ', fg='green', nl=False)


def write_intro():
    c.secho('\nPowerTAC log-files', bold=True, underline=True)
    c.secho('number of games: {}'.format(len(b.GAME_NUMBERS)))
    c.secho('executed: {}'.format(datetime.datetime.now()))
