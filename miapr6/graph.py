import math


def get_hierarhy(graph, mode='min'):
    if mode == 'max':
        for vertex_connections in graph:
            for key, value in vertex_connections.items():
                if value != 0:
                    vertex_connections[key] = 1 / value
    connections = []
    v, u, price = 0, 0, 0
    for _ in range(len(graph) - 1):
        v, (u, price) = min(map(lambda x: (x[0], min(x[1].items(), key=lambda y: y[1])), enumerate(graph)),
                            key=lambda z: z[1][1])
        connections.append([v, u, price])
        vertixes_unite(graph, u, v)
        graph[u] = {u: math.inf}
    graph[v] = {v: math.inf}
    return connections


def vertixes_unite(graph, deleted, remain):
    for vertex_connections in graph:
        if (remain in vertex_connections) and (deleted in vertex_connections):
            vertex_connections[remain] = min(vertex_connections[remain], vertex_connections[deleted])
        try:
            del vertex_connections[deleted]
        except KeyError:
            pass


def add_connection(graph, v, u, price):
    graph[v][u] = price
    graph[u][v] = price
