import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from powertac_logfiles import data, visualize
import ewiis3DatabaseConnector as db


def visualize_cleared_trades(combine_game_ids=''):
    files_to_consider = visualize.get_relevant_file_paths('MktPriceStats', combine_game_ids)
    time_deltas = [str(i) for i in range(0, 24)]

    if combine_game_ids == '':
        for file_name in files_to_consider:
            df_cleared_trades_transformed = create_dataframe_for_single_mktPriceStats(file_name, time_deltas)
            game_id, iteration = visualize.get_game_id_from_logfile_name(file_name)
            plot_cleared_trades(df_cleared_trades_transformed, time_deltas, game_id + iteration)
    else:
        results = []

        for file_name in files_to_consider:
            print('consider MktPriceStats: {}'.format(file_name))
            results.append(create_dataframe_for_single_mktPriceStats(file_name, time_deltas))

        df_plot_cleared_trades_combined = pd.concat(results, ignore_index=True)
        # plot_cleared_trades(df_plot_cleared_trades_combined, time_deltas, combine_game_ids, show_outliers=True)
        plot_cleared_trades(df_plot_cleared_trades_combined, time_deltas, combine_game_ids, show_outliers=False)


def plot_cleared_trades(df_cleared_trades_transformed, time_deltas, game_suffix, show_outliers=False):

    outliers = "_show_outliers" if show_outliers else ""

    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)

    ax1 = fig.add_subplot(211)
    ax1.set_title("Cleared price dependent on proximity")
    ax1 = sns.boxplot(ax=ax1, x="time_delta", y="mkt_price", data=df_cleared_trades_transformed, order=time_deltas, showfliers=show_outliers)

    ax2 = fig.add_subplot(212)
    ax2.set_title("Cleared quantity dependent on proximity")
    ax2 = sns.boxplot(ax=ax2, x="time_delta", y="mkt_qty_MWh", data=df_cleared_trades_transformed, order=time_deltas, showfliers=show_outliers)

    fig.tight_layout()

    plt.savefig(visualize.create_path_for_plot('cleared_trades', 'time_delta{}'.format(outliers), game_suffix, subfolder='cleared_trades'))
    print("Successfully created market price and quantity timedelta boxplot plot.")


    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)

    ax1 = fig.add_subplot(211)
    ax1.set_title("Cleared price dependent on hour of the day")
    ax1 = sns.boxplot(ax=ax1, x="hour_of_day", y="mkt_price", data=df_cleared_trades_transformed, order=[i for i in range(0, 24)], showfliers=show_outliers)

    ax2 = fig.add_subplot(212)
    ax2.set_title("Cleared quantity dependent on hour of the day")
    ax2 = sns.boxplot(ax=ax2, x="hour_of_day", y="mkt_qty_MWh", data=df_cleared_trades_transformed, order=[i for i in range(0, 24)], showfliers=show_outliers)

    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('cleared_trades', 'hour_of_day{}'.format(outliers), game_suffix, subfolder='cleared_trades'))

    print("Successfully created market price and quantity hour of day boxplot plot.")

    df_cleared_trades_transformed['time_delta'] = pd.to_numeric(df_cleared_trades_transformed['time_delta'])
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)

    ax1 = fig.add_subplot(211)
    ax1.set_title("Cleared Trade dependent on hour of the day")
    ax1 = sns.scatterplot(ax=ax1, x="mkt_price", y="mkt_qty_MWh", hue='hour_of_day', palette="ch:r=-.2,d=.3_r",
                    data=df_cleared_trades_transformed, s=visualize.MARKER_SIZE_OF_SCATTERPLOT)
    ax2 = fig.add_subplot(212)
    ax2.set_title("Cleared Trade dependent on proximity")
    ax2 = sns.scatterplot(ax=ax2, x="mkt_price", y="mkt_qty_MWh", hue='time_delta', palette="ch:r=-.2,d=.3_r",
                    data=df_cleared_trades_transformed, s=visualize.MARKER_SIZE_OF_SCATTERPLOT)
    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('cleared_trades', '', game_suffix, subfolder='cleared_trades'))
    print("Successfully created cleared trade plot.")


def create_dataframe_for_single_mktPriceStats(file_name, time_deltas):
    df_cleared_trades = pd.read_csv(data.PROCESSED_DATA_PATH + file_name, sep=';', decimal=',', header=None)
    column_names = ['timeslot', 'day_of_week', 'hour_of_day']
    column_names.extend(time_deltas)
    df_cleared_trades.columns = column_names
    df_cleared_trades_transformed = df_cleared_trades.melt(id_vars=['timeslot', 'day_of_week', 'hour_of_day'],
                                                           var_name='time_delta', value_name='mkt_qty_and_price')
    df_cleared_trades_transformed['mkt_price'] = df_cleared_trades_transformed['mkt_qty_and_price'].apply(
        lambda x: x[x.find(' '):].replace(']', '').replace(',', '.').strip())
    df_cleared_trades_transformed['mkt_qty_MWh'] = df_cleared_trades_transformed['mkt_qty_and_price'].apply(
        lambda x: x[:x.find(' ')].replace('[', '').replace(',', '.').strip())
    df_cleared_trades_transformed['mkt_price'] = pd.to_numeric(df_cleared_trades_transformed['mkt_price'])
    df_cleared_trades_transformed['mkt_qty_MWh'] = pd.to_numeric(df_cleared_trades_transformed['mkt_qty_MWh'])
    df_cleared_trades_transformed['timeslot'] = pd.to_numeric(df_cleared_trades_transformed['timeslot'])
    df_cleared_trades_transformed['day_of_week'] = pd.to_numeric(df_cleared_trades_transformed['day_of_week'])
    df_cleared_trades_transformed['hour_of_day'] = pd.to_numeric(df_cleared_trades_transformed['hour_of_day'])
    df_cleared_trades_transformed = df_cleared_trades_transformed.drop('mkt_qty_and_price', 1)
    return df_cleared_trades_transformed


def visualize_cleared_trades_from_database():
    df_cleared_trades = db.load_cleared_trades()

    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)

    ax1 = fig.add_subplot(111)
    sns.scatterplot(ax=ax1, x="executionPrice", y="executionMWh",
                    data=df_cleared_trades, s=visualize.MARKER_SIZE_OF_SCATTERPLOT)

    fig.tight_layout()
    plt.savefig('{}/cleared_trades/cleared_trades'.format(data.OUTPUT_DIR))
    print("Successfully created cleared trade plot.")