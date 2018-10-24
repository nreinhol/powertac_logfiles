import click as c

from powertac_logfiles import output
from powertac_logfiles import build as b


@c.command()
@c.option("--option", prompt='option', type=c.Choice(['a', 'b', 'c']))
def choose_option(option):
    """PowerTac log-files. A small cli program which build csv log-files of the PowerTAC """

    if option == 'a':
        output.print_local_intro()
        b.make_log_files()

    elif option == 'b':
        output.print_web_intro()
        b.make_web_log_files()

    elif option == 'c':
        output.print_help()


def main():
    output.print_cli_intro()
    choose_option()


if __name__ == '__main__':
    main()
