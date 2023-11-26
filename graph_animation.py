from matplotlib.animation import FuncAnimation
import networkx as nx
from PIL import Image
import io

loop=1
dir = []
def animate_node(n_frames, fig, ax, G, pos, G_guards, G_edges, pos_g, pos_g1, labels, font_size):
    global loop, dir
    loop=1
    dir = []
    steps=[0]
    for i in range(n_frames): steps.append(1/n_frames)
    
    animation = FuncAnimation(fig, update, frames=range(n_frames+1), repeat=False, fargs=[steps, fig, ax, G, pos, G_guards, G_edges, pos_g, pos_g1, labels, font_size], )
    return animation


def update(frame, steps, fig, ax, G, pos, G_guards, G_edges, pos_g, pos_g1, labels, font_size):
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
    
    #10, 12 per 10x10
    #5, 7 per 20x20
    nx.draw(G, pos=pos, ax=ax, with_labels=True, labels=labels, node_color="#1E96FC", node_size=40, font_size=font_size)
    nx.draw(G_edges, pos=pos,  ax=ax, node_color="#1E96FC", edge_color="#ff0000", node_size=60, font_size=font_size)
    nx.draw(G_guards, pos=pos_g, ax=ax, node_color="#FFC600", node_size=60, font_size=font_size)
    
   
def convert(old_filename, new_filename, duration):
    images = []
    with Image.open(old_filename) as im:
        for i in range(im.n_frames):
            im.seek(i)
            buf = io.BytesIO()
            im.save(buf, format='png')
            buf.seek(0)
            images.append(Image.open(buf))
    images[0].save(new_filename, save_all=True, append_images=images[1:], optimize=False)