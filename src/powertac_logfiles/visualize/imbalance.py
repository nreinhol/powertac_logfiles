import matplotlib.pyplot as plt
from powertac_logfiles import data
from powertac_logfiles import visualize
import os
import pandas as pd
import seaborn as sns

def visualize_imbalance():
    for file_name in os.listdir(data.PROCESSED_DATA_PATH):
        if not file_name.find('ImbalanceCost') == -1:
            df_imbalance = pd.read_csv(data.PROCESSED_DATA_PATH + file_name, sep=';', decimal=',')

            fig = plt.figure(figsize=(12, 15))
            # fig.suptitle("Imbalance", fontsize=16)
            ax1 = fig.add_subplot(311)
            ax1.set_title("Net Demand")
            ax1 = sns.lineplot(x="timeslot", y="netDemand", hue="broker", data=df_imbalance)
            ax2 = fig.add_subplot(312)
            ax2.set_title("Imbalance")
            ax2 = sns.lineplot(x="timeslot", y="imbalance", hue="broker", data=df_imbalance)
            ax3 = fig.add_subplot(313)
            ax3.set_title("Imbalance Cost")
            ax1 = sns.lineplot(x="timeslot", y="imbalanceCost", hue="broker", data=df_imbalance)
            fig.tight_layout()
            plt.savefig('{}/{}_imbalance'.format(data.OUTPUT_DIR, visualize.grep_game_name(file_name)))
            print("Successfully created imbalance cost plot.")


def visualize_total_costs():
    for file_name in os.listdir(data.PROCESSED_DATA_PATH):
        if not file_name.find('Costs') == -1:
            df_costs = pd.read_csv(data.PROCESSED_DATA_PATH + file_name, sep=';', decimal=',', skiprows=1)
            # df_costs_shares = df_costs.drop('broker-name', 1).convert_objects(convert_numeric=True).apply(lambda x: x/x.sum())
            df_costs_transformed = df_costs.melt(id_vars=['broker-name'], var_name='cost', value_name='value')
            df_costs_transformed['value'] = pd.to_numeric(df_costs_transformed['value'])
            fig = plt.figure()
            ax = sns.barplot(x="cost", y="value", hue="broker-name", data=df_costs_transformed)
            fig.tight_layout()
            plt.savefig('{}/{}_costs'.format(data.OUTPUT_DIR, visualize.grep_game_name(file_name)))
            print("Successfully created costs plot.")
