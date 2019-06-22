import pandas as pd

import ewiis3DatabaseConnector as db


class DataService():
    # raw db datasets
    df_tariff_transactions = None

    # processed db data
    df_tariff_transactions_prod_con = None

    def __init__(self):
        pass

    def load_raw_datasets(self):
        self.df_tariff_transactions = db.load_tariff_transactions()

    def process_data(self):
        self.create_tariff_transactions_prod_con()

    def load_raw_data_and_process(self):
        self.load_raw_datasets()
        self.process_data()

    def create_tariff_transactions_prod_con(self):
        allow = ['PRODUCE', 'CONSUME']
        self.df_tariff_transactions_prod_con = self.df_tariff_transactions[self.df_tariff_transactions['txType'].isin(allow)]

    def create_total_powertype_prosumption_per_gameId(self, game_id):
        if not game_id == 'all':
            df_powerType_prosumption_per_gameId = self.df_tariff_transactions_prod_con[self.df_tariff_transactions_prod_con['gameId'] == game_id]
        else:
            df_powerType_prosumption_per_gameId = self.df_tariff_transactions_prod_con
        df_powerType_prosumption_per_gameId = df_powerType_prosumption_per_gameId[['brokerName', 'kWh', 'powerType']].groupby(by=['brokerName', 'powerType'], as_index=False).sum()
        df_powerType_prosumption_per_gameId['kWh'] = abs(df_powerType_prosumption_per_gameId['kWh'])
        return df_powerType_prosumption_per_gameId

    def create_total_production_per_customer_and_gameId(self, game_id):
        if not game_id == 'all':
            df_powerType_prosumption_per_gameId = self.df_tariff_transactions_prod_con[self.df_tariff_transactions_prod_con['gameId'] == game_id]
        else:
            df_powerType_prosumption_per_gameId = self.df_tariff_transactions_prod_con
        df_powerType_prosumption_per_gameId = df_powerType_prosumption_per_gameId[
            ['brokerName', 'kWh', 'customerName']].groupby(by=['brokerName', 'customerName'],
                                                                  as_index=False).sum()
        df_powerType_prosumption_per_gameId['kWh'] = abs(df_powerType_prosumption_per_gameId['kWh'])
        df_powerType_prosumption_per_gameId = df_powerType_prosumption_per_gameId.sort_values(by=['kWh'], ascending=False)
        df_powerType_prosumption_per_gameId.reset_index(inplace=True)
        return df_powerType_prosumption_per_gameId
