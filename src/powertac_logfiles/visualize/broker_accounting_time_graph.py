import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from powertac_logfiles import data, visualize


def visualize_broker_accounting_time_graph(combine_game_ids=None):
    files_to_consider = visualize.get_relevant_file_paths('BrokerAccounting', combine_game_ids)
    for file_name in files_to_consider:
        df_broker_accounting = create_dataframe_for_single_brokeraccounting(file_name)
        game_id, iteration = visualize.get_game_id_from_logfile_name(file_name)
        plot(game_id + iteration, df_broker_accounting)


def create_dataframe_for_single_brokeraccounting(file_name):
    df_broker_accounting = pd.read_csv(data.PROCESSED_DATA_PATH + file_name, sep=';', decimal='.')
    return df_broker_accounting

def plot(game_id, df):
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE_THIN)

    ax1 = fig.add_subplot(111)
    ax1 = sns.lineplot(ax=ax1, x="ts", y="cash", hue='broker', data=df)
    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('BrokerAccountings_ingame_development', '', game_id, subfolder='general'))
    print("Successfully created broker accounting time graph plot.")