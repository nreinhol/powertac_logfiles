import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from powertac_logfiles import data, visualize


def visualize_tariff_mkt_share(combine_game_ids):
    files_to_consider_ts = visualize.get_relevant_file_paths('TariffMktShare', combine_game_ids)
    results = []

    for file_name in files_to_consider_ts:
        print('consider tariffMktShare: {}'.format(file_name))
        results.append(create_dataframe_for_single_tariffMktShare(file_name))

    df_plot_tariffMktShare_combined = pd.concat(results, ignore_index=True)
    plot_tariff_mkt_share(df_plot_tariffMktShare_combined, combine_game_ids)


def plot_tariff_mkt_share(df_tariff_mkt_share_transformed, game_suffix):
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_PORTRAIT)

    ax1 = fig.add_subplot(311)
    ax1.set_title("Tariff Market Share (all powerTypes)")
    ax1 = sns.lineplot(ax=ax1, x="ts", y="tariff_subscriptions", hue="broker", data=df_tariff_mkt_share_transformed)

    df_subs_powertype = create_df_for_powerType_shares(game_suffix)
    ax2 = fig.add_subplot(312)
    ax2.set_title("Subscriptions to powerTypes (EWIIS3)")
    ax2 = sns.lineplot(x="postedTimeslotIndex", y="currentSubscribedPopulation", hue="powerType", data=df_subs_powertype)

    ax3 = fig.add_subplot(313)
    ax3.set_title("Market Shares of powerTypes (EWIIS3)")
    ax3 = sns.lineplot(x="postedTimeslotIndex", y="mkt_share", hue="powerType", data=df_subs_powertype)

    ax1.xaxis.grid(True)  # Show the vertical gridlines
    ax2.xaxis.grid(True)  # Show the vertical gridlines
    ax3.xaxis.grid(True)  # Show the vertical gridlines

    ax1.legend(markerscale=visualize.MARKER_SCALE)
    ax2.legend(markerscale=visualize.MARKER_SCALE)
    ax3.legend(markerscale=visualize.MARKER_SCALE)

    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('TariffMktShare', '', game_suffix, subfolder='tariffs'))
    print("Successfully created tariff market share plot.")


def create_dataframe_for_single_tariffMktShare(file_name):
    df_tariff_mkt_share = pd.read_csv(data.PROCESSED_DATA_PATH + file_name, sep=';', decimal=',')
    df_tariff_mkt_share = df_tariff_mkt_share.drop(['total'], 1)
    df_tariff_mkt_share_transformed = df_tariff_mkt_share.melt(id_vars=['ts'], var_name='broker',
                                                               value_name='tariff_subscriptions')
    return df_tariff_mkt_share_transformed


def create_df_for_powerType_shares(combine_game_ids):
    files_to_consider_cs = visualize.get_relevant_file_paths('CustomerStats', combine_game_ids)
    results = []
    for file in files_to_consider_cs:
        print('consider customer stats files: {}'.format(file))
        results.append(visualize.parse_customer_stats_file(file))
    df_for_customer_stats_plot = pd.concat(results, ignore_index=True).rename(
        columns={'size': 'populationSize', 'game_id': 'gameId'})

    df_tariff_subscriptions = data.load_tariff_transactions()
    df_tariff_subscriptions = df_tariff_subscriptions[df_tariff_subscriptions['txType'].isin(['CONSUME', 'PRODUCE'])]
    df_subs_powertype = df_tariff_subscriptions[
        ['currentSubscribedPopulation', 'gameId', 'customerName', 'postedTimeslotIndex', 'txType',
         'powerType']].groupby(by=['postedTimeslotIndex', 'powerType', 'customerName', 'gameId'], as_index=False).mean()
    df_subs_powertype = df_subs_powertype[
        ['gameId', 'postedTimeslotIndex', 'powerType', 'currentSubscribedPopulation']].groupby(
        by=['gameId', 'postedTimeslotIndex', 'powerType'], as_index=False).sum()
    df_subs_powertype = pd.merge(df_subs_powertype, df_for_customer_stats_plot, how='left', on=['gameId', 'powerType'])
    df_subs_powertype['mkt_share'] = df_subs_powertype['currentSubscribedPopulation'] / df_subs_powertype[
        'populationSize']
    return df_subs_powertype
