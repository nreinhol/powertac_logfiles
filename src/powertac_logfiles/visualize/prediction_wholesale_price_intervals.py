import matplotlib.pyplot as plt
import seaborn as sns

from powertac_logfiles import visualize
import ewiis3DatabaseConnector as data


def db_visualize_wholesale_price_intervals(game_id):
    df_wholesale_price_intervals = data.load_predictions('wholesale_price_intervals', game_id)
    df_wholesale_price_intervals = df_wholesale_price_intervals.melt(id_vars=['priceIntervalId', 'game_id', 'segment_type', 'segment_type_value'], var_name='price')


    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_PORTRAIT)
    # fig.suptitle("Imbalance", fontsize=16)
    ax1 = fig.add_subplot(211)
    ax1.set_title("Wholesale price intervals dependent on proximity")
    df_wholesale_price_intervals_proximity = df_wholesale_price_intervals[df_wholesale_price_intervals['segment_type'] == 'time_delta']
    ax1 = sns.lineplot(ax=ax1, x="segment_type_value", y="value", hue='price', data=df_wholesale_price_intervals_proximity)

    ax2 = fig.add_subplot(212)
    ax2.set_title("Wholesale price intervals dependent on slotInDay")
    df_wholesale_price_intervals_slotInDay = df_wholesale_price_intervals[df_wholesale_price_intervals['segment_type'] == 'slotInDay']
    ax2 = sns.lineplot(ax=ax2, x="segment_type_value", y="value", hue='price', data=df_wholesale_price_intervals_slotInDay)
    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('prediction_wholesale_price_intervals', 'db', game_id, subfolder='prediction'))
    print("Successfully created wholesale price interval prediction plot.")
