import click as c
from powertac_logfiles import visualize
from powertac_logfiles.data import OUTPUT_DIR


@c.command()
@c.option("--database", default='Yes', help='Select which data source shall be used. Database or processed files.')
@c.option("--combine_game_ids", default='', help='Select which performances should be evaluated.')
def choose_option(database, combine_game_ids):
    """PowerTac log-files. A small cli program which build csv log-files of the PowerTAC """
    if not combine_game_ids == '':
        visualize.create_dir_if_not_exists('{}/{}'.format(OUTPUT_DIR, combine_game_ids))

    if database == 'Yes':
        visualize.visualize_tariff_specification(combine_game_ids)
        visualize.plot_imbalance_database(combine_game_ids)
        visualize.visualize_customer_demand(combine_game_ids)
        # visualize.visualize_cleared_trades_from_database(combine_game_ids)
        # visualize.visualize_orderbook(combine_game_ids)
        # visualize.visualize_weather(combine_game_ids)
        # visualize.plot_balancing_transactions(combine_game_ids)
        # visualize.visualize_capacity_transactions(combine_game_ids)
    else:
        visualize.visualize_total_costs(combine_game_ids)
        visualize.visualize_tariff_mkt_share(combine_game_ids)
        visualize.visualize_cleared_trades(combine_game_ids)
        visualize.visualize_imbalance(combine_game_ids)
        visualize.visualize_broker_accounting(combine_game_ids)


def main():
    choose_option()


if __name__ == '__main__':
    main()
