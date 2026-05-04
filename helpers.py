"""
    
    Christpher Getzie
    CSC 5930 - 002: Network Science
    Dr. Maurício Gruppi
    
    Helper functions for the "Follow the Industy" Final Project.
    Functions were taken from labs & modified for this project.
    
    
"""

import networkx as nx
import numpy as np
import scipy as si
import scipy.stats

#------------------------------------------------------------------
# Degree Helpers
#------------------------------------------------------------------

# Average Degree
def get_average_degree(g: nx.Graph):
    nodes, degrees = zip(*nx.degree(g))
    return np.mean(degrees)

# Maximum Degree
def get_kmax(g: nx.Graph):
    nodes, degrees = zip(*nx.degree(g))
    return max(degrees)

# Minimum Degree
def get_kmin(g: nx.Graph):
    nodes, degrees = zip(*nx.degree(g))
    return min(degrees)

# <k^2>
def get_second_moment_of_degree(g: nx.Graph) -> float:
    """Second moment <k^2> of the degree distribution."""
    nodes, degrees = zip(*nx.degree(g))
    degrees = np.array(degrees, dtype=float)
    return float(np.mean(degrees ** 2))

# Make Degree Histogram
def make_degree_histogram(g, bins=None, ccdf=False):
    nodes, degrees = zip(*nx.degree(g))

    if bins is None and not ccdf:
        bins = np.logspace(np.log2(1), np.log2(max(degrees)), base=2)
    else:
        bins = 'auto'

    pk, k = np.histogram(degrees, density=True, bins=bins)
    if ccdf:
        pk = 1 - np.cumsum(pk)
    k = k[:-1]
    return k, pk

#------------------------------------------------------------------
# Giant Component Helpers
#------------------------------------------------------------------

# This is used to retrieve the size of the giant component of a graph g.
def size_of_giant_component(g: nx.Graph):
    gc = sorted(nx.connected_components(g), key=len, reverse=True)
    if not gc:
        return 0
    g0 = g.subgraph(gc[0])
    
    # Return the number of nodes
    return g0.number_of_nodes()

# Return the largest connected component as a new graph.
def giant_component(g: nx.Graph) -> nx.Graph:
    gc = sorted(nx.connected_components(g), key=len, reverse=True)
    return g.subgraph(gc[0]).copy()

#------------------------------------------------------------------
# Bipartite Projection Helpers
#------------------------------------------------------------------

# Project a bipartite graph onto one of its node sets.
def bipartite_projection(B: nx.Graph, node_set, weight_func='count'):
    """ 
    weight_func:
      - 'count'   : number of shared neighbors
      - 'overlap' : weighted overlap (sum of min weights)
      - 'sum'     : sum of products of edge weights through shared neighbors
    """
    if weight_func == 'count':
        return nx.algorithms.weighted_projected_graph(B, node_set)
    elif weight_func == 'overlap':
        return nx.algorithms.overlap_weighted_projected_graph(B, node_set)
    elif weight_func == 'sum':
        return nx.algorithms.collaboration_weighted_projected_graph(B, node_set)
    else:
        raise ValueError(f"Unknown weight_func: {weight_func}")

# First attempt took too long, 
def fast_bipartite_projection(B: nx.Graph, project_nodes, threshold_percentile=None):
    """
    Fast bipartite projection using scipy sparse matrix multiplication.
 
    For a bipartite adjacency A (project_nodes x other_nodes), the projection
    onto project_nodes is A @ A.T, where entry (i,j) is the number of shared
    neighbors between i and j.
 
    NetworkX's weighted_projected_graph is O(N^2 * d) and becomes very slow
    for large dense bipartite graphs. This sparse-matrix version is typically
    100-1000x faster and produces an identical result for the 'count' weight.
 
    Parameters
    ----------
    B : networkx.Graph
        Bipartite graph.
    project_nodes : iterable
        Nodes to project onto.
    threshold_percentile : int or None
        If given, only edges whose weight is at or above this percentile of
        the projected-edge weights are kept. Useful because bipartite
        projections are notoriously dense.
 
    Returns
    -------
    networkx.Graph
        Weighted projection graph (edge attribute 'weight' = shared neighbors).
        All node attributes from B are copied onto the projection.
    """
 
 
    project_nodes = list(project_nodes)
    other_nodes = [n for n in B.nodes if n not in set(project_nodes)]
 
    p_idx = {n: i for i, n in enumerate(project_nodes)}
    o_idx = {n: i for i, n in enumerate(other_nodes)}
 
    rows, cols = [], []
    for u, v in B.edges:
        if u in p_idx and v in o_idx:
            rows.append(p_idx[u]); cols.append(o_idx[v])
        elif v in p_idx and u in o_idx:
            rows.append(p_idx[v]); cols.append(o_idx[u])
 
    A = si.sparse.coo_matrix(
        (np.ones(len(rows)), (rows, cols)),
        shape=(len(project_nodes), len(other_nodes)),
    ).tocsr()
 
    PP = A @ A.T
    PP = PP.tolil()
    PP.setdiag(0)
    PP = si.sparse.triu(PP.tocsr(), k=1).tocoo()
 
    weights = PP.data
    if threshold_percentile is not None and len(weights) > 0:
        cutoff = np.percentile(weights, threshold_percentile)
        keep = weights >= cutoff
        ii, jj, ww = PP.row[keep], PP.col[keep], weights[keep]
    else:
        ii, jj, ww = PP.row, PP.col, weights
 
    P = nx.Graph()
    for n in project_nodes:
        P.add_node(n, **{k: v for k, v in B.nodes[n].items() if k != 'bipartite'})
    for i, j, w in zip(ii, jj, ww):
        P.add_edge(project_nodes[i], project_nodes[j], weight=int(w))
 
    return P

#------------------------------------------------------------------
# Community Detection Helpers
#------------------------------------------------------------------

# Find communities using NetworkX's implementation of greedy modularity maximization
def find_communities(g: nx.Graph, attr_name='c', resolution=1.0, weight=None):
    """
    Runs NetworkX's greedy modularity and returns a graph with nodes holding their community attribute.
    Also returns the communities found as a list of sets like [{comm_1_nodes}, {comm_2_nodes},...].
    """
    comms = nx.community.greedy_modularity_communities(
        g, 
        resolution=resolution,
        weight=weight
    )

    for comm_idx, comm in enumerate(comms):
        for node_idx in comm:
            g.nodes[node_idx][attr_name] = comm_idx
    return g, comms

#------------------------------------------------------------------
# Network Drawing Helpers
#------------------------------------------------------------------

# draw_network from lab 2. Modified for project.
def draw_network(g, node_color='red', node_size = 100, ax=None):
    nx.draw(
        g,
        pos=nx.spring_layout(g, scale=5, seed=42),
        node_size=node_size,
        node_color=node_color,
        edgecolors='black',
        alpha=0.75,
        linewidths=1, 
        ax=ax
    )