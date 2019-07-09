import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from powertac_logfiles import visualize
import ewiis3DatabaseConnector as data


def db_visualize_customer_prosumption_prediction(game_id):
    df_customer_prosumption = data.load_customer_prosumption(game_id)
    df_customer_prosumption.rename(columns={'postedTimeslotIndex': 'timeslot'}, inplace=True)
    df_customer_prosumption_prediction = data.load_predictions('prediction', game_id, 'customer', 'prosumption')

    if df_customer_prosumption.empty or df_customer_prosumption_prediction.empty:
        print('Can not create customer prosumption plot because prediction data or prosumption data is missing in database.')
        return

    df_customer_prosumption_prediction['actual'] = df_customer_prosumption_prediction.apply(
        lambda row: get_actual_value(row, df_customer_prosumption), axis=1)

    df_customer_prosumption_prediction.rename(columns={'proximity': 'Proximity'}, inplace=True)
    plot_prediction(df_customer_prosumption, df_customer_prosumption_prediction, game_id)
    visualize.evaluate_prediction(game_id, df_customer_prosumption_prediction, 'customer_demand')


def plot_prediction(df_customer_prosumption, df_customer_prosumption_prediction, game_id):
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE_LARGE)
    # fig.suptitle("Imbalance", fontsize=16)
    ax1 = fig.add_subplot(111)
    # ax1.set_title("Customer prosumption prediction")
    palette = sns.color_palette("Blues_d", n_colors=24)
    ax1 = sns.lineplot(ax=ax1, x="target_timeslot", y="prediction", hue='Proximity',
                       data=df_customer_prosumption_prediction, palette=palette)
    ax1 = sns.lineplot(x="timeslot", y="SUM(kWH)", data=df_customer_prosumption, label='Actual Customer Demand', color='#e8483b')
    ax1.xaxis.grid(True)  # Show the vertical gridlines
    ax1.set_ylabel('Customer Demand')
    ax1.set_xlabel('Timeslot')
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
