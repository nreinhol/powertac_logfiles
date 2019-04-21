import ewiis3DatabaseConnector as db


def check_predictions(all_game_ids):
    print('Check prediction data.')
    for game_id in all_game_ids:
        df_grid_imba = db.load_predictions('prediction', game_id, 'grid', 'imbalance')
        df_customer_pros = db.load_predictions('prediction', game_id, 'customer', 'prosumption')
        print('game: {} -> grid_imba: {}, customer_prosumption: {}'.format(game_id, len(df_grid_imba), len(df_customer_pros)))


def check_game_data(all_game_ids):
    print('Check game data.')
    for game_id in all_game_ids:
        df_br = db.load_balance_report(game_id)
        df_wr = db.load_weather_report(game_id)
        df_ts = db.load_tariff_subscription_shares(game_id)
        df_tt = db.load_tariff_transactions(game_id)
        print('game: {} -> balancing_report: {}, weather_report: {}, tariff shares: {}, tarif transactions: {}'.format(game_id, len(df_br), len(df_wr), len(df_ts), len(df_tt)))


def do_consistency_checks():
    all_game_ids = db.load_all_gameIds()
    check_predictions(all_game_ids)
    check_game_data(all_game_ids)


if __name__ == '__main__':
    do_consistency_checks()
