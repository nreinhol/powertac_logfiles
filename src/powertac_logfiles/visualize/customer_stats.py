import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from powertac_logfiles import visualize, data


def visualize_customer_stats(combine_game_ids):
    files_to_consider = visualize.get_relevant_file_paths('CustomerStats', combine_game_ids)
    if combine_game_ids == '':
        for file_name in files_to_consider:
            df_customer_stats = __parse_customer_stats_file(file_name)
            game_id, iteration = visualize.get_game_id_from_logfile_name(file_name)
            plot_customer_stats(df_customer_stats, game_id + iteration)
    else:
        results = []

        for file in files_to_consider:
            print('consider imbalance cost files: {}'.format(file))
            results.append(__parse_customer_stats_file(file))

        df_for_customer_stats_plot = pd.concat(results, ignore_index=True)
        plot_customer_stats(df_for_customer_stats_plot, combine_game_ids)


def __parse_customer_stats_file(file_name):
    df_customer_stats = pd.DataFrame()
    with open(data.PROCESSED_DATA_PATH + file_name, 'r') as file_content:
        for line in file_content:
            customer_stats = line.split(':')
            entry = {'powerType': customer_stats[0].strip(), 'size': customer_stats[1].strip()}
            df_customer_stats = df_customer_stats.append(entry, ignore_index=True)
    df_customer_stats['size'] = pd.to_numeric(df_customer_stats['size'])
    return df_customer_stats


def plot_customer_stats(df_customer_stats, game_suffix):
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)
    ax1 = fig.add_subplot(111)
    g = sns.swarmplot(ax=ax1, x="powerType", y="size", data=df_customer_stats, size=12)
    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('customer_stats', '', game_suffix))
    print("Successfully created customer stats plot.")
