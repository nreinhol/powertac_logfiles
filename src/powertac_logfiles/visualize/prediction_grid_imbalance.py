import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from powertac_logfiles import data, visualize


def db_visualize_imbalance_prediction(combine_game_ids):
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)
    # fig.suptitle("Imbalance", fontsize=16)

    ax1 = fig.add_subplot(111)
    df_balancing_report = data.load_balance_report()
    df_balancing_report.rename(columns={'timeslotIndex': 'timeslot'}, inplace=True)
    df_imbalance_prediction = data.load_grid_imbalance_prediction()

    ax1.set_title("Grid imbalance prediction")
    ax1 = sns.lineplot(x="target_timeslot", y="prediction", hue='proximity', data=df_imbalance_prediction)
    ax1 = sns.lineplot(x="timeslot", y="netImbalance", data=df_balancing_report, label='grid imbalance', color='#e8483b')


    ax1.xaxis.grid(True)  # Show the vertical gridlines

    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('prediction_grid_imbalance', 'db', combine_game_ids))
    print("Successfully created imbalance prediction plot.")

