import pygame
from graph import Graph
from vertex import Vertex
from edge import Edge
from button import Button
from algorithms import dijkstra, bfs, dfs, prim
from instruction import Instruction
import random

pygame.init()
graph_radius = 10

def generate_random_graph(num_vertices, density, verteces_color):
    max_possible_edges = num_vertices * (num_vertices - 1) // 2
    num_edges = min(density, max_possible_edges)

    # Step 1: Create vertices
    next_availble_vertex_name = 0
    vertices = []
    for i in range(num_vertices):
        name = 'v' + str(i)
        v = Vertex(name, 0, 0, graph_radius, verteces_color)
        vertices.append(v)
        next_availble_vertex_name += 1

    edges = []
    used_pairs = set()

    # Step 2: Build a spanning tree (n - 1 edges)
    unconnected = vertices.copy()
    connected = [unconnected.pop(random.randrange(len(unconnected)))]
    
    while unconnected:
        u = random.choice(connected)
        v = unconnected.pop(random.randrange(len(unconnected)))
        w = random.randint(1, 10)
        edges.append(Edge(u, v, w))
        used_pairs.add(frozenset((u, v)))
        connected.append(v)

    # Step 3: Add random edges until reaching density
    while len(edges) < num_edges:
        v = random.choice(vertices)
        u = random.choice(vertices)
        if v != u:
            key = frozenset((v, u))
            if key not in used_pairs:
                w = random.randint(1, 10)
                edges.append(Edge(v, u, w))
                used_pairs.add(key)

    return Graph(vertices, edges, next_availble_vertex_name)


def check_cursor_hand(mouse_x, mouse_y, graph, buttons):
    # for vertex in verteces:
    #     if vertex.is_mouse_over():
    #         return True
    for vertex in graph.adjacency_list:
        for edge in graph.adjacency_list[vertex]:
            if edge.is_mouse_on():
                return True
        if vertex.is_mouse_over():
            return True
        
    for btn in buttons:
        if btn.is_mouse_on():
            return True
        
    return False

def drawing(win, graph, buttons, graph_zone, font):
    win.fill((255, 255, 255))
    graph.draw(win, font)  
    for btn in buttons:
        btn.draw(win)    
    # pygame.draw.rect(win, (0, 0, 0), graph_zone, width=1)
    pygame.display.flip()

