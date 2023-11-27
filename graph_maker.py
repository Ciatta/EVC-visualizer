from enum import Enum
import networkx as nx

class shapes(Enum):
    triangle = 1
    square = 2
    octagon = 3
    hexagon = 4

def make_grid(shape, h, w):
    # Define the dimensions of the grid
    nrows = h
    ncols = w
    
    # Create a grid graph using NetworkX
    G = nx.grid_2d_graph(nrows, ncols, periodic=False)
    
    #Adjust nodes and edges for each type of grid
    if (shape == shapes.triangle or shape == shapes.octagon):
        for i, j in G.nodes():
            if i < nrows-1 and j > 0:
                G.add_edge((i, j), (i+1, j-1))
    
    if (shape == shapes.octagon):
        for i, j in G.nodes():
            if i < nrows-1 and j < ncols-1:
                G.add_edge((i, j), (i+1, j+1))
    
    if (shape == shapes.hexagon):
        if (h<4 or h%2==1): 
            print("h needs to be even and bigger than 4")
            return
        G.remove_node((0,w-1))
        if (h%4 == 0): G.remove_node((h-1,w-1))
        else: G.remove_node((h-1,0))
        to_add = []
        for i, j in G.nodes():
            if i < nrows and j < ncols-1:
                if ((i, j), (i, j+1)) in G.edges():
                    G.remove_edge((i, j), (i, j+1))
        for i, j in G.nodes():
            if (i) % 4 == 0:
                if i < nrows-1 and j < ncols-1:
                    to_add.append(((i, j), (i+1, j+1)))
            if (i+2) % 4 == 0:
                if i < nrows-1 and j >0:
                    to_add.append(((i, j), (i+1, j-1)))
        for edge in to_add:
            G.add_edge(edge[1], edge[0])
        
    return G

#Get nodes positions
def get_pos(G):
    return {(i, j): (j, -i) for i, j in G.nodes()}

#Get nodes labels
def get_labels(G):
    labels = {}
    i=1
    for n in G.nodes():
        labels[n] = i
        i+=1
    return labels