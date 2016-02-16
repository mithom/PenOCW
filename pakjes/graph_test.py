import dijkstra
import random


def random_graph(nr_nodes):
    test_graph = dijkstra.Graph()
    for x in xrange(1, nr_nodes + 1):
        test_graph.add_node(x)
    for x in xrange(1, nr_nodes + 1):
        for y in xrange(1, nr_nodes + 1):
            if y != x:
                t = random.randint(1, 10)
                if t > 3:
                    z = random.randint(1, 10)
                    test_graph.add_edge(x, y, z)
    return test_graph


def construct_graph(nr_nodes, edges, distances):
    graph = dijkstra.Graph()
    for x in xrange(1, nr_nodes + 1):
        graph.add_node(x)
    for x in edges:
        for y in edges[x]:
            graph.add_edge(x, y, distances[(x, y)])
    return graph


def print_graph(graph):
    nr_nodes = len(graph.nodes)
    print " "
    print "Graph"
    print "-----"
    print nr_nodes, "nodes"
    print "Edges: "
    print dict(graph.edges)
    print "Distances: "
    print graph.distances


def print_solution(visit, paths, source_node):
    print " "
    print "Dijkstra solution (Source node:", str(source_node) + ")"
    print "----------------------------------"
    print "Shortest path distances from node", source_node, "to all nodes: "
    print visit
    print "Paths to nodes:"
    print paths, "                   (x: y means follow the edge from y to x)"


if __name__ == "__main__":
    start_node = 1
    test = random_graph(4)
    print_graph(test)
    (visited, path) = dijkstra.dijsktra(test, start_node)
    print_solution(visited, path, start_node)
