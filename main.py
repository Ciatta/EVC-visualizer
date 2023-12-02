
import io
import base64
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
import networkx as nx

from graph_maker import shapes, make_grid, get_pos, get_labels
from vertex_cover import put_guards, move_guards
from graph_animation import animate_node, convert




shape = shapes.triangle
height = 0
width = 0
G = []
G_guards= []
G_edges= []
pos_g={}
pos_g1={}
color = "#B8D4E3"

def main(h, w, s, edge):
    global width, height, shape, G, G_guards,  G_edges, pos_g
    width = w
    height=h
    if (s=='triangle'): shape = shapes.triangle
    elif (s=='square'): shape = shapes.square
    elif (s=='octagon'): shape = shapes.octagon
    elif (s=='hexagon'): shape = shapes.hexagon

    #Make the graphs
    G = make_grid(shape, height, width)
    G_guards = put_guards(shape, G, height, width)
    G_edges = nx.Graph()

    #Get node positions and labels
    pos = get_pos(G)
    pos_g = get_pos(G_guards)
    pos_g1=pos_g.copy()
    labels = get_labels(G)

    #Initialize the plot
    fig, ax = plt.subplots()
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)
    fig.set_facecolor(color)
    fig.subplots_adjust(top=1,bottom=0,left=0,right=1)
    
    #Save the image
    if max(height,width) <= 10: font_size=10
    elif max(height,width) <= 15: font_size=7
    elif max(height,width) <= 20: font_size=5
    anim = animate_node(1, fig, ax, G, pos, G_guards, G_edges, pos_g, pos_g1, labels, font_size)
    anim.save('static/test.png', writer=PillowWriter(fps=10), dpi=200)
    convert("static/test.png", "static/test2.png")
    
    return True
    
   
def defend(edge):
    global width, height, shape, G, G_guards, G_edges, pos_g, pos_g1
    
    #Fix nodes positions
    for k in pos_g:
        pos_g[k]=(round(pos_g[k][0]), round(pos_g[k][1]))
    pos_g1=pos_g.copy()
    
    #Move guards
    G_guards, G_edges, pos_g1, edge_ok = move_guards(shape, G, G_guards, G_edges, pos_g1, edge, height, width)
    
    #Get positons and labels
    pos = get_pos(G)
    labels = get_labels(G)

    #Initialize the plot
    fig, ax = plt.subplots()
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)
    fig.set_facecolor(color)
    fig.subplots_adjust(top=1,bottom=0,left=0,right=1)

    #Save the image
    if max(height,width) <= 10: font_size=10
    elif max(height,width) <= 15: font_size=7
    elif max(height,width) <= 20: font_size=5
    anim = animate_node(12, fig, ax, G, pos, G_guards, G_edges, pos_g, pos_g1, labels, font_size)
    anim.save('static/anim.gif', writer=PillowWriter(fps=10), dpi=200)
    convert("static/anim.gif", "static/anim2.gif")
    
    return edge_ok
   


    