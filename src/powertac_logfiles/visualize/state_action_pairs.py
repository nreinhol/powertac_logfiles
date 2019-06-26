import numpy as np; np.random.seed(0)
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from powertac_logfiles import visualize


def create_plot_Q(data):
    sns.set(font_scale=3)
    sns.set_style(style='white')
    fig = plt.figure(figsize=(40, 20))
    ax1 = fig.add_subplot(111)
    ax1.set_title("Q(s,a): The State-Action Value Function")
    ax = sns.heatmap(data, cmap="YlGnBu", annot=True, fmt="d")
    # ax.hlines([7, 14, 21], *ax.get_xlim())
    ax.hlines([4, 8, 12], *ax.get_xlim())
    plt.xlabel('actions')
    plt.ylabel('states')
    plt.savefig(visualize.create_path_for_plot('state-action_value_function', 'prod', 'Q_Learning'), bbox_inches="tight")
    print("Successfully created state-action_value_function plot.")


def create_plot_Q_visit(data_visit):
    sns.set(font_scale=3)
    sns.set_style(style='white')
    fig = plt.figure(figsize=(40, 20))
    ax1 = fig.add_subplot(111)
    ax1.set_title("(s,a) visits")
    ax = sns.heatmap(data_visit, cmap="YlGnBu", annot=True, fmt="d")
    # ax.hlines([7, 14, 21], *ax.get_xlim())
    ax.hlines([4, 8, 12], *ax.get_xlim())
    plt.xlabel('actions')
    plt.ylabel('states')
    plt.savefig(visualize.create_path_for_plot('state-action_visits', 'prod', 'Q_Learning'), bbox_inches="tight")
    print("Successfully created state-action_visits plot.")


def create_data():
    data = [[0,0,0,0,0],[10981,0,0,5167,-8836],[66367,13064,0,8598,207],[54002,52727,0,0,23253],[137,323,158,114,0],[8023,831,1935,284,-36],[-14396,574,-6800,77754,346],[80778,61911,50875,0,34726],[0,0,0,0,0],[2929,0,0,659,0],[2184,0,0,0,0],[-19946,331,43102,0,1028],[-237,0,107,0,0],[11572,0,2730,3756,0],[3056,0,2534,28112,-4474],[28969,0,8915,0,-3303]]
    data_visit = [[0,0,0,0,0],[16,0,0,1,2],[34,4,0,4,2],[102,24,0,0,20],[2,1,1,1,0],[13,1,1,1,1],[8,7,5,27,1],[164,68,30,0,20],[0,0,0,0,0],[2,0,0,1,0],[1,0,0,0,0],[7,1,13,0,1],[1,0,1,0,0],[23,0,3,4,0],[4,0,2,24,7],[182,0,28,0,33]]
    return data, data_visit


if __name__ == '__main__':
    data, data_visit = create_data()
    create_plot_Q(data)
    create_plot_Q_visit(data_visit)
