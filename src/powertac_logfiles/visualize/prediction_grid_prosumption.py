import matplotlib.pyplot as plt
import seaborn as sns

from powertac_logfiles import data, visualize


def db_visualize_grid_prosumption_prediction(game_id):
    df_prosumption_prediction = data.load_prosumption_prediction()
    df_distribution_report = data.load_distribution_reports()

    if df_prosumption_prediction.empty or df_distribution_report.empty:
        print('Can not create total_grid_prediction_performance plot because prediction data or distribution report data is missing in database.')
        return

    plot_prediction(df_prosumption_prediction, df_distribution_report, game_id)

    df_prosumption_prediction['actual'] = df_prosumption_prediction.apply(lambda row: get_actual_value(row, df_distribution_report), axis=1)

    df_prosumption_prediction = calculate_prediction_performance(df_prosumption_prediction)
    plot_prediction_performance(game_id, df_prosumption_prediction)
    plot_prediction_performance(game_id, df_prosumption_prediction, show_outliers=True)


def calculate_prediction_performance(df_prosumption_prediction):
    ae, se, rse, ape = visualize.calculate_all_error_measures(y_true=df_prosumption_prediction['actual'],
                                                              y_pred=df_prosumption_prediction['prediction'])
    df_prosumption_prediction['ae'] = ae
    df_prosumption_prediction['se'] = se
    df_prosumption_prediction['rse'] = rse
    df_prosumption_prediction['ape'] = ape
    return df_prosumption_prediction


def plot_prediction_performance(game_id, df_prosumption_prediction, show_outliers=False):
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_PORTRAIT)
    # fig.suptitle("Imbalance", fontsize=16)
    ax1 = fig.add_subplot(411)
    ax1.set_title("Absolut error of grid prosumption SARIMAX Prediction")
    ax1 = sns.boxplot(ax=ax1, x="proximity", y="ae", hue='type', data=df_prosumption_prediction[['proximity', 'type', 'ae']],
                      showfliers=show_outliers)

    ax2 = fig.add_subplot(412)
    ax2.set_title("Squared error of grid prosumption SARIMAX Prediction")
    ax2 = sns.boxplot(ax=ax2, x="proximity", y="se", hue='type', data=df_prosumption_prediction[['proximity', 'type', 'se']],
                      showfliers=show_outliers)

    ax3 = fig.add_subplot(413)
    ax3.set_title("Root squared error of grid prosumption SARIMAX Prediction")
    ax3 = sns.boxplot(ax=ax3, x="proximity", y="rse", hue='type', data=df_prosumption_prediction[['proximity', 'type', 'rse']],
                      showfliers=show_outliers)

    ax4 = fig.add_subplot(414)
    ax4.set_title("Absolut percentage error of grid prosumption SARIMAX Prediction")
    ax4 = sns.boxplot(ax=ax4, x="proximity", y="ape", hue='type', data=df_prosumption_prediction[['proximity', 'type', 'ape']],
                      showfliers=show_outliers)

    fig.tight_layout()

    outliers = "_show_outliers" if show_outliers else ""

    plt.savefig(visualize.create_path_for_plot('prediction_grid_prosumption_performance{}'.format(outliers), 'db', game_id, subfolder='prediction'))
    print("Successfully created grid prosumption prediction performance plot.")


def plot_prediction(df_prosumption_prediction, df_distribution_report, game_id):
    df_prediction_plot = df_prosumption_prediction[df_prosumption_prediction['type'] == 'consumption']
    df_plot = df_distribution_report.drop('gameId', 1).melt(id_vars=['balanceReportId', 'timeslot'], var_name='type', value_name='kWh')

    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE_LARGE)
    ax1 = fig.add_subplot(211)
    ax1.set_title("SARIMAX Prediction of grid Consumption and Production")
    palette = sns.color_palette("Blues_d", n_colors=24)
    ax1 = sns.lineplot(ax=ax1, x="target_timeslot", y="prediction", hue='proximity',
                       data=df_prediction_plot, palette=palette)
    ax1 = sns.lineplot(ax=ax1, x="timeslot", y="kWh", data=df_plot[df_plot['type'] == 'totalConsumption'], label='total grid Consumption', color='#14779b')

    ax2 = fig.add_subplot(212)
    ax2.set_title("SARIMAX Prediction of grid Consumption and Production")
    df_prediction_plot = df_prosumption_prediction[df_prosumption_prediction['type'] == 'production']
    ax2 = sns.lineplot(ax=ax2, x="target_timeslot", y="prediction", hue='proximity',
                       data=df_prediction_plot, palette=palette)
    ax2 = sns.lineplot(ax=ax2, x="timeslot", y="kWh", data=df_plot[df_plot['type'] == 'totalProduction'], label='total grid Consumption', color='#14779b')

    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('prediction_grid_prosumption', 'db', game_id, subfolder='prediction'))
    print("Successfully created total_grid_prediction_performance plot.")


def get_actual_value(row, df_distribution_report):
    type = 'total{}'.format(row['type'].title())
    df_dr_ts = df_distribution_report[df_distribution_report['timeslot'] == row['target_timeslot']]
    if not df_dr_ts.empty:
        return df_dr_ts[type].values[0]
    else:
        return None
