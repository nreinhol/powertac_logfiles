import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

from powertac_logfiles import visualize
import ewiis3DatabaseConnector as data


def db_visualize_grid_imbalance_prediction(game_id):
    df_balancing_report = data.load_balance_report(game_id)
    df_balancing_report.rename(columns={'timeslotIndex': 'timeslot'}, inplace=True)
    df_imbalance_prediction = data.load_predictions('prediction', game_id, 'grid', 'imbalance')

    if df_balancing_report.empty or df_imbalance_prediction.empty:
        print('Can not create grid imbalance prediction_performance plot because prediction data or balance report data is missing in database.')
        return

    df_imbalance_prediction['actual'] = df_imbalance_prediction.apply(
        lambda row: get_actual_value(row, df_balancing_report), axis=1)

    df_imbalance_prediction.rename(columns={'proximity': 'Proximity'}, inplace=True)
    plot_prediction(df_balancing_report, df_imbalance_prediction, game_id)
    visualize.evaluate_prediction(game_id, df_imbalance_prediction, 'grid_imbalance')


def plot_prediction(df_balancing_report, df_imbalance_prediction, game_id):
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE_THIN)

    start = 1000
    end = 1336
    df_imbalance_prediction = df_imbalance_prediction[df_imbalance_prediction['target_timeslot'] >= start]
    df_balancing_report = df_balancing_report[df_balancing_report['timeslot'] >= start]
    df_imbalance_prediction = df_imbalance_prediction[df_imbalance_prediction['target_timeslot'] < end]
    df_balancing_report = df_balancing_report[df_balancing_report['timeslot'] < end]

    max_timeslot = max(df_imbalance_prediction['target_timeslot'])
    min_timeslot = min(df_imbalance_prediction['target_timeslot'])
    # fig.suptitle("Imbalance", fontsize=16)
    ax1 = fig.add_subplot(111)
    # ax1.set_title("Grid imbalance prediction")
    palette = sns.color_palette("Blues_d", n_colors=24)
    ax1 = sns.lineplot(ax=ax1, x="target_timeslot", y="prediction", hue='Proximity', data=df_imbalance_prediction, palette=palette)
    ax1 = sns.lineplot(ax=ax1, x="timeslot", y="netImbalance", data=df_balancing_report, label='Actual Grid Imbalance',
                       color='#e8483b')
    ax1 = sns.lineplot(ax=ax1, x="timeslot", y="imbalance", data=pd.DataFrame({'timeslot': [min_timeslot, max_timeslot], 'imbalance': [0, 0]}), color='black') # x axis
    ax1.set_ylabel('Imbalance')
    ax1.set_xlabel('Timeslot')
    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('prediction_grid_imbalance', 'db', game_id, subfolder='prediction'))
    print("Successfully created imbalance prediction plot.")


def get_actual_value(row, df_balancing_report):
    df_br_ts = df_balancing_report[df_balancing_report['timeslot'] == row['target_timeslot']]
    if not df_br_ts.empty:
        return df_br_ts['netImbalance'].values[0]
    else:
        return None
