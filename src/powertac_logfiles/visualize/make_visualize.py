import click as c
from powertac_logfiles import visualize


@c.command()
@c.option("--combine_game_ids", default='No', help='Select which performances should be evaluated.')
def choose_option(combine_game_ids):
    """PowerTac log-files. A small cli program which build csv log-files of the PowerTAC """
    if combine_game_ids == 'No':
        visualize.visualize_imbalance()
        visualize.visualize_total_costs()
        visualize.plot_tariff_market_share()
        visualize.visualize_cleared_trades()
        visualize.visualize_broker_accounting()
    else:
        visualize.visualize_broker_accounting(combine_game_ids)

def main():
    choose_option()


if __name__ == '__main__':
    main()
