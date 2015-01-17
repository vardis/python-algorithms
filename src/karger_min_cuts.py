"""
Implements Karger's randomised algorithm for finding a minimum cut of an undirected graph.
"""

__author__ = 'giorgos'

import random


def read_graph():
    g = []
    num_edges = 0
    f = open("kargerMinCuts.txt", "r")
    for l in f.readlines():
        if len(l) > 0:
            entries = l.split("\t")
            entries.pop(0)

            edge_list = []
            for e in entries:
                edge_list.append(int(e))

            edge_list = [int(s) - 1 for s in l.split("\t")]
            edge_list.pop(0)
            num_edges += len(edge_list)
            g.append(edge_list)
    return (g, num_edges)



def pick_edge(graph, edge):
    """
    Picks the nth edge of the graph from its adjacency list representation and returns a tuple of the vertex indices
    for that edge.
    """
    accum = 0
    for i in range(len(graph)):
        edge_list = graph[i]
        if (accum + len(edge_list)) > edge:
            return i, edge_list[edge - accum]
        accum += len(edge_list)

    raise Exception("Illegal state, asked for an edge that does not exist!")


def merge_vertices(graph, u, v):
    graph[u].extend(graph[v])
    graph[v] = []

    def p(x):
        if x == v: return u
        else: return x

    for i in range(len(graph)):
        edge_list = map(p, graph[i])
        graph[i] = edge_list


def remove_self_loops(graph, u, v):
    edge_list = graph[u]

    new_edge_list = [x for x in edge_list if x != u and x != v]
    removed = len(edge_list) - len(new_edge_list)
    graph[u] = new_edge_list

    return removed


def random_contraction(graph, num_edges):
    g = []
    for edge_list in graph:
        g.append([x for x in edge_list])

    vertices = len(g)
    edges = num_edges

    while vertices > 2:
        edge = random.randint(0, edges - 1)
        u, v = pick_edge(g, edge)

        # merge v into u, so v's adjacency list is removed and u's list is extended
        merge_vertices(g, u, v)

        vertices -= 1
        edges -= remove_self_loops(g, u, v)

        if edges < 1:
            raise Exception("Illegal state, there should be some edges left!")

    return edges


input_graph, num_edges = read_graph()
# print input_graph

import time

min_cuts = 1e1000
for i in xrange(4000):
    random.seed(time.time())
    cuts = random_contraction(input_graph, num_edges)
    if min_cuts > cuts:
        min_cuts = cuts

print 'Found minimum cut with ', min_cuts / 2, ' crossing edges'
