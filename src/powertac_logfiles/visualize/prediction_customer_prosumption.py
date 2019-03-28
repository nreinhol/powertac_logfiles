import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from powertac_logfiles import visualize
import ewiis3DatabaseConnector as data


def db_visualize_customer_prosumption_prediction(game_id):
    df_customer_prosumption = data.load_customer_prosumption(game_id)
    df_customer_prosumption.rename(columns={'postedTimeslotIndex': 'timeslot'}, inplace=True)
    df_customer_prosumption_prediction = data.load_predictions('customer_prosumption_prediction', game_id)

    if df_customer_prosumption.empty or df_customer_prosumption_prediction.empty:
        print('Can not create customer prosumption plot because prediction data or prosumption data is missing in database.')
        return

    df_customer_prosumption_prediction['actual'] = df_customer_prosumption_prediction.apply(
        lambda row: get_actual_value(row, df_customer_prosumption), axis=1)

    plot_prediction(df_customer_prosumption, df_customer_prosumption_prediction, game_id)

    df_customer_prosumption_prediction = calculate_prediction_performance(df_customer_prosumption_prediction)
    plot_prediction_performance(game_id, df_customer_prosumption_prediction, show_outliers=False)
    plot_prediction_performance(game_id, df_customer_prosumption_prediction, show_outliers=True)


def plot_prediction_performance(game_id, df_customer_prosumption_prediction, show_outliers=False):
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_PORTRAIT)
    # fig.suptitle("Imbalance", fontsize=16)
    ax2 = fig.add_subplot(511)
    ax2.set_title("Absolut error of SARIMAX Prediction")
    ax2 = sns.boxplot(ax=ax2, x="proximity", y="ae", data=df_customer_prosumption_prediction[['proximity', 'ae']],
                      showfliers=show_outliers)
    ax3 = fig.add_subplot(512)
    ax3.set_title("Squared error of Customer Prosumption SARIMAX Prediction")
    ax3 = sns.boxplot(ax=ax3, x="proximity", y="se", data=df_customer_prosumption_prediction[['proximity', 'se']],
                      showfliers=show_outliers)
    ax4 = fig.add_subplot(513)
    ax4.set_title("Root squared error of Customer Prosumption SARIMAX Prediction")
    ax4 = sns.boxplot(ax=ax4, x="proximity", y="rse", data=df_customer_prosumption_prediction[['proximity', 'rse']],
                      showfliers=show_outliers)
    ax5 = fig.add_subplot(514)
    ax5.set_title("Absolut percentage error of Customer Prosumption SARIMAX Prediction")
    ax5 = sns.boxplot(ax=ax5, x="proximity", y="ape", data=df_customer_prosumption_prediction[['proximity', 'ape']],
                      showfliers=show_outliers)
    ax6 = fig.add_subplot(515)
    ax6.set_title("Right imbalance direction of Customer Prosumption SARIMAX Prediction")
    ax6 = sns.countplot(ax=ax6, x="proximity", hue='imb_direction_true',
                        data=df_customer_prosumption_prediction[['proximity', 'imb_direction_true']])
    fig.tight_layout()

    outliers = "_show_outliers" if show_outliers else ""

    plt.savefig(visualize.create_path_for_plot('prediction_customer_prosumption_prediction_performance{}'.format(outliers), 'db', game_id, subfolder='prediction'))
    print("Successfully created customer prosumption prediction performance plot.")


def plot_prediction(df_customer_prosumption, df_customer_prosumption_prediction, game_id):
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE_LARGE)
    # fig.suptitle("Imbalance", fontsize=16)
    ax1 = fig.add_subplot(111)
    ax1.set_title("Customer prosumption prediction")
    palette = sns.color_palette("Blues_d", n_colors=24)
    ax1 = sns.lineplot(ax=ax1, x="target_timeslot", y="prediction", hue='proximity',
                       data=df_customer_prosumption_prediction, palette=palette)
    ax1 = sns.lineplot(x="timeslot", y="SUM(kWH)", data=df_customer_prosumption, label='Customer Prosumption', color='#e8483b')
    ax1.xaxis.grid(True)  # Show the vertical gridlines
    fig.tight_layout()
    plt.savefig(
        visualize.create_path_for_plot('prediction_customer_prosumption', 'db', game_id, subfolder='prediction'))
    print("Successfully created customer prosumption prediction plot.")


def get_actual_value(row, df_customer_prosumption):
    df_br_ts = df_customer_prosumption[df_customer_prosumption['timeslot'] == row['target_timeslot']]
    if not df_br_ts.empty:
        return df_br_ts['SUM(kWH)'].values[0]
    else:
        return None


def correctly_classified(row):
    return np.sign(row['prediction']) == np.sign(row['actual'])


def calculate_prediction_performance(df_customer_prosumption_prediction):
    df_customer_prosumption_prediction['imb_direction_true'] = df_customer_prosumption_prediction.apply(lambda row: correctly_classified(row), axis=1)
    ae, se, rse, ape = visualize.calculate_all_error_measures(y_true=df_customer_prosumption_prediction['actual'],
                                                              y_pred=df_customer_prosumption_prediction['prediction'])
    df_customer_prosumption_prediction['ae'] = ae
    df_customer_prosumption_prediction['se'] = se
    df_customer_prosumption_prediction['rse'] = rse
    df_customer_prosumption_prediction['ape'] = ape
    return df_customer_prosumption_prediction
