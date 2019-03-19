import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from powertac_logfiles import data, visualize


def db_visualize_customer_prosumption_prediction(combine_game_ids):
    df_customer_prosumption = data.load_customer_prosumption()
    df_customer_prosumption.rename(columns={'postedTimeslotIndex': 'timeslot'}, inplace=True)
    df_customer_prosumption_prediction = data.load_customer_prosumption_prediction()

    if df_customer_prosumption.empty or df_customer_prosumption_prediction.empty:
        print('Can not create customer prosumption plot because prediction data or prosumption data is missing in database.')
        return

    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)
    # fig.suptitle("Imbalance", fontsize=16)

    ax1 = fig.add_subplot(111)



    ax1.set_title("Customer prosumption prediction")
    ax1 = sns.lineplot(x="target_timeslot", y="prediction", hue='proximity', data=df_customer_prosumption_prediction)
    ax1 = sns.lineplot(x="timeslot", y="SUM(kWH)", data=df_customer_prosumption, label='Prosumption', color='#e8483b')


    ax1.xaxis.grid(True)  # Show the vertical gridlines

    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('prediction_customer_prosumption', 'db', combine_game_ids))
    print("Successfully created customer prosumption prediction plot.")

