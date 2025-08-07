from collections import deque
from vertex import Vertex
from edge import Edge
from graph import Graph
import random

def dijkstra(graph, s): # s = starting vertex
    prev = dict() # used to restore the shortest path later on
    d = dict()
    constants = [s]
    temp = []
    curr = s
    d[s] = 0
    for vertex in graph.adjacency_list:
        if vertex != s:
            temp.append(vertex)
            d[vertex] = float('inf')
        prev[vertex] = None
    
    while len(temp) != 0:
        # relaxing:
        for edge in graph.adjacency_list[curr]:
            v, u, w = edge.v, edge.u, edge.w
            if d[v] + w < d[u]:
                d[u] = d[v] + w
                prev[u] = v
        
        next_in = temp[0] # next vertex to join constants list
        for v in temp:
            if d[v] < d[next_in]:
                next_in = v
        
        constants.append(next_in) # adding to constants
        temp.remove(next_in) # removing from temp
        curr = next_in
    return prev


def bfs(graph, s):# s = starting vertex
    if len(graph.adjacency_list) <= 0:
        return Graph([], [], 0)
    spanning_bfs_tree_verteces = [s]
    spanning_bfs_tree_edges = []
    stack = deque()
    stack.append(s)
    shown = {}
    for v in graph.adjacency_list:
        shown[v] = False
    shown[s] = True
    while stack:
        curr = stack.popleft()
        neighbors = graph.adjacency_list[curr]
        for n in neighbors:
            if not shown[n.u]:
                stack.append(n.u)
                shown[n.u] = True
                spanning_bfs_tree_verteces.append(n.u)
                spanning_bfs_tree_edges.append(n)

    spanning_bfs_tree = Graph(spanning_bfs_tree_verteces, spanning_bfs_tree_edges, len(spanning_bfs_tree_verteces))
    return spanning_bfs_tree


def dfs(graph, s):# s = starting vertex
    if len(graph.adjacency_list) <= 0:
        return Graph([], [], 0)
    spanning_dfs_tree_verteces = [s]
    spanning_dfs_tree_edges = []
    stack = deque()
    stack.append(s)
    shown = {}
    for v in graph.adjacency_list:
        shown[v] = False
    shown[s] = True
    while stack:
        curr = stack.pop()
        neighbors = graph.adjacency_list[curr]
        for n in neighbors:
            if not shown[n.u]:
                stack.append(n.u)
                shown[n.u] = True
                spanning_dfs_tree_verteces.append(n.u)
                spanning_dfs_tree_edges.append(n)

    spanning_dfs_tree = Graph(spanning_dfs_tree_verteces, spanning_dfs_tree_edges, len(spanning_dfs_tree_verteces))
    return spanning_dfs_tree


def prim(graph):
    if len(graph.adjacency_list) <= 0:
        return Graph([], [], 0)
    
    # choosing a random initial vertex
    starting_vertex = random.choice(list(graph.adjacency_list.keys()))
    
    num_of_verteces = len(graph.adjacency_list)
    min_spanning_tree_verteces = [starting_vertex]
    min_spanning_tree_edges = []

    while len(min_spanning_tree_verteces) < num_of_verteces:
        min_edge = Edge(None, None, float('inf'))
        for vertex in min_spanning_tree_verteces:
            for edge in graph.adjacency_list[vertex]:
                if (edge.w < min_edge.w) and (edge.u not in min_spanning_tree_verteces):
                    min_edge = edge
        
        if min_edge.u is None: # unconnected graph: prim cannot run
            return Graph([], [], 0)
        min_spanning_tree_verteces.append(min_edge.u)
        min_spanning_tree_edges.append(min_edge)
    
    return Graph(min_spanning_tree_verteces, min_spanning_tree_edges, len(min_spanning_tree_verteces))

