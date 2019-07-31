import numpy as np; np.random.seed(0)
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from powertac_logfiles import visualize


def create_plot_Q(data):
    sns.set(font_scale=3)
    sns.set_style(style='white')
    fig = plt.figure(figsize=(40, 20))
    ax1 = fig.add_subplot(111)
    # ax1.set_title("Q(s,a): The State-Action Value Function")
    ax = sns.heatmap(data, cmap="YlGnBu", annot=True, fmt="d")
    # ax.hlines([7, 14, 21], *ax.get_xlim())
    ax.hlines([4, 8, 12], *ax.get_xlim())
    plt.xlabel('Actions')
    plt.ylabel('States')
    plt.savefig(visualize.create_path_for_plot('state-action_value_function', 'prod', 'Q_Learning'), bbox_inches="tight")
    print("Successfully created state-action_value_function plot.")


def create_plot_Q_visit(data_visit):
    sns.set(font_scale=3)
    sns.set_style(style='white')
    fig = plt.figure(figsize=(40, 20))
    ax1 = fig.add_subplot(111)
    # ax1.set_title("(s,a) visits")
    ax = sns.heatmap(data_visit, cmap="YlGnBu", annot=True, fmt="d")
    # ax.hlines([7, 14, 21], *ax.get_xlim())
    ax.hlines([4, 8, 12], *ax.get_xlim())
    plt.xlabel('Actions')
    plt.ylabel('States')
    plt.savefig(visualize.create_path_for_plot('state-action_visits', 'prod', 'Q_Learning'), bbox_inches="tight")
    print("Successfully created state-action_visits plot.")


def create_data():
    data = [[0,0,0,0,0],[1970,0,0,0,-26],[38607,1725,0,956,207],[55081,23238,0,0,11502],[137,323,158,114,0],[5792,0,0,284,-36],[-14396,574,-6800,21238,0],[85787,15232,28503,0,7943],[0,0,0,0,0],[2929,0,0,659,0],[2184,0,0,0,0],[-19946,331,21111,0,1028],[-237,0,107,0,0],[11662,0,1821,586,0],[3056,0,2534,9474,-5977],[2471,0,6579,0,4216]]
    data_visit = [[0,0,0,0,0],[2,0,0,0,1],[18,2,0,3,2],[56,16,0,0,9],[2,1,1,1,0],[8,0,0,1,1],[8,7,5,14,0],[65,59,21,0,9],[0,0,0,0,0],[2,0,0,1,0],[1,0,0,0,0],[7,1,5,0,1],[1,0,1,0,0],[19,0,2,2,0],[4,0,2,17,6],[133,0,15,0,26]]
    return data, data_visit


if __name__ == '__main__':
    data, data_visit = create_data()
    create_plot_Q(data)
    create_plot_Q_visit(data_visit)
