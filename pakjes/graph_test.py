import dijkstra
import random

def random_graph(nr_nodes):
    test_graph = dijkstra.Graph()
    for x in xrange(1,nr_nodes + 1):
        test_graph.add_node(x)
    for x in xrange(1,nr_nodes + 1):
        for y in xrange(1,nr_nodes + 1):
            if y != x:
                t = random.randint(1,10)
                if t > 3:
                    z = random.randint(1,10)
                    test_graph.add_edge(x, y, z)
    return test_graph

def print_graph(graph):
    nr_nodes = len(graph.nodes)
    print " "
    print "Graph"
    print "-----"
    print nr_nodes, " nodes"
    print "Edges: "
    print graph.edges
    print "Distances: "
    print graph.distances

def print_solution(visited, path):
    print " "
    print "Dijkstra solution"
    print "-----------------"
    print "Visited: "
    print visited
    print "Path: "
    print path
    print " "

if __name__ == "__main__":
    test = random_graph(4)
    print_graph(test)
    (visited, path) = dijkstra.dijsktra(test, 1)
    print_solution(visited, path)
