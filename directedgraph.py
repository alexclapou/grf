from collections import OrderedDict
import math
from rungraph import random_graph
import time
import copy
import random
class DirectedGraph(object):
    '''
    keep the target and origins in dictionaries neighbours_out and neighbours_in
    for cost keep the cost of every edge in a dictionary cost
    e.g. neighbours_in = {0: [0]}
    e.g. neighbours_out = {0: [0, 1]}
    e.g. cost = {(0, 0) = 1}
    '''
    def __init__(self, file_name):
        f = open(file_name, "r")
        first_line = f.readline()
        vertices, edges = first_line.split()
        self.vertices = int(vertices)
        self.edges = 0
        self.neighbours_in = {}
        self.neighbours_out  = {}
        self.cost = {}
        for i in range(0, self.vertices):
            self.neighbours_in[i] = []
            self.neighbours_out[i] = []
        new_line = f.read()
        aux1, aux2 = -1, -1
        filee = open("graph.txt", "r")
        for i in filee:
            if aux1 == aux2 and aux1 == -1:
                aux1 = 0
                aux2 = 0
            else:
                i = i[:-1]
                parameters = i.split(" ")
                parameters = list(map(int, parameters))
                self.add_edge(parameters[0], parameters[1], parameters[2])

    #get the number of vertices
    def vertices_number(self):
        return len(self.neighbours_in.keys())

    #parse  the set of vertices
    def parse_vertices(self):
        return list(self.neighbours_in.keys())

    #find out whether there is an edge from the first one to the second one and return edge id
    def edge_id(self, vertex1, vertex2):
        edge = (vertex1, vertex2)
        if edge in self.cost.keys():
            costs = OrderedDict(self.cost)#create an orderedDict to get index of the edge
            return list(costs.keys()).index(edge)
        return None

    #get  the in degree
    def in_degree(self, vertex):
        return len(self.neighbours_in[vertex])

    #get the out degree
    def out_degree(self, vertex):
        return len(self.neighbours_out[vertex])

    #parse inbound edges
    def parse_inbound_edges(self, vertex):
        inbound_edges = []
        for i in self.neighbours_in[vertex]:
            edge = [i, vertex]
            inbound_edges.append(edge)
        return inbound_edges
    
    #parse the origin of the edge 
    def parse_inbound(self, vertex):
        return list(self.neighbours_in[vertex])

    #parse the target of the edge
    def parse_outbound(self, vertex):
            return list(self.neighbours_out[vertex])

    #get the endpoint for an edge_id
    def get_endpoint(self, edge_id):
        endpoints = []
        costs = OrderedDict(self.cost)
        edges = list(costs.keys())
        for i, edge in enumerate(edges):
            if i == edge_id:
                endpoints.append(edge[1])
        return endpoints

    #add an edge
    def add_edge(self, origin, target, cost):
        if origin in self.neighbours_in.keys() and target in self.neighbours_in.keys():
            self.neighbours_out[origin].append(target)
            self.neighbours_in[target].append(origin)
            edge = (origin, target)
            self.cost[edge] = cost
            self.edges += 1
        else:
            print("can't add this edge")

    #remove an edge
    def remove_edge(self, origin, target):
        edge = (origin, target)
        del self.cost[edge]
        self.neighbours_out[target].remove(origin)
        self.neighbours_in[origin].remove(target)
        self.edges -= 1

    #add a vertex
    def add_vertex(self, vertex):
        if vertex not in self.neighbours_in.keys():
            self.neighbours_out[vertex] = []
            self.neighbours_in[vertex] = []
            self.vertices += 1

    #remove a vertex
    def remove_vertex(self, vertex):
        try:
            for i in self.neighbours_in:
                if vertex in self.neighbours_in.get(i):
                    self.neighbours_in.get(i).remove(vertex)
                    del self.cost[(vertex, i)]
                    self.edges -= 1
            del self.neighbours_in[vertex]
            for i in self.neighbours_out:
                if vertex in self.neighbours_out.get(i):
                    self.neighbours_out.get(i).remove(vertex)
            del self.neighbours_out[vertex]
            self.vertices -= 1
        except:
            print("nothing to remove")

    def check_if_vertex(self, vertex):
        try:
            if vertex in self.neighbours_in.keys():
                return 1
            return 0
        except:
            pass

    #check if exist an edge
    def check_if_edge(self, origin, target):
        try:
            if target in self.neighbours_out[origin] or origin in self.neighbours_out[target]:
                return 1
            return 0
        except:
            pass

    def modify_cost(self, origin, target, new_cost):
        edge = (origin, target)
        self.cost[edge] = new_cost

    def input_graph(self, file_input):
        f = open(file_input, "r")
        number_of_vertices = -1
        number_of_edges = -1
        self.copy_vertices = copy.deepcopy(self.vertices)
        self.copy_edges = copy.deepcopy(self.edges)
        self.copy_neighbours_in = dict(self.neighbours_in)
        self.copy_neighbours_out  = dict(self.neighbours_out)
        self.copy_cost = dict(self.cost)
        self.neighbours_in.clear()
        self.neighbours_out.clear()
        self.cost.clear()
        for i in f:
            if number_of_edges == -1 and number_of_vertices == -1:
                i = i[:-1]
                parameters = i.split(" ")
                number_of_vertices, number_of_edges = list(map(int, parameters))
                self.vertices = number_of_vertices
                self.edges = number_of_edges
                for i in range(self.vertices):
                    self.neighbours_in[i] = []
                    self.neighbours_out[i] = []
            else:
                i = i[:-1]
                parameters = i.split(" ")
                parameters = list(map(int, parameters))
                self.add_edge(parameters[0], parameters[1], parameters[2])

    def output_graph(self, file_output):
        f = open(file_output, "w")
        f.write(str(self.vertices))
        f.write(" ")
        f.write(str(self.edges))
        f.write("\n")
        for edge in self.cost:
            f.write(str(edge[0]))
            f.write(" ")
            f.write(str(edge[1]))
            f.write(" ")
            f.write(str(self.cost[edge]))
            f.write("\n")

    def swap_copied_graph(self):
        try:
            self.vertices, self.copy_vertices = self.copy_vertices, self.vertices
            self.edges, self.copy_edges = self.copy_edges, self.edges
            self.neighbours_out, self.copy_neighbours_out = self.copy_neighbours_out, self.neighbours_out
            self.neighbours_in, self.copy_neighbours_in = self.copy_neighbours_in, self.neighbours_in
            self.cost, self.copy_cost = self.copy_cost, self.cost
        except:
            print("can't copy anything\n")

    def print_menu(self):
        print("\n1.read graph from a file")
        print("2.write graph to a file")
        print("3.switch to the copy")
        print("4.add a vertex")
        print("5.remove a vertex")
        print("6.add a new edge")
        print("7.modify the cost of an edge")
        print("8.remove an edge")
        print("9.get number of vertices")
        print("10.parse the set of vertices")
        print("11.check if a number is vertex")
        print("12.check if 2 vertices are an edge")
        print("13.get the in degree of a vertex")
        print("14.get the out degree of a vertex")
        print("15.parse outbound edges")
        print("16.parse inbound edges")
        print("17.print a random graph")
        print("18.exit")
        print("19.BFS between two nodes")

    def run(self):
        while True:
            self.print_menu()
            command = input("command: ")
            if command == "1":
                file_name = input("give a file name to read: ")
                self.input_graph(file_name)
            if command == "2":
                file_name = input("give a file name to write: ")
                self.output_graph(file_name)
            if command == "3":
                self.swap_copied_graph()
            if command == "4":
                vertex = int(input("vertex to add: "))
                self.add_vertex(vertex)
            if command == "5":
                vertex = int(input("vertex to remove: "))
                self.remove_vertex(vertex)
            if command == "6":
                origin = int(input("origin: "))
                target = int(input("target: "))
                cost = int(input("cost: "))
                self.add_edge(origin, target, cost)
            if command == "7":
                origin = int(input("origin: "))
                target = int(input("target: "))
                new_cost = int(input("cost: "))
                self.modify_cost(origin, target, new_cost)
            if command == "8":
                origin = int(input("origin: "))
                target = int(input("target: "))
                self.remove_edge(origin, target)
            if command == "9":
                print("vertices number: " + str(self.vertices_number()))
            if command == "10":
                print("vertices:", end=" ")
                for i in self.parse_vertices():
                    print(i, end=" ")
            if command == "11":
                check_vertex = int(input("given vertex: "))
                if self.check_if_vertex(check_vertex) == 1:
                    print("is vertex")
                else:
                    print("not a vertex")
            if command == "12":
                origin = int(input("origin: "))
                target = int(input("target: "))
                if self.check_if_edge(origin, target) == 1:
                    print("is a edge")
                else:
                    print("not an edge")
            if command == "13":
                vertex = int(input("give vertex: "))
                print("in degree: " + str(self.in_degree(vertex)))
            if command == "14":
                vertex = int(input("give vertex: "))
                print("in degree: " + str(self.out_degree(vertex)))
            if command == "15":
                vertex = int(input("give vertex: "))
                for j in self.parse_outbound(vertex):
                    print(vertex, '->', j)
            if command == "16":
                vertex = int(input("give vertex: "))
                for j in self.parse_inbound(vertex):
                    print(vertex, '<-', j)
            if command == "17":
                new_graph = random_graph(DirectedGraph, 1000, 10000)
                for i in new_graph.parse_vertices():
                    for j in new_graph.parse_inbound(i):
                        print(i, '<-', j)
            if command == "18" or command == "exit":
                return 0
            if command == "19":
                start = int(input("start vertex: "))
                end = int(input("end vertex: "))
                print(self.BFS(start, end))

    def get_tree(self, vertex):
        next_vertices = []
        tree = {}
        vertices_added = []

        tree[vertex] = []
        vertices_added.append(vertex)
        next_vertices.append(vertex)
        while len(next_vertices) > 0:
            current_vertex = next_vertices.pop()
            for neighbour_out in self.parse_outbound(current_vertex):
                if neighbour_out not in vertices_added:
                    vertices_added.append(neighbour_out)
                    tree[neighbour_out] = []
                    tree[current_vertex].append(neighbour_out)
                    next_vertices.append(neighbour_out)
        return tree
   
    def print_tree(self, tree, root, spaces):
        print(spaces + str(root))
        for children in tree[root]:
            self.print_tree(tree, children, spaces + "    ")

    
    def BFS(self, start, end):
        '''

        '''
        path = [end]
        current_nodes = [start]
        visited_nodes = []
        in_degree = dict.fromkeys(self.parse_vertices(), 0)

        #visit all the nodes until the end node
        while end not in visited_nodes and current_nodes:
            pop_node = current_nodes.pop(0)
            for node in self.neighbours_out[pop_node]:
                if node not in current_nodes and node not in  visited_nodes:
                    current_nodes.append(node)
                #if we didn't visit the node we add +1 for in degree so we know how many vertices found point to node
                if node not in visited_nodes:
                    in_degree[node] += 1
            visited_nodes.append(pop_node)
        #now we have all the nodes visited in bfs in visited_nodes

        last_node = 0
        last_pop_node = visited_nodes.pop()
        #go to the first in degree in visited nodes, that's the lowest path
        while visited_nodes:
            #we have nodes in degree and we assume that we have a path
            #the last element in visited_nodes is the vertex that point to the end node
            #so we find the first node that point to the vertex that point to the end node and so on
            #first node that point to the vertex should lead to lowest length path
            while in_degree[last_pop_node] > 0:
                last_node = visited_nodes.pop()
                if last_node in self.neighbours_in[last_pop_node]:
                    in_degree[last_pop_node] -= 1
            last_pop_node = last_node
            #if the last node is targeting to the last node in path append it
            if last_node in self.neighbours_in[path[-1]]:
                path.append(last_node)

        path.reverse()
        #check if the path is correct (start = first element, end = last and the length of the path > 0
        if path == [end] or path[0] != start or path[-1] != end:
            path = "not a path"
        return path
    
    def matrix_multiplication(self, matrix_a, matrix_b):
        result_matrix = [[math.inf for column in range(self.vertices)]for rows in range(self.vertices)]
        for i in range(len(matrix_a)):
            for j in range(len(matrix_b[0])):
                for k in range(len(matrix_b)):
                    result_matrix[i][j] = matrix_a[i][k] * matrix_b[k][j]
        return result_matrix
    
    def costs_to_matrix(self):
        cost_matrix = [[math.inf for column in range(self.vertices)]for rows in range(self.vertices)]
        for i in self.cost:
            origin, target = i
            cost_matrix[origin][target] = self.cost[i]
        for i in range(self.vertices):
            cost_matrix[i][i] = 0
        return cost_matrix

    def lowest_cost(self, origin, target):
        W_matrix = self.costs_to_matrix()
        D_matrix = W_matrix
        for i in range(self.vertices):
            D_matrix = self.ceva_functie(D_matrix, W_matrix)
        return D_matrix


