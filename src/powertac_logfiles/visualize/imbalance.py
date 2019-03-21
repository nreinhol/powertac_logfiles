import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from powertac_logfiles import data, visualize


def visualize_imbalance(combine_game_ids):
    '''visualize the imbalance from data of a processed state file'''
    files_to_consider = visualize.get_relevant_file_paths('BrokerImbalanceCost', combine_game_ids)

    if combine_game_ids == '':
        for file_name in files_to_consider:
            df_imbalance = pd.read_csv(data.PROCESSED_DATA_PATH + file_name, sep=';', decimal=',')
            game_id, iteration = visualize.get_game_id_from_logfile_name(file_name)
            plot_imbalance(df_imbalance, game_id + iteration)
    else:
        results = []

        for file in files_to_consider:
            print('consider imbalance cost files: {}'.format(file))
            results.append(pd.read_csv(data.PROCESSED_DATA_PATH + file, sep=';', decimal=','))

        df_for_imbalance_plot = pd.concat(results, ignore_index=True)
        plot_imbalance(df_for_imbalance_plot, combine_game_ids)


def plot_imbalance(df_imbalance, game_suffix):
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_PORTRAIT)
    # fig.suptitle("Imbalance", fontsize=16)

    ax1 = fig.add_subplot(411)
    ax1.set_title("Imbalance")
    ax1 = sns.lineplot(x="timeslot", y="imbalance", hue="broker", data=df_imbalance)
    ax1.xaxis.grid(True)  # Show the vertical gridlines

    ax2 = fig.add_subplot(412)
    ax2.set_title("Imbalance Cost")
    ax2 = sns.lineplot(x="timeslot", y="imbalanceCost", hue="broker", data=df_imbalance)
    ax2.xaxis.grid(True)  # Show the vertical gridlines

    ax3 = fig.add_subplot(413)
    df_balancing_report = data.load_balance_report()
    df_balancing_report.rename(columns={'timeslotIndex': 'timeslot'}, inplace=True)

    ax3.set_title("Imbalance of total grid")
    ax3 = sns.lineplot(x="timeslot", y="netImbalance", data=df_balancing_report)
    ax3.xaxis.grid(True)  # Show the vertical gridlines

    ax4 = fig.add_subplot(414)
    df_balancing_transactions = data.load_balancing_transactions()
    df_balancing_transactions.rename(columns={'postedTimeslot': 'timeslot'}, inplace=True)

    ax4.set_title("Balancing Transactions of EWIIS3")
    sns.lineplot(ax=ax4, x="timeslot", y="kWh", data=df_balancing_transactions)
    ax41 = ax4.twinx()
    sns.lineplot(ax=ax41, x="timeslot", y="charge", data=df_balancing_transactions, color='orange')

    ax4.xaxis.grid(True)  # Show the vertical gridlines

    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('imbalance', 'logfileAndDb', game_suffix, subfolder='imbalance'))
    print("Successfully created imbalance cost plot.")


def plot_imbalance_database(combine_game_ids):
    df_balance_report = data.load_balance_report()

    if df_balance_report.empty:
        print('ERROR: no imbalance data for any game stored in db.')

    if combine_game_ids == '':  # don't combine results, plot results for each single game_id
        for game_id in list(df_balance_report['gameId'].unique()):
            df_balance_report_for_game = df_balance_report[
                df_balance_report['gameId'] == game_id]
            plot_imbalance_histogram(df_balance_report_for_game, game_id)
    else:
        plot_imbalance_histogram(df_balance_report, combine_game_ids)


def plot_imbalance_histogram(df_balance_report, game_suffix):
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)

    ax1 = fig.add_subplot(311)
    ax1.set_title("netImbalance")
    ax1 = sns.lineplot(x="timeslotIndex", y="netImbalance", data=df_balance_report)

    ax2 = fig.add_subplot(312)
    ax2.set_title("netImbalance")
    g = sns.distplot(df_balance_report['netImbalance'], bins=100, color='#14779b')

    ax3 = fig.add_subplot(313)
    ax3.set_title("netImbalance")
    g = sns.boxplot(x=df_balance_report['netImbalance'])

    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('grid_imbalance', 'db', game_suffix, subfolder='imbalance'))
    print("Successfully created imbalance plot.")


def plot_balancing_transactions():
    df_balancing_transactions = data.load_balancing_transactions()
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)

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
