import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

from powertac_logfiles import data, visualize


def db_visualize_imbalance_prediction(combine_game_ids):
    df_balancing_report = data.load_balance_report()
    df_balancing_report = df_balancing_report[df_balancing_report['gameId'] == "game_1"]
    df_balancing_report.rename(columns={'timeslotIndex': 'timeslot'}, inplace=True)
    df_imbalance_prediction = data.load_grid_imbalance_prediction()

    if df_balancing_report.empty or df_imbalance_prediction.empty:
        print('Can not create grid imbalance prediction_performance plot because prediction data or balance report data is missing in database.')
        return

    df_imbalance_prediction['actual'] = df_imbalance_prediction.apply(
        lambda row: get_actual_value(row, df_balancing_report), axis=1)

    plot_prediction(df_balancing_report, df_imbalance_prediction, combine_game_ids)

    df_imbalance_prediction = calculate_prediction_performance(df_imbalance_prediction)
    plot_prediction_performance(combine_game_ids, df_imbalance_prediction, show_outliers=False)
    plot_prediction_performance(combine_game_ids, df_imbalance_prediction, show_outliers=True)


def calculate_prediction_performance(df_imbalance_prediction):
    df_imbalance_prediction['imb_direction_true'] = df_imbalance_prediction.apply(lambda row: correctly_classified(row),
                                                                                  axis=1)
    df_grouped = df_imbalance_prediction[['proximity', 'imb_direction_true', 'prediction']].groupby(
        by=['proximity', 'imb_direction_true'], as_index=False).count()
    df_grouped.rename(columns={'prediction': 'correct_classified'}, inplace=True)
    ae, se, rse, ape = visualize.calculate_all_error_measures(y_true=df_imbalance_prediction['actual'],
                                                              y_pred=df_imbalance_prediction['prediction'])
    df_imbalance_prediction['ae'] = ae
    df_imbalance_prediction['se'] = se
    df_imbalance_prediction['rse'] = rse
    df_imbalance_prediction['ape'] = ape
    return df_imbalance_prediction


def plot_prediction_performance(combine_game_ids, df_imbalance_prediction, show_outliers=False):
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_PORTRAIT)
    # fig.suptitle("Imbalance", fontsize=16)
    ax2 = fig.add_subplot(511)
    ax2.set_title("Absolut error of grid imbalance SARIMAX Prediction")
    ax2 = sns.boxplot(ax=ax2, x="proximity", y="ae", data=df_imbalance_prediction[['proximity', 'ae']],
                      showfliers=show_outliers)
    ax3 = fig.add_subplot(512)
    ax3.set_title("Squared error of grid imbalance SARIMAX Prediction")
    ax3 = sns.boxplot(ax=ax3, x="proximity", y="se", data=df_imbalance_prediction[['proximity', 'se']],
                      showfliers=show_outliers)
    ax4 = fig.add_subplot(513)
    ax4.set_title("Root squared error of grid imbalance SARIMAX Prediction")
    ax4 = sns.boxplot(ax=ax4, x="proximity", y="rse", data=df_imbalance_prediction[['proximity', 'rse']],
                      showfliers=show_outliers)
    ax5 = fig.add_subplot(514)
    ax5.set_title("Absolut percentage error of grid imbalance SARIMAX Prediction")
    ax5 = sns.boxplot(ax=ax5, x="proximity", y="ape", data=df_imbalance_prediction[['proximity', 'ape']],
                      showfliers=show_outliers)
    ax6 = fig.add_subplot(515)
    ax6.set_title("Right imbalance direction of grid imbalance SARIMAX Prediction")
    ax6 = sns.countplot(ax=ax6, x="proximity", hue='imb_direction_true',
                        data=df_imbalance_prediction[['proximity', 'imb_direction_true']])
    fig.tight_layout()

    outliers = "_show_outliers" if show_outliers else ""

    plt.savefig(visualize.create_path_for_plot('prediction_grid_imbalance_performance{}'.format(outliers), 'db', combine_game_ids))
    print("Successfully created imbalance prediction performance plot.")


def plot_prediction(df_balancing_report, df_imbalance_prediction, combine_game_ids):
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE_LARGE)
    # fig.suptitle("Imbalance", fontsize=16)
    ax1 = fig.add_subplot(111)
    ax1.set_title("Grid imbalance prediction")
    palette = sns.color_palette("Blues_d", n_colors=24)
    ax1 = sns.lineplot(ax=ax1, x="target_timeslot", y="prediction", hue='proximity', data=df_imbalance_prediction, palette=palette)
    ax1 = sns.lineplot(ax=ax1, x="timeslot", y="netImbalance", data=df_balancing_report, label='grid imbalance',
                       color='#e8483b')
    ax1 = sns.lineplot(ax=ax1, x="x", y="y", data=pd.DataFrame({'x': [360, 1800], 'y': [0, 0]}), color='black') # x axis
    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('prediction_grid_imbalance', 'db', combine_game_ids))
    print("Successfully created imbalance prediction plot.")


def get_actual_value(row, df_balancing_report):
    df_br_ts = df_balancing_report[df_balancing_report['timeslot'] == row['target_timeslot']]
    if not df_br_ts.empty:
        return df_br_ts['netImbalance'].values[0]
    else:
        return None


def correctly_classified(row):
    return np.sign(row['prediction']) == np.sign(row['actual'])
