import matplotlib.pyplot as plt
from powertac_logfiles import data
from powertac_logfiles import visualize
import os
import pandas as pd
import seaborn as sns

def visualize_imbalance(combine_game_ids=None):
    '''visualize the imbalance from data of a processed state file'''
    if combine_game_ids == None:
        visualize_imbalance_for_single_game()
    else:
        visualize_imbalance_of_tournament(combine_game_ids)



def visualize_imbalance_of_tournament(combine_game_ids):
    # find relavant files
    files_to_consider = []
    for file_name in os.listdir(data.PROCESSED_DATA_PATH):
        if file_name.find('ImbalanceCost') > -1 and file_name.find(combine_game_ids) > -1:
            files_to_consider.append(file_name)
    results = []
    for file in files_to_consider:
        print('consider imbalance cost files: {}'.format(file))
        results.append(pd.read_csv(data.PROCESSED_DATA_PATH + file, sep=';', decimal=','))
    df_for_imbalance_plot = pd.concat(results, ignore_index=True)
    plot_imbalance(df_for_imbalance_plot, files_to_consider[0])


def visualize_imbalance_for_single_game():
    for file_name in os.listdir(data.PROCESSED_DATA_PATH):
        if not file_name.find('ImbalanceCost') == -1:
            df_imbalance = pd.read_csv(data.PROCESSED_DATA_PATH + file_name, sep=';', decimal=',')

            plot_imbalance(df_imbalance, file_name)


def plot_imbalance(df_imbalance, file_name):
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
    ax3 = sns.lineplot(x="timeslot", y="imbalanceCost", hue="broker", data=df_imbalance)
    fig.tight_layout()
    plt.savefig('{}/{}_imbalance'.format(data.OUTPUT_DIR, visualize.grep_game_name(file_name)))
    print("Successfully created imbalance cost plot.")


def visualize_total_costs():
    '''visualize the imbalance costs from data of a processed state file.'''
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


def plot_imbalance_histogram():
    df_balance_report = data.load_balance_report()
    fig = plt.figure(figsize=(12, 15))
    ax1 = fig.add_subplot(211)
    ax1.set_title("netImbalance")
    ax1 = sns.lineplot(x="timeslotIndex", y="netImbalance", data=df_balance_report)
    ax2 = fig.add_subplot(212)
    ax2.set_title("netImbalance")
    g = sns.distplot(df_balance_report['netImbalance'], bins=100, color='#14779b')
    fig.tight_layout()
    plt.savefig('{}/imbalance/imbalance'.format(data.OUTPUT_DIR))
    print("Successfully created imbalance plot.")


def plot_balancing_transactions():
    df_balancing_transactions = data.load_balancing_transactions()
    fig = plt.figure(figsize=(12, 15))
    # fig.suptitle("Imbalance", fontsize=16)
    ax1 = fig.add_subplot(211)
    ax1.set_title("kWh")
    ax1 = sns.lineplot(x="postedTimeslot", y="kWh", data=df_balancing_transactions)
    ax2 = fig.add_subplot(212)
    ax2.set_title("Charge")
    ax2 = sns.lineplot(x="postedTimeslot", y="charge", data=df_balancing_transactions)
    fig.tight_layout()
    plt.savefig('{}/imbalance/balancing_transactions'.format(data.OUTPUT_DIR))
    print("Successfully created balancing transaction plot.")