def test__read_from_file():
    graph = DirectedGraph("graph.txt")
    assert(graph.vertices_number() == 5)
    assert(graph.edges == 6)
    for i in range(4):
        assert(graph.check_if_vertex(i) == 1)
    assert(graph.check_if_edge(0, 0) == 1)
    assert(graph.check_if_edge(0, 1) == 1)
    assert(graph.check_if_edge(1, 2) == 1)
    assert(graph.check_if_edge(2, 1) == 1)
    assert(graph.check_if_edge(1, 3) == 1)
    assert(graph.check_if_edge(2, 3) == 1)

def test__add_vertex():
    graph = DirectedGraph("graph.txt")
    assert(graph.vertices_number() == 5)
    graph.add_vertex(123)
    assert(graph.vertices_number() == 6)

def test__remove_vertex():
    graph = DirectedGraph("graph.txt")
    assert(graph.vertices_number() == 5)
    graph.remove_vertex(0)
    assert(graph.vertices_number() == 4)


def test__add_edge():
    graph = DirectedGraph("graph.txt")
    assert(graph.edges == 6)
    graph.add_edge(3, 0, 12)
    assert(graph.edges == 7)
    assert(graph.check_if_edge(3, 0) == 1)

def test__remove_edge():
    graph = DirectedGraph("graph.txt")
    assert(graph.edges == 6)
    graph.remove_edge(0, 0)
    assert(graph.edges == 5)
    assert(graph.check_if_edge(0, 0) == 0)

def test__in_out_degree():
    graph = DirectedGraph("graph.txt")
    assert(graph.in_degree(1) == 2)
    assert(graph.out_degree(1) == 2)

def test__edge_id():
    graph = DirectedGraph("graph.txt")
    assert(graph.edge_id(0, 0) == 0)
    assert(graph.edge_id(0, 1) == 1)
    assert(graph.edge_id(2, 3) == 5)
    assert(graph.edge_id(2, 1) == 3)

'''
test__edge_id()
test__in_out_degree()
test__add_edge()
test__remove_vertex()
test__read_from_file()
test__add_vertex()
'''
graph = DirectedGraph("graph.txt")
print(graph.lowest_cost(0,0))
