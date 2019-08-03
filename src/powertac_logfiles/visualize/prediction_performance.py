import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

from powertac_logfiles import visualize
import ewiis3DatabaseConnector as data


def evaluate_prediction(game_id, df_prediction, type):
    df_prediction = calculate_prediction_performance(df_prediction)
    df_accuracy =  calculate_accuracy(df_prediction)
    plot_prediction_performance(game_id, df_prediction, df_accuracy, type, show_outliers=False)
    # plot_prediction_performance(game_id, df_prediction, show_outliers=True)


def calculate_prediction_performance(df_prediction):
    df_prediction['Correct sign'] = df_prediction.apply(lambda row: correctly_classified(row), axis=1)
    ae, se, rse, ape = visualize.calculate_all_error_measures(y_true=df_prediction['actual'],
                                                              y_pred=df_prediction['prediction'])
    df_prediction['mae'] = ae
    df_prediction['mse'] = se
    df_prediction['rmse'] = rse
    df_prediction['mape'] = ape
    return df_prediction


def plot_prediction_performance(game_id, df_prediction, df_accuracy, type, show_outliers=False):

    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)
    # fig.suptitle("Imbalance", fontsize=16)
    ax2 = fig.add_subplot(411)
    ax2.set_title("Absolut Error")
    ax2 = sns.boxplot(ax=ax2, x="Proximity", y="mae", data=df_prediction[['Proximity', 'mae']],
                      showfliers=show_outliers)
    ax2.set_ylabel("Value")

    ax3 = fig.add_subplot(412)
    ax3.set_title("Squared Error")
    ax3 = sns.boxplot(ax=ax3, x="Proximity", y="mse", data=df_prediction[['Proximity', 'mse']],
                      showfliers=show_outliers)
    ax3.set_ylabel("Value")

    """ax4 = fig.add_subplot(413)
    ax4.set_title("Root Mean Squared Error")
    ax4 = sns.boxplot(ax=ax4, x="Proximity", y="rmse", data=df_prediction[['Proximity', 'rmse']],
                      showfliers=show_outliers)"""

    ax5 = fig.add_subplot(413)
    ax5.set_title("Absolut Percentage Error")
    ax5 = sns.boxplot(ax=ax5, x="Proximity", y="mape", data=df_prediction[['Proximity', 'mape']],
                      showfliers=show_outliers)
    ax5.set_ylabel("Value")

    ax6 = fig.add_subplot(414)
    ax6.set_title("Accuracy of Sign")
    ax6 = sns.lineplot(ax=ax6, x="Proximity", y="accuracy", data=df_accuracy)
    ax6.set_ylabel("Value")

    fig.tight_layout()

    outliers = "_show_outliers" if show_outliers else ""

    plt.savefig(visualize.create_path_for_plot('prediction_performance_{}_{}'.format(type, outliers), 'db', game_id, subfolder='prediction'))
    print("Successfully created {} prediction performance plot.".format(type))
    # calculate_accuracy(df_prediction)


def correctly_classified(row):
    return np.sign(row['prediction']) == np.sign(row['actual'])


def calculate_accuracy(df_prediction):
    df_accuracy = df_prediction.groupby(['Proximity', 'Correct sign']).size().reset_index(name='counts')
    # print(df_accuracy)
    df_number_of_total_predictions = df_prediction.groupby(['Proximity']).size().reset_index(name='counts')
    # print(df_number_of_total_predictions)
    df_accuracy = df_accuracy[df_accuracy['Correct sign']].reset_index()
    df_accuracy['accuracy'] = df_accuracy['counts'] / df_number_of_total_predictions['counts']
    return df_accuracy
