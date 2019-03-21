import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from powertac_logfiles import visualize, data


def visualize_customer_stats(combine_game_ids):
    files_to_consider = visualize.get_relevant_file_paths('CustomerStats', combine_game_ids)
    if combine_game_ids == '':
        for file_name in files_to_consider:
            df_customer_stats = parse_customer_stats_file(file_name)
            game_id, iteration = visualize.get_game_id_from_logfile_name(file_name)
            plot_customer_stats(df_customer_stats, game_id + iteration)
    else:
        results = []

        for file in files_to_consider:
            print('consider imbalance cost files: {}'.format(file))
            results.append(parse_customer_stats_file(file))

        df_for_customer_stats_plot = pd.concat(results, ignore_index=True)
        plot_customer_stats(df_for_customer_stats_plot, combine_game_ids)


def parse_customer_stats_file(file_name):
    df_customer_stats = pd.DataFrame()
    game_id, iteration = visualize.get_game_id_from_logfile_name(file_name)
    with open(data.PROCESSED_DATA_PATH + file_name, 'r') as file_content:
        for line in file_content:
            customer_stats = line.split(':')
            entry = {'powerType': customer_stats[0].strip(), 'size': customer_stats[1].strip()}
            df_customer_stats = df_customer_stats.append(entry, ignore_index=True)
    df_customer_stats['size'] = pd.to_numeric(df_customer_stats['size'])
    df_customer_stats['game_id'] = game_id + iteration
    return df_customer_stats


def plot_customer_stats(df_customer_stats, game_suffix):
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)

    ax1 = fig.add_subplot(111)
    g = sns.swarmplot(ax=ax1, x="powerType", y="size", data=df_customer_stats, size=visualize.MARKER_SIZE_OF_SWARMPLOT)
    g.set_xticklabels(g.get_xticklabels(), rotation=90)

    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('customer_stats', '', game_suffix, subfolder='general'))
    print("Successfully created customer stats plot.")
