import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from powertac_logfiles import data, visualize


def visualize_total_costs(combine_game_ids):
    '''visualize the total costs from data of a processed state file.'''
    files_to_consider = visualize.get_relevant_file_paths('BrokerCosts', combine_game_ids)

    if combine_game_ids == '':
        for file_name in files_to_consider:
            df_costs = pd.read_csv(data.PROCESSED_DATA_PATH + file_name, sep=';', decimal=',', skiprows=1)
            game_id, iteration = visualize.get_game_id_from_logfile_name(file_name)
            plot_total_costs(df_costs, game_id + iteration)
    else:
        results = []
        for file in files_to_consider:
            print('consider imbalance cost files: {}'.format(file))
            results.append(pd.read_csv(data.PROCESSED_DATA_PATH + file, sep=';', decimal=',', skiprows=1))
        df_for_total_costs_plot = pd.concat(results, ignore_index=True)
        plot_total_costs(df_for_total_costs_plot, combine_game_ids)


def plot_total_costs(df_costs, game_suffix):
    df_costs_transformed = df_costs.melt(id_vars=['broker-name'], var_name='cost', value_name='value')
    df_costs_transformed['value'] = pd.to_numeric(df_costs_transformed['value'])
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)
    ax1 = fig.add_subplot(111)
    # ax = sns.barplot(x="cost", y="value", hue="broker-name", data=df_costs_transformed)
    g = sns.swarmplot(ax=ax1, x="cost", y="value", hue='broker-name', data=df_costs_transformed, size=12)
    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('total_costs', '', game_suffix))
    print("Successfully created total costs plot.")
