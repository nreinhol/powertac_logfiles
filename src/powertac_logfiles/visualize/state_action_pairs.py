import numpy as np; np.random.seed(0)
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from powertac_logfiles import visualize


def create_plot_Q(data):
    sns.set(font_scale=3)
    sns.set_style(style='white')
    fig = plt.figure(figsize=(40, 30))
    ax1 = fig.add_subplot(111)
    ax1.set_title("Q(s,a): The State-Action Value Function")
    ax = sns.heatmap(data, cmap="YlGnBu", annot=True, fmt="d")
    plt.xlabel('actions')
    plt.ylabel('states')
    plt.savefig(visualize.create_path_for_plot('state-action_value_function', '', 'sarsaLambda'), bbox_inches="tight")
    print("Successfully created state-action_value_function plot.")


def create_plot_Q_visit(data_visit):
    sns.set(font_scale=3)
    sns.set_style(style='white')
    fig = plt.figure(figsize=(40, 30))
    ax1 = fig.add_subplot(111)
    ax1.set_title("(s,a) visits")
    ax = sns.heatmap(data_visit, cmap="YlGnBu", annot=True, fmt="d")
    plt.xlabel('actions')
    plt.ylabel('states')
    plt.savefig(visualize.create_path_for_plot('state-action_visits', '', 'sarsaLambda'), bbox_inches="tight")
    print("Successfully created state-action_visits plot.")


def create_data():
    data = [[8284,0,0,11484,0],[6344,15509,0,74978,0],[33606,8489,0,76203,74435],[0,77931,0,2954,23867],[6753,7342,0,5930,0],[0,18623,0,0,0],[0,0,0,43120,0],[31822,54598,173986,81531,28741],[128740,101630,116596,52807,61650],[89021,106858,130029,116343,38586],[253349,81908,97540,77599,112456],[62240,82456,60326,0,77316],[31701,0,0,0,0],[2014,25398,0,0,0],[0,0,0,0,0],[30001,0,0,16790,0],[0,0,0,32929,0],[10347,19275,31769,0,36590],[11688,0,11034,0,0],[0,0,1888,0,2173],[14521,0,0,18849,1520],[16943,0,0,11920,12969],[1277,0,0,14126,7313],[1875,0,4019,0,12549]]
    data_visit = [[1,0,0,1,0],[1,1,0,5,0],[3,1,0,5,5],[0,4,0,1,2],[2,1,0,2,0],[0,4,0,0,0],[0,0,0,2,0],[2,2,12,4,2],[14,7,7,4,3],[9,8,15,9,2],[31,7,9,9,9],[6,10,7,0,9],[2,0,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[2,0,0,1,0],[0,0,0,2,0],[1,2,3,0,2],[3,0,2,0,0],[0,0,1,0,1],[2,0,0,3,1],[5,0,0,3,3],[1,0,0,7,2],[1,0,2,0,7]]
    return data, data_visit


if __name__ == '__main__':
    data, data_visit = create_data()
    create_plot_Q(data)
    create_plot_Q_visit(data_visit)
