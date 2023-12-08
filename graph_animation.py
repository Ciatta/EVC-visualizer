from matplotlib.animation import FuncAnimation
import networkx as nx
from PIL import Image
import io
import matplotlib.pyplot as plt
from graph_maker import shapes

loop=1
dir = []
#Move the guards according to current position and previous position
def animate_node(n_frames, fig, ax, G, pos, G_guards, G_edges, G_last_edge, pos_g, pos_g1, labels, font_size, shape):
    global loop, dir
    loop=1
    dir = []
    steps=[0]
    for i in range(n_frames): steps.append(1/n_frames)
    
    animation = FuncAnimation(fig, update, frames=range(n_frames+1), repeat=False, fargs=[steps, shape, ax, G, pos, G_guards, G_edges, G_last_edge, pos_g, pos_g1, labels, font_size], )
    return animation

#Update function for each frame
def update(frame, steps, shape, ax, G, pos, G_guards, G_edges, G_last_edge, pos_g, pos_g1, labels, font_size):
    global loop, dir
    # Clear the previous frame
    ax.clear()
    if loop==1:
        for x,y in G_guards: dir.append(tuple(map(lambda i, j: i - j, pos_g1[(x,y)], pos_g[(x,y)])))
            
    guards = list(G_guards.nodes())
    for i in range(len(guards)):
        guard = guards[i]
        d = dir[i]
        pos_g[guard] = (pos_g[guard][0]+steps[frame]*d[0], pos_g[guard][1]+steps[frame]*d[1])
    loop+=1
    
    node_color = "#1E96FC"
    guards_color = "#FFC600"
    att_edge_color = "#ff0000"
    att_edge_color_past = "#b30000"
    nx.draw(G, pos=pos, ax=ax, with_labels=True, labels=labels, node_color=node_color, node_size=70, font_size=font_size, font_weight="bold")
    nx.draw(G_edges, pos=pos, ax=ax, node_color=node_color, edge_color=att_edge_color_past, node_size=70, font_size=font_size, font_weight="bold")
    nx.draw(G_last_edge, pos=pos, ax=ax, node_color=node_color, edge_color=att_edge_color, node_size=70, font_size=font_size, font_weight="bold")
    nx.draw(G_guards, pos=pos_g, ax=ax, node_color=guards_color, node_size=80, font_size=font_size, font_weight="bold")
    edg = list(G_last_edge.edges())
    print(edg)
    if edg!=[] and shape==shapes.octagon:
        x1=min(edg[0][0][1], edg[0][1][1])
        x2=max(edg[0][0][1], edg[0][1][1])
        if x1==x2 and x1%2!=0:
            x1=x2-1
        plt.axvspan(x1-0.2, x2+0.2, 0.05, 0.95, color='red', alpha=0.1)
    
#Make the gif loop only once   
def convert(old_filename, new_filename):
    images = []
    with Image.open(old_filename) as im:
        for i in range(im.n_frames):
            im.seek(i)
            buf = io.BytesIO()
            im.save(buf, format='png')
            buf.seek(0)
            images.append(Image.open(buf))
    images[0].save(new_filename, save_all=True, append_images=images[1:], optimize=False)