def main():
    win = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    graph_zone = (10, 10, win.get_width() / 2, win.get_height())

    btns = [(1, "Reset graph location", "Reset graph location:\nWill make the graph look\nnicer in a circular way"), 
            (2, "Delete Graph", "Delete Graph:\nGives you the opportunity\nto create a new graph"), 
            (3, "Generate new graph", "Generate new graph"),
            (4, "Run dijkstra", "Run dijkstra:\n1. Choose starting node\nclick 's' on the keyboard\nwhile puting the mouse\non the node\n2. Choose final node\nclick 'f' on the keyboard\nwhile puting the mouse\non the node\n3. Click 'Run dijkstra'"),
            (5, "Run BFS", "Run BFS:\nWill replace the current graph\nwith it's spanning BFS tree\nnotice that the BFS algorithm\nignores the weights\non the edges"),
            (6, "Run DFS", "Run BFS:\nWill replace the current graph\nwith it's spanning DFS tree\nnotice that the DFS algorithm\nignores the weights\non the edges"),
            (7, "Run Prim", "Run Prim:\nWill found the minimum\nspanning tree of the graph")]
    buttons = [Button(id, win.get_width() - 185, (id - 1) * 27 + 5, 180, 25, title, (200, 200, 200), (0, 0, 0), Instruction(instruction, win.get_width() - 388, (id - 1) * 27 + 5, 200)) for id, title, instruction in btns]

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 18)
    verteces_color = (173, 216, 230)
    graph = Graph([], [], 0)
    adding_edge_from = None
    starting_color_algo = (0, 255, 0)
    final_color_algo = (120, 0, 120)
    tagged_edge_color = (220, 220, 0)
    starting_vertex_algo = None
    final_vertex_algo = None
    running = True
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovering = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                new_width, new_height = event.size
                win = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                graph_zone = (10, 10, win.get_width() / 2, win.get_height())
                graph.set_graph_for_visual(*graph_zone) 
                
                for btn in buttons:
                    btn.x = win.get_width() - 185
                    btn.rect = pygame.Rect(btn.x, btn.y, btn.w, btn.h)
                    btn.instruction.rect = pygame.Rect(btn.x - 203, btn.instruction.y, btn.instruction.w, btn.instruction.h)

            elif event.type == pygame.MOUSEBUTTONUP:
                for vertex in graph.adjacency_list:
                    vertex.choosen = False
                if adding_edge_from != None:
                    for vertex in graph.adjacency_list:
                        if vertex.is_mouse_over():
                            new_edge = Edge(adding_edge_from, vertex, 1)
                            new_edge2 = Edge(vertex, adding_edge_from, 1)
                            graph.adjacency_list[adding_edge_from].append(new_edge)
                            graph.adjacency_list[vertex].append(new_edge2)
                    adding_edge_from = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s: # stance for start
                    for vertex in graph.adjacency_list:
                        if vertex.is_mouse_over():
                            if starting_vertex_algo is not None:
                                starting_vertex_algo.color = verteces_color
                            vertex.color = starting_color_algo
                            starting_vertex_algo = vertex
                if event.key == pygame.K_f: # stance for final
                    for vertex in graph.adjacency_list:
                        if vertex.is_mouse_over():
                            if final_vertex_algo is not None:
                                final_vertex_algo.color = verteces_color
                            vertex.color = final_color_algo
                            final_vertex_algo = vertex
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    on_edge = False
                    for vertex in graph.adjacency_list:
                        for edge in graph.adjacency_list[vertex]:
                            if edge.is_mouse_on():
                                edge.decrease_weight()
                                on_edge = True
                    if not on_edge:
                        new_vertex = Vertex("v" + str(graph.next_availble_vertex_name), mouse_x, mouse_y, graph_radius, verteces_color)
                        graph.next_availble_vertex_name += 1
                        graph.adjacency_list[new_vertex] = []
                if event.button == 2:
                    for vertex in graph.adjacency_list:
                        if vertex.is_mouse_over():
                            adding_edge_from = vertex
                if event.button == 1:
                    for vertex in graph.adjacency_list:
                        if vertex.is_mouse_over():
                            vertex.choosen = True
                        for edge in graph.adjacency_list[vertex]:
                            if edge.is_mouse_on():
                                edge.increase_weight()
                    for btn in buttons:
                        if btn.is_mouse_on():
                            if btn.id == 1: # reset graph location
                                graph.set_graph_for_visual(*graph_zone)
                            if btn.id == 2: # delete graph
                                graph.reset()
                            if btn.id == 3: # generate new graph
                                r = random.randint(3, 20)
                                graph = generate_random_graph(r, random.randint(2, r), verteces_color)
                                graph.set_graph_for_visual(*graph_zone) 
                            if btn.id == 4: # run dijkstra
                                if starting_vertex_algo and final_vertex_algo:
                                    for vertex in graph.adjacency_list:
                                        for edge in graph.adjacency_list[vertex]:
                                            edge.color = (0, 0, 0)
                                    prev = dijkstra(graph, starting_vertex_algo)
                                    v = final_vertex_algo
                                    while prev[v] is not None:
                                        for vertex in graph.adjacency_list:
                                            for edge in graph.adjacency_list[vertex]:
                                                if (edge.v == prev[v] and edge.u == v) or (edge.v == v and edge.u == prev[v]):
                                                    edge.color = tagged_edge_color
                                        v = prev[v]
                            if starting_vertex_algo:
                                if btn.id == 5: # run BFS
                                    graph = bfs(graph, starting_vertex_algo)  
                                if btn.id == 6: # run BFS
                                    graph = dfs(graph, starting_vertex_algo)
                            if btn.id == 7:
                                graph = prim(graph)             
        hovering = check_cursor_hand(mouse_x, mouse_y, graph, buttons)

        if hovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        drawing(win, graph, buttons, graph_zone, font)
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()