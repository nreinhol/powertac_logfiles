import matplotlib.pyplot as plt
import seaborn as sns

from powertac_logfiles import data
from powertac_logfiles import visualize


def db_visualize_prosumption_prediction(combine_game_ids):
    df_prosumption_prediction = data.load_prosumption_prediction()
    df_distribution_report = data.load_distribution_reports()

    if df_prosumption_prediction.empty or df_distribution_report.empty:
        print('can not create total_grid_prediction_performance plot because prediction data or distribution report data is missing in database.')

    fig = plt.figure(figsize=(15, 20))
    ax1 = fig.add_subplot(211)
    ax1.set_title("SARIMAX Prediction of total grid Consumption and Production")
    ax1 = sns.lineplot(x="target_timeslot", y="prediction", style='type', hue='proximity', data=df_prosumption_prediction)

    df_distribution_reports = data.load_distribution_reports()
    df_plot = df_distribution_reports.drop('gameId', 1).melt(id_vars=['balanceReportId', 'timeslot'], var_name='type', value_name='kWh')
    df_all_production_plot = df_plot[df_plot['type'] == 'totalProduction']
    ax1 = sns.lineplot(ax=ax1, x="timeslot", y="kWh", data=df_all_production_plot, label='total grid Customers Production', color='#e8483b')
    df_all_consumption_plot = df_plot[df_plot['type'] == 'totalConsumption']
    # df_all_consumption_plot['kWh'] = -1 * df_all_consumption_plot['kWh']
    ax1 = sns.lineplot(ax=ax1, x="timeslot", y="kWh", data=df_all_consumption_plot, label='total grid Consumption', color='#14779b')


    df_prosumption_prediction['actual'] = df_prosumption_prediction.apply(lambda row: get_actual_value(row, df_distribution_report), axis=1)
    df_prosumption_prediction['mae'] = abs(df_prosumption_prediction['actual'] - df_prosumption_prediction['prediction'])

    ax2 = fig.add_subplot(212)
    ax2.set_title("MAE of total grid SARIMAX Prediction")
    ax2 = sns.boxplot(ax=ax2, x="proximity", y="mae", hue='type', data=df_prosumption_prediction[['proximity', 'mae', 'type']])

    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('total_grid_prediction_performance', 'db', combine_game_ids))
    print("Successfully created total_grid_prediction_performance plot.")


def get_actual_value(row, df_distribution_report):
    type = 'total{}'.format(row['type'].title())
    df_dr_ts = df_distribution_report[df_distribution_report['timeslot'] == row['target_timeslot']]
    if not df_dr_ts.empty:
        return df_dr_ts[type].values[0]
    else:
        return None
