import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns


def draw_graph(G, with_labels=False, font_size=30, connection_style=0.1, node_colors=None, edge_colors=None, savefig=False, file_format='pdf', ax=None):
      
    pos = nx.circular_layout(G, center=[0, 0], scale=1)
    rotate90 = np.array([[0, 1],
                         [-1, 0]])

    pos = {k: np.array([1, 1]) * (v @ rotate90) for k, v in pos.items()}
    if not node_colors:
        colors = {k: sns.color_palette()[i] for i, k in enumerate(pos.keys())}
    else:
        colors = {k: node_colors[i] for i, k in enumerate(pos.keys())}

    if not edge_colors:
        edge_colors_list = None
    else:
        edge_colors_list = []
        for edge, color in edge_colors.items():
            if type(color) == np.ndarray or type(color) == tuple or type(color) == list:
                edge_colors_list.append(color)
            else:
                edge_colors_list.append(np.array([0, 0, 0, color], dtype=float))

    edge_weights = {k: np.exp(1*np.abs(v)) for k, v in nx.get_edge_attributes(G,'weight').items()}
    edge_styles = {k: '--' if v < 0 else '-' for k, v in nx.get_edge_attributes(G,'weight').items()}

    if ax:
        ax = ax
    else:
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))

    #fig = plt.figure(1)
    nx.draw(G, 
            ax=ax,
            with_labels=with_labels, 
            pos=pos, 
            node_size=4000, 
            node_color=list(colors.values()),
            font_size=font_size,
            font_family='Times New Roman',
            connectionstyle=f"arc3,rad={connection_style}",
            arrowstyle="-|>, head_length=1.8, head_width=0.6",
            width=list(edge_weights.values()),
            style=list(edge_styles.values()),
            edge_color=edge_colors_list)


    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    plt.tight_layout()
    if savefig:
        extent = ax.get_window_extent().transformed(ax.get_figure().dpi_scale_trans.inverted())
        plt.savefig(f'./figures/{savefig}.{file_format}', format=file_format, dpi=600, bbox_inches=extent)