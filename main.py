
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
pos_g={}
pos_g1={}
color = "#bfdef3"

def main(h, w, s, edge):
    global width, height, shape, G, G_guards, pos_g
    width = w
    height=h
    if (s=='triangle'): shape = shapes.triangle
    elif (s=='square'): shape = shapes.square
    elif (s=='octagon'): shape = shapes.octagon
    elif (s=='hexagon'): shape = shapes.hexagon
    

    
    G = make_grid(shape, height, width)
    G_guards = put_guards(shape, G, height, width)

    pos = get_pos(G)
    pos_g = get_pos(G_guards)
    pos_g1=pos_g.copy()

    labels = get_labels(G)

    fig, ax = plt.subplots()
   
    # turn off axis spines
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)
    fig.set_facecolor(color)
   
    fig.tight_layout()
    if max(height,width) <= 10: font_size=10
    elif max(height,width) <= 15: font_size=7
    elif max(height,width) <= 20: font_size=5
   
    anim = animate_node(1, fig, ax, G, pos, G_guards, pos_g, pos_g1, labels, font_size)
    anim.save('static/test.png', writer=PillowWriter(fps=10), dpi=200)
    convert("static/test.png", "static/test2.png", 100)
    """
    fig, ax = plt.subplots()
    nx.draw(G, pos=pos, ax=ax, with_labels=True, labels=labels, node_color="gray", node_size=40, font_size=10)
    nx.draw(G_guards, pos=pos_g, ax=ax, node_color="blue", node_size=40, font_size=12)
    plt.gca().set_aspect('equal')
    plt.savefig("static/test.png", format='png', bbox_inches='tight', transparent="True", dpi=300)
    plt.close
    # Save the plot to a bytes object
   
    #plt.figure(figsize=(100,60))
    """


    return "yes"
    
   
def defend(edge):
    global width, height, shape, G, G_guards, pos_g, pos_g1
    for k in pos_g:
        pos_g[k]=(round(pos_g[k][0]), round(pos_g[k][1]))
    pos_g1=pos_g.copy()
    
   
    G_guards, pos_g1, edge_ok = move_guards(shape, G, G_guards, pos_g1, edge, height, width)
    
    pos = get_pos(G)
    labels = get_labels(G)
    fig, ax = plt.subplots()
    if max(height,width) <= 10: font_size=10
    elif max(height,width) <= 15: font_size=7
    elif max(height,width) <= 20: font_size=5
    anim = animate_node(12, fig, ax, G, pos, G_guards, pos_g, pos_g1, labels, font_size)
    # turn off axis spines
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)
    fig.set_facecolor(color)
    fig.tight_layout()
   
    anim.save('static/anim.gif', writer=PillowWriter(fps=10), dpi=200)
    convert("static/anim.gif", "static/anim2.gif", 100)
    return edge_ok
    """
    fig, ax = plt.subplots()
    nx.draw(G, pos=pos, ax=ax, with_labels=True, labels=labels, node_color="gray", node_size=40, font_size=10)
    nx.draw(G_guards, pos=pos_g1, ax=ax, node_color="blue", edge_color="red", node_size=40, font_size=12)
    plt.gca().set_aspect('equal')
    #plt.savefig("static/anim2.gif", format='png', bbox_inches='tight', transparent="True", dpi=300)
    plt.close
    """
    


    