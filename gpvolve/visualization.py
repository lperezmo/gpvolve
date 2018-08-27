from .utils import *
import matplotlib.pyplot as plt
from gpgraph.draw import *


def plot_timescales(timescales, figsize=None, n=None, color='orange'):
    fig, ax = plt.subplots(figsize=figsize)
    ax.bar([i for i in range(0, len(timescales[:n]))], timescales[:n], color=color)
    ax.set_title("Timescales")
    return fig, ax

def plot_eigenvalues(eigenvalues, figsize=None, n=None, color='orange'):
    fig, ax = plt.subplots(figsize=figsize)
    ax.bar([i for i in range(0, len(eigenvalues[:n]))], eigenvalues[:n], color=color)
    ax.set_title("Timescales")
    return fig, ax

def plot_clusters(network, clusters, scale=1, figsize=(10,10)):
    spm = shortest_path_matrix(network)
    pos = cluster_positions(network, clusters, spm, scale=scale)

    #fig, ax = plt.subplots(figsize=figsize)
    fig, ax = draw_flattened(network, pos=pos)


    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.set_xticks([i for i in np.arange(0, 1.1, 0.1)])
    ax.set_yticks([i for i in np.arange(0, 1.1, 0.05)])
    ax.autoscale(enable=True)
    ax.set_xlabel("Forward Committor", size=15)
    ax.set_ylabel("Fitness", size=15)

    return fig, ax

def draw_clusters(
    network,
    clusters,
    ax=None,
    figsize=(10,10),
    cluster_scale=1,
    nodelist=[],
    attribute="phenotypes",
    vmin=None,
    vmax=None,
    cmap="YlOrRd",
    cmap_truncate=False,
    colorbar=False,
    labels='binary',
    **kwds):
    """Draw the GenotypePhenotypeGraph using Matplotlib.

    Draw the graph with Matplotlib with options for node positions,
    labeling, titles, and many other drawing features.
    See draw() for simple drawing without labels or axes.

    Parameters
    ----------
    G : graph
       A networkx graph

    pos : dictionary, optional
       A dictionary with nodes as keys and positions as values.
       If not specified a spring layout positioning will be computed.
       See :py:mod:`networkx.drawing.layout` for functions that
       compute node positions.

    arrows : bool, optional (default=False)
       For directed graphs, if True draw arrowheads.

    with_labels :  bool, optional (default=True)
       Set to True to draw labels on the nodes.

    ax : Matplotlib Axes object, optional
       Draw the graph in the specified Matplotlib axes.

    nodelist : list, optional (default G.nodes())
       Draw only specified nodes

    attribute : string (default = "phenotypes")
       node attribute that is used to set the color

    edgelist : list, optional (default=G.edges())
       Draw only specified edges

    node_size : scalar or array, optional (default=300)
       Size of nodes.  If an array is specified it must be the
       same length as nodelist.

    node_color : color string, or array of floats, (default=phenotypes)
       Node color. Can be a single color format string,
       or a  sequence of colors with the same length as nodelist.
       If numeric values are specified they will be mapped to
       colors using the cmap and vmin,vmax parameters.  See
       matplotlib.scatter for more details.

    node_shape :  string, optional (default='o')
       The shape of the node.  Specification is as matplotlib.scatter
       marker, one of 'so^>v<dph8'.

    alpha : float, optional (default=1.0)
       The node and edge transparency

    cmap : Matplotlib colormap, optional (default='plasmas')
       Colormap for mapping intensities of nodes

    vmin,vmax : float, optional (default=None)
       Minimum and maximum for node colormap scaling

    linewidths : [None | scalar | sequence]
       Line width of symbol border (default =1.0)

    width : float, optional (default=1.0)
       Line width of edges

    color_bar : False
        If True, show colorbar for nodes.

    edge_color : color string, or array of floats (default='gray')
       Edge color. Can be a single color format string,
       or a sequence of colors with the same length as edgelist.
       If numeric values are specified they will be mapped to
       colors using the edge_cmap and edge_vmin,edge_vmax parameters.

    edge_cmap : Matplotlib colormap, optional (default=None)
       Colormap for mapping intensities of edges

    edge_vmin,edge_vmax : floats, optional (default=None)
       Minimum and maximum for edge colormap scaling

    style : string, optional (default='solid')
       Edge line style (solid|dashed|dotted,dashdot)

    labels : dictionary, optional (default='genotypes')
       Node labels in a dictionary keyed by node of text labels

    font_size : int, optional (default=12)
       Font size for text labels

    font_color : string, optional (default='k' black)
       Font color string

    font_weight : string, optional (default='normal')
       Font weight

    font_family : string, optional (default='sans-serif')
       Font family

    label : string, optional
        Label for graph legend

    Notes
    -----
    For directed graphs, "arrows" (actually just thicker stubs) are drawn
    at the head end.  Arrows can be turned off with keyword arrows=False.
    Yes, it is ugly but drawing proper arrows with Matplotlib this
    way is tricky.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure(figsize=figsize)

    # Flattened position
    pos = cluster_positions(network, clusters, scale=cluster_scale)

    if not nodelist:
        nodelist = list(network.nodes().keys())

    if vmax is None:
        attributes = list(nx.get_node_attributes(network, name=attribute).values())
        vmin = min(attributes)
        vmax = max(attributes)

    if cmap_truncate:
        cmap = truncate_colormap(cmap, minval=0.05, maxval=0.95)

    # Default options
    options = dict(
        pos=pos,
        nodelist=nodelist,
        arrows=False,
        vmin=vmin,
        vmax=vmax,
        node_color=[network.nodes[n][attribute] for n in nodelist],
        cmap=cmap,
        cmap_truncate=False,
        edge_color='white',
        labels={n: network.nodes[n][labels] for n in nodelist},
        with_labels=False
    )
    options.update(**kwds)

    # Draw fig
    nx.draw_networkx(network, **options)

    # Add a colorbar?
    if colorbar:
        norm = mpl.colors.Normalize(
            vmin=vmin,
            vmax=vmax)

        # create a ScalarMappable and initialize a data structure
        cm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
        cm.set_array([])
        fig.colorbar(cm)

    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.set_xticks([i for i in np.arange(0, 1.1, 0.1)])
    ax.autoscale(enable=True)
    ax.set_xlabel("Forward Committor", size=15)
    ax.set_ylabel("Fitness", size=15)
    ax.axis("equal")

    return fig, ax