import click as c
from powertac_logfiles import visualize


@c.command()
@c.option("--logs", default='all', help='Select which performances should be evaluated.')
def choose_option(logs):
    """PowerTac log-files. A small cli program which build csv log-files of the PowerTAC """
    if logs == 'imbalance':
        visualize.visualize_imbalance()

    elif logs == 'costs':
        visualize.visualize_total_costs()

    elif logs == 'tariff':
        visualize.visualize_total_costs()

    elif logs == 'cleared_trades':
        visualize.visualize_cleared_trades()

    elif logs == 'broker_accounting':
        visualize.visualize_broker_accounting()

    elif logs == 'all':
        visualize.visualize_imbalance()
        visualize.visualize_total_costs()
        visualize.plot_tariff_market_share()
        visualize.visualize_cleared_trades()
        visualize.visualize_broker_accounting()


def main():
    choose_option()


if __name__ == '__main__':
    main()
