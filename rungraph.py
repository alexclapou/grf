import random
def random_graph(graph,n,m):
    g = graph("graph1k.txt")
    addedEdges = 0
    g.vertices = n
    g.edges = m
    while addedEdges < m:
            origin = random.randrange(0,n)
            target = random.randrange(0,n)
            if not g.check_if_edge(origin, target):
                    g.add_edge(origin, target, 0)
                    addedEdges += 1
    return g
