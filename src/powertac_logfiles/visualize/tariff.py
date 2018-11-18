import matplotlib.pyplot as plt
from powertac_logfiles import data
from powertac_logfiles import visualize
import os
import pandas as pd
import seaborn as sns


def plot_tariff_market_share():
    for file_name in os.listdir(data.PROCESSED_DATA_PATH):
        if not file_name.find('TariffMktShare') == -1:
            df_tariff_mkt_share = pd.read_csv(data.PROCESSED_DATA_PATH + file_name, sep=';', decimal=',')
            df_tariff_mkt_share = df_tariff_mkt_share.drop(['total'], 1)
            df_tariff_mkt_share_transformed = df_tariff_mkt_share.melt(id_vars=['ts'], var_name='broker', value_name='tariff_subscriptions')

            fig = plt.figure()
            ax = sns.lineplot(x="ts", y="tariff_subscriptions", hue="broker", data=df_tariff_mkt_share_transformed)
            fig.tight_layout()
            plt.savefig('{}/{}_tariff_market_share'.format(data.OUTPUT_DIR, visualize.grep_game_name(file_name)))
            print("Successfully created tariff market share plot.")

if __name__ == '__main__':
    plot_tariff_market_share()