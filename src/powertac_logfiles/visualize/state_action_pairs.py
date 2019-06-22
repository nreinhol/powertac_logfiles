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
    # ax.hlines([7, 14, 21], *ax.get_xlim())
    ax.hlines([4, 8, 12], *ax.get_xlim())
    plt.xlabel('actions')
    plt.ylabel('states')
    plt.savefig(visualize.create_path_for_plot('state-action_value_function', 'prod', 'Q_Learning'), bbox_inches="tight")
    print("Successfully created state-action_value_function plot.")


def create_plot_Q_visit(data_visit):
    sns.set(font_scale=3)
    sns.set_style(style='white')
    fig = plt.figure(figsize=(40, 30))
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
    data = [[0,0,0,0,0],[0,0,0,0,0],[0,464,0,197,0],[2540,-1212,0,0,-9039],[0,0,0,0,0],[0,0,0,0,0],[52,-15074,-7413,5654,-8260],[-849,-9342,7044,0,-1469],[0,0,0,0,0],[855,0,0,0,0],[1598,0,0,0,-7994],[-4991,4788,-4237,0,-9023],[11,0,0,0,0],[842,0,-23828,3415,-16517],[-3107,0,-31686,9439,-8782],[22780,0,-15846,0,3761]]
    data_visit = [[0,0,0,0,0],[0,0,0,0,0],[0,2,0,1,0],[5,13,0,0,4],[0,0,0,0,0],[0,0,0,0,0],[1,5,4,11,2],[35,30,24,0,17],[0,0,0,0,0],[1,0,0,0,0],[3,0,0,0,2],[6,3,8,0,2],[1,0,0,0,0],[3,0,5,9,4],[42,0,20,32,24],[388,0,84,0,99]]
    return data, data_visit


if __name__ == '__main__':
    data, data_visit = create_data()
    create_plot_Q(data)
    create_plot_Q_visit(data_visit)
