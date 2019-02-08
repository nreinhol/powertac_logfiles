import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from powertac_logfiles import data, visualize


def visualize_tariff_mkt_share(combine_game_ids):
    files_to_consider = visualize.get_relevant_file_paths('TariffMktShare', combine_game_ids)

    if combine_game_ids == '':
        for file_name in files_to_consider:
            df_tariffMktShare = create_dataframe_for_single_tariffMktShare(file_name)
            game_id, iteration = visualize.get_game_id_from_logfile_name(file_name)
            plot_tariff_mkt_share(df_tariffMktShare, game_id+iteration)
    else:
        results = []

        for file_name in files_to_consider:
            print('consider tariffMktShare: {}'.format(file_name))
            results.append(create_dataframe_for_single_tariffMktShare(file_name))

        df_plot_tariffMktShare_combined = pd.concat(results, ignore_index=True)
        plot_tariff_mkt_share(df_plot_tariffMktShare_combined, combine_game_ids)


def plot_tariff_mkt_share(df_tariff_mkt_share_transformed, game_suffix):
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)
    ax = sns.lineplot(x="ts", y="tariff_subscriptions", hue="broker", data=df_tariff_mkt_share_transformed)
    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('TariffMktShare', '', game_suffix))
    print("Successfully created tariff market share plot.")


def create_dataframe_for_single_tariffMktShare(file_name):
    df_tariff_mkt_share = pd.read_csv(data.PROCESSED_DATA_PATH + file_name, sep=';', decimal=',')
    df_tariff_mkt_share = df_tariff_mkt_share.drop(['total'], 1)
    df_tariff_mkt_share_transformed = df_tariff_mkt_share.melt(id_vars=['ts'], var_name='broker',
                                                               value_name='tariff_subscriptions')
    return df_tariff_mkt_share_transformed
