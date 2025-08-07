from edge import Edge
import math

class Graph:
    def __init__(self, vertices, edges, next_availble_vertex_name):
        self.adjacency_list = {}
        for v in vertices:
            self.adjacency_list[v] = []
        for e in edges:
            self.adjacency_list[e.v].append(e)
            self.adjacency_list[e.u].append(Edge(e.u, e.v, e.w))  # mirror edge
        self.ready_to_visualize = False
        self.next_availble_vertex_name = next_availble_vertex_name
    
    def set_graph_for_visual(self, x, y, width, height):
        vertices_len = len(self.adjacency_list)
        center_x = x + width // 2
        center_y = y + height // 2
        radius = min(width, height) // 2 - 50  # padding

        for i, v in enumerate(self.adjacency_list):
            angle = 2 * math.pi * i / vertices_len
            v.x = int(center_x + radius * math.cos(angle))
            v.y = int(center_y + radius * math.sin(angle))
        self.ready_to_visualize = True

    def draw(self, win, font):
        for v in self.adjacency_list:
            for e in self.adjacency_list[v]:
                e.draw(win, font)
            v.draw(win, font)

    def reset(self):
        self.adjacency_list = {}
    def __str__(self):
        output = "--------------\n"
        output += "Adjacency List\n"
        output += "--------------\n"
        for v in self.adjacency_list:
            output += f"\nNeighbors of {v.name}\n"
            for e in self.adjacency_list[v]:
                output += f"*\t (neighbor: {e.u.name}, weight: {e.w})\n"
        return output
