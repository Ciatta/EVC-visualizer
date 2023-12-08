from graph_maker import shapes, get_labels, get_pos
import networkx as nx

"""
Put guards on the initial configuration
"""
def put_guards(shape, G, h, w):
    if (shape == shapes.hexagon): return put_guards_h(G, h, w)
    elif (shape == shapes.triangle): return put_guards_t(G, h, w)
    elif (shape == shapes.octagon): return put_guards_o(G, h, w)
    elif (shape == shapes.square): return put_guards_s(G, h, w)
    
"""
Put guards on the initial configuration on hexagonal grids
"""
def put_guards_h(G, h, w):
    guards = []
    for node in G:
        if node[0]%2 == 0:
            guards.append(node)
    G_guards = nx.Graph()
    G_guards.add_nodes_from(guards)
    return G_guards

"""
Put guards on the initial configuration on triangular grids
"""
def put_guards_t(G, h, w):
    guards = []
    sy = h%3
    for node in G:
        i = node[0]- sy
        j = node[1]
        if j%3==0 and i%3 == 0:
            guards.append(node)
        elif (j+1)%3==0 and (i)%3 == 0:
            guards.append(node)
        elif (j+2)%3==0 and (i+2)%3 == 0:
            guards.append(node)
        elif (j)%3==0 and (i+2)%3 == 0:
            guards.append(node)
        elif (j+2)%3==0 and (i+1)%3 == 0:
            guards.append(node)
        elif (j+1)%3==0 and (i+1)%3 == 0:
            guards.append(node)
        if w!=2 and h!=2:
            if node[1]==w-1 and w%3==1: guards.append(node)
            elif node[1]==w-2 and w%3==2: guards.append(node)
            if node[0]==0 and h%3==1: guards.append(node)
            elif node[0]==1 and h%3==2: guards.append(node)
        
    G_guards = nx.Graph()
    G_guards.add_nodes_from(guards)
    return G_guards

"""
Put guards on the initial configuration on octagonal grids
"""
def put_guards_o(G, h, w):
    guards=[]
    for node in G:
        if node[0]%2 == 0:
            guards.append(node)
        else:
            if node[1]%2 == 0:
                guards.append(node)
    G_guards = nx.Graph()
    G_guards.add_nodes_from(guards)
    return G_guards

"""
Put guards on the initial configuration on square grids
"""
def put_guards_s(G, h, w):
    guards = []
    for node in G:
        if node[0]%2 == 0:
          if node[1]%2 == 1:
            guards.append(node)
        else:
            if node[1]%2 == 0:
                guards.append(node)
    G_guards = nx.Graph()
    G_guards.add_nodes_from(guards)
    return G_guards


"""
Move guards according to the grid type and the attacked edge
"""
def move_guards(shape, G, G_guards, G_edges, G_last_edge, pos, edge, h, w):
    #get the edge
    edge = edge[1:-1].split(",")
    try: x=int(edge[0])
    except: return G_guards, G_edges, G_last_edge, pos, False
    try: y=int(edge[1])
    except: return G_guards, G_edges, G_last_edge, pos, False
    #map edge label to id
    labels = get_labels(G)
    x_n=list(labels.keys())[x-1]
    y_n=list(labels.keys())[y-1]
    edge = (x_n, y_n)
    #check if the edge is valid
    if not G.has_edge(x_n, y_n): return G_guards, G_edges, G_last_edge, pos, False
    #execute the move guards algorithm according to the grid type
    if (shape == shapes.hexagon): return move_guards_h(G, G_guards, G_edges, G_last_edge, pos, edge, h, w)
    elif (shape == shapes.triangle): return move_guards_t(G, G_guards, G_edges, G_last_edge, pos, edge, h, w)
    elif (shape == shapes.octagon): return move_guards_o(G, G_guards, G_edges, G_last_edge, pos, edge, h, w)
    elif (shape == shapes.square): return move_guards_s(G, G_guards, G_edges, G_last_edge, pos, edge, h, w)

"""
Algoritm to move guards on a hexagonal grids
"""
def move_guards_h(G, G_guards, G_edges, G_last_edge, pos, edge, h, w):
    #define the 4 cases, if the h is odd or even, step 1 or 2 and combine them
    G_edges.add_edge(edge[0], edge[1])
    G_last_edge=nx.Graph()
    G_last_edge.add_edge(edge[0], edge[1])
    pos_nodes = get_pos(G)
    if pos_nodes[edge[0]] in list(pos.values()):
        pos1 = pos_nodes[(edge[0][0],edge[0][1])]
        pos2 = pos_nodes[(edge[1][0],edge[1][1])]
     
    else:
        pos1 = pos_nodes[(edge[1][0],edge[1][1])]
        pos2 = pos_nodes[(edge[0][0],edge[0][1])]
    # guards on even y cases
    case1 = (pos2[0]==pos1[0] and pos2[1]==pos1[1]+1)
    case2 = (pos2[0]==pos1[0] and pos2[1]==pos1[1]-1)
    case3 = (pos2[0]==pos1[0]+1 and pos2[1]==pos1[1]-1)
    case4 = (pos2[0]==pos1[0]-1 and pos2[1]==pos1[1]-1)
    # guards on odd y cases
    case1b = (pos2[0]==pos1[0] and pos2[1]==pos1[1]-1)
    case2b = (pos2[0]==pos1[0] and pos2[1]==pos1[1]+1)
    case3b = (pos2[0]==pos1[0]+1 and pos2[1]==pos1[1]+1)
    case4b = (pos2[0]==pos1[0]-1 and pos2[1]==pos1[1]+1)

    mul4 = h%4==0
    s1 = pos[(0,0)][1]%2==0
    
    # move guards according to the cases
    for x,y in G_guards.nodes():
        posg = pos[(x,y)]
        #Guards on even y 
        if s1:
            if case1:
                #guard
                if posg == pos1: pos[(x,y)] = pos2
                #posg[x] <= pos1[x]-1
                elif posg[0]<=pos1[0]-1:
                    if posg[1]==-h+2:
                        if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        else: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                    else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                #posg[x] = pos1[x]
                elif posg[0]==pos1[0]:
                    if posg[1]==-h+2:
                        if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                    elif posg[1]==0: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                    else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                #posg[x] >= pos1[x]+1
                elif posg[0]>=pos1[0]+1:
                    if posg[1]==-h+2:
                        if mul4: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]-1)
                        else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                    elif posg[1]==0: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                    else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
            
            if case2:
                #guard
                if posg == pos1: pos[(x,y)] = pos2
                #posg[x] <= pos1[x]-1
                elif posg[0]<=pos1[0]-1:
                    if posg[0]==pos1[0]-1:
                        if pos1[1]==-h+2 or pos1[0]==w-1:
                            print("caso 1")
                            if posg[1]==0:
                                if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                                else: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                            elif posg[1]==-h+2:
                                if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                                else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                            else: 
                                if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                                else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        else:
                            if posg[1]==0:
                                pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                            elif posg[1]==-h+2:
                                if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                                else: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                            else: 
                                pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                    else:
                        if posg[1]==-h+2:
                            if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                            else: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                        else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                #posg[x] = pos1[x]
                elif posg[0]==pos1[0]:
                    if posg[1]==0:
                        if pos1[1]==-h+2 or pos1[0]==w-1:
                            print("caso 2")
                            if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                            else: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                        else:
                            pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                    elif posg[1]==-h+2:
                        if pos1[0]==w-1: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        else:
                            if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                            else: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                    else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                #posg[x] >= pos1[x]+1
                elif posg[0]>=pos1[0]+1:
                    if posg[0]==pos1[0]+1:
                        if pos1[1]==-h+2 or pos1[0]==w-1:
                            print("caso 3")
                            if posg[1]==0:
                                pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                            elif posg[1]==-h+2:
                                if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                                else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                            else: 
                                if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                                else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        else:
                            if posg[1]==0:
                                pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                            elif posg[1]==-h+2:
                                pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                            else: 
                                pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                    else:
                        if posg[1]==0:
                           pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                        elif posg[1]==-h+2:
                            if mul4: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]-1)
                            else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
            
            if case3:
                #guard
                if posg == pos1: pos[(x,y)] = pos2
                #posg[x] <= pos1[x]-1
                elif posg[0]<=pos1[0]-1:
                    if posg[1]==-h+2:
                        if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        else: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                    else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                #posg[x] = pos1[x]
                elif posg[0]==pos1[0]:
                    if posg[1]==-h+2:
                        if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        else: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                    elif posg[1]==0:
                        if mul4: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                        else: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                    else:
                        if (-posg[1])%4==0: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                        else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)           
                #posg[x] >= pos1[x]+1
                elif posg[0]>=pos1[0]+1:
                    if posg[0]==pos1[0]+1:
                        if posg[1]==0:
                            pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                        elif posg[1]==-h+2:
                            if mul4: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]-1)
                            else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        else:
                            if ((-posg[1])-2)%4==0: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]-1)
                            else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                    else:
                        if posg[1]==0:
                            pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                        elif posg[1]==-h+2:
                            if mul4: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]-1)
                            else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        else: 
                            pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
            
            if case4:
                #guard
                if posg == pos1: pos[(x,y)] = pos2
                #posg[x] <= pos1[x]-1
                elif posg[0]<=pos1[0]-1:
                    if posg[0]==pos1[0]-1:
                        if posg[1]==0:
                            pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                        elif posg[1]==-h+2:
                            if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                            else: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                        else:
                            if (-posg[1])%4==0: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                            else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                    else:
                        if posg[1]==-h+2:
                            if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                            else: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                        else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)        
                #posg[x] = pos1[x]
                elif posg[0]==pos1[0]:
                    if posg[1]==0:
                            pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                    elif posg[1]==-h+2:
                        if mul4: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]-1)
                        else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                    else:
                        if ((-posg[1])-2)%4==0: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]-1)
                        else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                #posg[x] >= pos1[x]+1
                elif posg[0]>=pos1[0]+1:
                    if posg[1]==0:
                        pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                    elif posg[1]==-h+2:
                        if mul4: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]-1)
                        else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                    else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
        
        #guards on odd y
        else:
            if case1b:
                #guard
                if posg == pos1: pos[(x,y)] = pos2
                #posg[x] <= pos1[x]-1
                elif posg[0]<=pos1[0]-1:
                    if posg[1]==-h+1:
                        if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        else: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                    else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                #posg[x] = pos1[x]
                elif posg[0]==pos1[0]:
                    if posg[1]==-h+1:
                        if mul4: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                        else: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                    else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                #posg[x] >= pos1[x]+1
                elif posg[0]>=pos1[0]+1:
                    if posg[1]==-h+1:
                        if mul4: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                        else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                    elif posg[1]==-1: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                    else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
            
            if case2b:
                #guard
                if posg == pos1: pos[(x,y)] = pos2
                #posg[x] <= pos1[x]-1
                elif posg[0]<=pos1[0]-1:
                    if posg[0]==pos1[0]-1:
                        if pos1[1]==-h+1 or pos1[0]==w-1:
                            if posg[1]==-1:
                                if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                                else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                            elif posg[1]==-h+1:
                                if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                                else: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                            else: 
                                if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                                else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        else:
                            if posg[1]==-1:
                                pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                            elif posg[1]==-h+1:
                                if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                                else: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                            else: 
                                pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                    else:
                        if posg[1]==-h+1:
                            if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                            else: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                        else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                #posg[x] = pos1[x]
                #TO DO: dividi in sottocasi
                elif posg[0]==pos1[0]:
                    if posg[1]==-1:
                        if pos1[1]==-h+1 or pos1[0]==w-1:
                            if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                            else: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                        else:
                            pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                    elif posg[1]==-h+1:
                        if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        else: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                    else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                #posg[x] >= pos1[x]+1
                elif posg[0]>=pos1[0]+1:
                    if posg[0]==pos1[0]+1:
                        if pos1[1]==-h+1 or pos1[0]==w-1:
                            if posg[1]==-1:
                                if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                                else: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                            elif posg[1]==-h+1:
                                if mul4: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                                else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                            else: 
                                if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                                else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        else:
                            if posg[1]==-1:
                                pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                            elif posg[1]==-h+1:
                                if mul4: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                                else: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                            else: 
                                pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                    else:
                        if posg[1]==-1:
                           pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                        elif posg[1]==-h+1:
                            if mul4: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                            else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
            
            if case3b:
                #guard
                if posg == pos1: pos[(x,y)] = pos2
                #posg[x] <= pos1[x]-1
                elif posg[0]<=pos1[0]-1:
                    if posg[1]==-h+1:
                        if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        else: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                    else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                #posg[x] = pos1[x]
                elif posg[0]==pos1[0]:
                    if posg[1]==-h+1:
                        if mul4: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                        else: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                    elif posg[1]==-1:
                        if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                    else:
                        if ((-posg[1])+1)%4==0: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                        else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1) 
                #posg[x] >= pos1[x]+1
                elif posg[0]>=pos1[0]+1:
                    if posg[0]==pos1[0]+1:
                        if posg[1]==-1:
                            pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                        elif posg[1]==-h+1:
                            if mul4: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                            else: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                        else:
                            if ((-posg[1])+3)%4==0: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                            else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                    else:
                        if posg[1]==-1:
                            pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                        elif posg[1]==-h+1:
                            if mul4: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                            else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        else: 
                            pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
            
            if case4b:
                #guard
                if posg == pos1: pos[(x,y)] = pos2
                #posg[x] = pos1[x]-1
                elif posg[0]<=pos1[0]-1:
                    if posg[0]==pos1[0]-1:
                        if posg[1]==-1:
                            pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        elif posg[1]==-h+1:
                            if mul4: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                            else: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                        else:
                            if ((-posg[1])+1)%4==0: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                            else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                    else:
                        if posg[1]==-h+1:
                            if mul4: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                            else: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                        else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)  
                #posg[x] = pos1[x]
                elif posg[0]==pos1[0]:
                    if posg[1]==-1:
                            pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                    elif posg[1]==-h+1:
                        if mul4: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                        else: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                    else:
                        if ((-posg[1])-1)%4==0: pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                        else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                #posg[x] >= pos1[x]+1
                elif posg[0]>=pos1[0]+1:
                    if posg[1]==-1:
                        pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                    elif posg[1]==-h+1:
                        if mul4: pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                        else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                    else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)

    return G_guards, G_edges, G_last_edge, pos, True

"""
Algoritm to move guards on a triangular grids
"""
def move_guards_t (G, G_guards, G_edges, G_last_edge, pos, edge, h, w):
    G_edges.add_edge(edge[0], edge[1])
    G_last_edge=nx.Graph()
    G_last_edge.add_edge(edge[0], edge[1])
    pos_nodes = get_pos(G)
    s1 = (0,0) in list(pos.values())

    #strategies that map each guard to its movement ((None,None) means that there is no guards in that position)
    intile_s1 ={1: [(1,0), (None,None), (0,0), (0,0), (1,0), (None,None), (None,None), (-1,0), (-1,0)],
                2: [(0,-1), (None,None), (0,0), (1,1), (-1,-1), (None,None), (None,None), (0,0), (0,1)],
                3: [(0,-1), (None,None), (-1,0), (0,-1), (1,1), (None,None), (None,None), (0,0), (0,1)],
                4: [(1,0), (None,None), (0,-1), (0,0), (1,1), (None,None), (None,None), (-1,0), (-1,0)],
                5: [(0,-1), (None,None), (0,0), (0,-1), (0,1), (None,None), (None,None), (1,1), (-1,0)]}
    intile_s2 ={1: [(None,None), (-1,0), (0,0), (0,0), (None,None), (0,-1), (1,1), (0,0), (None,None)],
                2: [(None,None), (-1,0), (0,0), (1,0), (None,None), (0,-1), (1,0), (0,0), (None,None)],
                3: [(None,None), (-1,0), (0,0), (0,0), (None,None), (0,-1), (1,0), (0,1), (None,None)],
                4: [(None,None), (1,0), (-1,-1), (0,1), (None,None), (0,-1), (0,1), (0,0), (None,None)],
                5: [(None,None), (0,-1), (0,0), (0,1), (None,None), (0,-1), (0,1), (0,0), (None,None)],
                6: [(None,None), (-1,0), (0,0), (0,0), (None,None), (-1,0), (1,0), (1,0), (None,None)]}
   
    bet_tiles_y_s1={1: [(1,0), (None, None), (0,0), (0,0), (1,0), (None, None), (None, None), (0,0), (-1,-1),
                        (0,1), (None, None), (0,0), (0,0), (-1,-1), (None, None), (None, None), (0,0), (0,1)],
                    2: [(1,0), (None, None), (0,0), (0,0), (1,0), (None, None), (None, None), (0,-1), (-1,0),
                        (0,1), (None, None), (0,0), (0,0), (-1,-1), (None, None), (None, None), (0,0), (0,1)]}
    bet_tiles_y_s2={1: [(None, None), (-1,0), (0,0), (0,0), (None, None), (-1,0), (0,-1), (0,0), (None, None),
                        (None, None), (1,1), (0,0), (0,0), (None, None), (0,-1), (1,1), (0,0), (None, None)],
                    2: [(None, None), (-1,0), (0,0), (0,0), (None, None), (-1,0), (1,0), (-1,-1), (None, None),
                        (None, None), (1,1), (0,0), (0,0), (None, None), (0,-1), (1,1), (0,0), (None, None)],
                    3: [(None, None), (0,0), (-1,-1), (0,1), (None, None), (0,0), (0,0), (-1,-1), (None, None),
                        (None, None), (0,0), (0,1), (1,0), (None, None), (0,0), (0,0), (1,0), (None, None)]}
    
    bet_tiles_x_s1={1: [(1,0), (None, None), (0,0), (-1,-1), (None, None), (0,0),
                        (0,0), (-1,-1), (None, None), (0,0), (0,1), (None, None),
                        (None, None), (0,0), (1,0), (None, None), (0,0), (0,1)],
                    2: [(1,0), (None, None), (0,0), (0,-1), (None, None), (0,0),
                        (0,0), (-1,-1), (None, None), (-1,0), (0,1), (None, None),
                        (None, None), (0,0), (1,0), (None, None), (0,0), (0,1)]}
    bet_tiles_x_s2={1: [(None, None), (-1,0), (0,0), (None, None), (0,-1), (0,0),
                        (0,0), (None, None), (1,1), (-1,-1), (None, None), (0,-1),
                        (1,1), (0,0), (None, None), (0,1), (0,0), (None, None)],
                    2: [(None, None), (-1,0), (0,0), (None, None), (0,-1), (0,0),
                        (0,0), (None, None), (1,1), (0,0), (None, None), (0,-1),
                        (1,1), (0,0), (None, None), (-1,0), (0,0), (None, None)],
                    3: [(None, None), (0,0), (1,0), (None, None), (0,0), (-1,-1),
                        (0,1), (None, None), (0,0), (-1,-1), (None, None), (0,0),
                        (0,0), (0,1), (None, None), (0,0), (1,0), (None, None)]}
    
    stripe_tile_x_s1={1: [(1,0), (None, None), (0,0), (-1,-1), (0,0), (-1,-1),
                          (None, None), (0,1), (None, None), (0,0), (1,0), (0,1)],
                      2: [(1,0), (None, None), (0,0), (0,0), (0,0), (-1,-1),
                           (None, None), (-1,0), (None, None), (0,0), (1,0), (0,1)]}
    stripe_tile_x_s2={1: [(None, None), (-1,0), (0,0), (0,0), (0,0), (None, None),
                          (1,0), (-1,-1), (1,1), (0,0), (None, None), (0,0)],
                      2: [(None, None), (-1,0), (0,0), (0,0), (0,0), (None, None),
                          (1,0), (0,-1), (1,1), (0,0), (None,None), (-1,0)]}
    
    stripe_tile_y_s1={1: [(1,0), (1,0), (-1,-1), (0,1), (None,None), (0,0), 
                          (0,0), (-1,-1), (None,None), (None,None), (0,0), (0,1)],
                      2: [(1,0), (0,-1), (0,0), (0,1), (None,None), (0,0),
                          (0,0), (-1,-1), (None,None), (None,None), (0,0), (0,1)]}
    stripe_tile_y_s2={1: [(0,0), (-1,-1), (0,0), (None,None), (0,1), (0,0),
                          (0,0), (None,None), (0,-1), (1,1), (0,0), (None,None)],
                      2: [(0,-1), (-1,0), (0,0), (None,None), (0,1), (0,0),
                          (0,0), (None,None), (0,-1), (1,1), (0,0), (None,None)]}
    
    stripe_h2_s1 ={1:[(0,-1), (0,0), (None,None), (0,-1), (0,0), (None,None),
                        (None,None), (1,1), (0,0), (None,None), (1,1), (0,0)],
                     2:[(1,0), (-1,-1), (None,None), (-1,-1), (0,0), (None,None),
                        (None,None), (1,1), (1,0), (None,None), (1,0), (0,1)],
                     3:[(1,0), (1,0), (None,None), (1,0), (1,0), (None,None),
                        (None,None), (-1,0), (0,0), (None,None), (-1,0), (0,0)],
                     4:[(0,-1), (0,0), (None,None), (-1,0), (1,0), (None,None),
                        (None,None), (1,0), (1,0), (None,None), (0,1), (0,0)],
                     5:[(0,-1), (1,0), (None,None), (1,0), (-1,-1), (None,None),
                        (None,None), (0,1), (0,0), (None,None), (1,1), (0,0)],
                     6:[(0,-1), (0,0), (None,None), (1,0), (1,0), (None,None),
                        (None,None), (1,0), (0,1), (None,None), (-1,0), (0,0)]}
    stripe_h2_s2 ={1:[(None,None), (0,0), (-1,-1), (None,None), (0,0), (-1,-1),
                        (0,1), (None,None), (0,0), (0,1), (None,None), (0,0)],
                     2:[(None,None), (-1,0), (-1,-1), (None,None), (0,0), (0,-1),
                        (1,1), (None,None), (1,1), (-1,0), (None,None), (-1,0)],
                     3:[(None,None), (-1,0), (-1,0), (None,None), (-1,0), (-1,0),
                        (1,0), (None,None), (0,0), (1,0), (None,None), (0,0)],
                     4:[(None,None), (0,0), (1,0), (None,None), (0,-1), (-1,0),
                        (0,1), (None,None), (-1,0), (-1,0), (None,None), (0,0)],
                     5:[(None,None), (0,-1), (-1,0), (None,None), (-1,0), (-1,-1),
                        (0,1), (None,None), (0,0), (1,1), (None,None), (0,0)],
                     6:[(None,None), (0,0), (0,-1), (None,None), (-1,0), (-1,0),
                        (0,1), (None,None), (-1,0), (1,0), (None,None), (0,0)]}
    
    in_stripe_y_s1 ={1:[(0,-1), (0,0), (None,None), (0,-1), (0,0), (None,None),
                        (1,0), (1,1), (0,0), (1,0), (1,1), (0,0)],
                     2:[(1,0), (-1,-1), (None,None), (-1,-1), (0,0), (None,None),
                        (1,0), (1,1), (1,0), (1,0), (1,0), (0,1)],
                     3:[(1,0), (1,0), (None,None), (1,0), (1,0), (None,None),
                        (0,0), (0,0), (0,0), (0,0), (0,0), (0,0)],
                     4:[(0,-1), (0,0), (None,None), (-1,0), (1,0), (None,None),
                        (1,0), (1,0), (1,0), (1,0), (0,1), (0,0)],
                     5:[(0,-1), (1,0), (None,None), (1,0), (-1,-1), (None,None),
                        (1,0), (0,1), (0,0), (1,0), (1,1), (0,0)],
                     6:[(0,-1), (0,0), (None,None), (1,0), (1,0), (None,None),
                        (1,0), (1,0), (0,1), (0,0), (0,0), (0,0)]}
    in_stripe_y_s2 ={1:[(None,None), (0,0), (-1,-1), (None,None), (0,0), (-1,-1),
                        (0,1), (-1,0), (0,0), (0,1), (-1,0), (0,0)],
                     2:[(None,None), (-1,0), (-1,-1), (None,None), (0,0), (0,-1),
                        (1,1), (-1,0), (1,1), (-1,0), (-1,0), (-1,0)],
                     3:[(None,None), (-1,0), (-1,0), (None,None), (-1,0), (-1,0),
                        (0,0), (0,0), (0,0), (0,0), (0,0), (0,0)],
                     4:[(None,None), (0,0), (1,0), (None,None), (0,-1), (-1,0),
                        (0,1), (-1,0), (-1,0), (-1,0), (-1,0), (0,0)],
                     5:[(None,None), (0,-1), (-1,0), (None,None), (-1,0), (-1,-1),
                        (0,1), (-1,0), (0,0), (1,1), (-1,0), (0,0)],
                     6:[(None,None), (0,0), (0,-1), (None,None), (-1,0), (-1,0),
                        (0,1), (-1,0), (-1,0), (0,0), (0,0), (0,0)]}
    
    stripe_w2_s1={1:[(1,0), (None,None), (0,0), (-1,-1), (None,None), (0,0),
                       (1,0), (None,None), (0,0), (-1,-1), (None,None), (0,0)],
                    2:[(0,-1), (None,None), (0,-1), (0,1), (None,None), (0,0),
                       (0,-1), (None,None), (0,-1), (0,1), (None,None), (0,0)],
                    3:[(1,0), (None,None), (0,-1), (-1,0), (None,None), (0,0),
                       (0,-1), (None,None), (1,1), (-1,-1), (None,None), (0,0)],
                    4:[(0,-1), (None,None), (1,1), (-1,-1), (None,None), (0,-1),
                       (1,1), (None,None), (0,0), (0,-1), (None,None), (-1,0)],
                    5:[(1,0), (None,None), (0,0), (0,-1), (None,None), (0,-1),
                       (0,1), (None,None), (0,-1), (-1,0), (None,None), (0,0)],
                    6:[(1,0), (None,None), (0,0), (0,-1), (None,None), (-1,0),
                       (0,-1), (None,None), (0,-1), (0,1), (None,None), (0,0)]}
    stripe_w2_s2={1:[(None,None), (-1,0), (0,0), (None,None), (1,1), (0,0),
                       (None,None), (-1,0), (0,0), (None,None), (1,1), (0,0),],
                    2:[(None,None), (0,-1), (0,1), (None,None), (0,1), (0,0),
                       (None,None), (0,-1), (0,1), (None,None), (0,1), (0,0)],
                    3:[(None,None), (-1,0), (1,0), (None,None), (0,1), (0,0),
                       (None,None), (-1,-1), (0,1), (None,None), (1,1), (0,0)],
                    4:[(None,None), (-1,-1), (0,1), (None,None), (1,1), (-1,-1),
                       (None,None), (0,1), (0,0), (None,None), (1,0), (0,1)],
                    5:[(None,None), (-1,0), (0,0), (None,None), (0,-1), (0,1),
                       (None,None), (0,1), (1,0), (None,None), (0,1), (0,0)],
                    6:[(None,None), (-1,0), (0,0), (None,None), (1,0), (0,1),
                       (None,None), (0,-1), (0,1), (None,None), (0,1), (0,0)]}

    in_stripe_x_s1={1:[(1,0), (None,None), (0,1), (-1,-1), (0,1), (0,0),
                       (1,0), (None,None), (0,1), (-1,-1), (0,1), (0,0)],
                    2:[(0,0), (None,None), (0,0), (0,1), (0,0), (0,0),
                       (0,0), (None,None), (0,0), (0,1), (0,0), (0,0)],
                    3:[(1,0), (None,None), (0,1), (-1,0), (0,0), (0,0),
                       (0,0), (None,None), (1,1), (-1,-1), (0,1), (0,0)],
                    4:[(0,0), (None,None), (1,1), (-1,-1), (0,1), (0,-1),
                       (1,1), (None,None), (0,1), (0,-1), (0,1), (-1,0)],
                    5:[(1,0), (None,None), (0,1), (0,-1), (0,1), (0,-1),
                       (0,1), (None,None), (0,1), (-1,0), (0,0), (0,0)],
                    6:[(1,0), (None,None), (0,1), (0,-1), (0,1), (-1,0),
                       (0,0), (None,None), (0,0), (0,1), (0,0), (0,0)]}
    in_stripe_x_s2={1:[(0,-1), (-1,0), (0,-1), (None,None), (1,1), (0,0),
                       (0,-1), (-1,0), (0,-1), (None,None), (1,1), (0,0)],
                    2:[(0,0), (0,-1), (0,0), (None,None), (0,0), (0,0),
                       (0,0), (0,-1), (0,0), (None,None), (0,0), (0,0)],
                    3:[(0,-1), (-1,0), (0,0), (None,None), (0,0), (0,0),
                       (0,0), (-1,-1), (0,-1), (None,None), (1,1), (0,0)],
                    4:[(0,0), (-1,-1), (0,-1), (None,None), (1,1), (-1,-1),
                       (0,-1), (0,1), (0,-1), (None,None), (1,0), (0,1)],
                    5:[(0,-1), (-1,0), (0,-1), (None,None), (0,-1), (0,1),
                       (0,-1), (0,1), (1,0), (None,None), (0,0), (0,0)],
                    6:[(0,-1), (-1,0), (0,-1), (None,None), (1,0), (0,1),
                       (0,0), (0,-1), (0,0), (None,None), (0,0), (0,0)]}
    

    if pos_nodes[edge[0]] in list(pos.values()):
        pos1 = pos_nodes[(edge[0][0],edge[0][1])]
        pos2 = pos_nodes[(edge[1][0],edge[1][1])]
    else:
        pos1 = pos_nodes[(edge[1][0],edge[1][1])]
        pos2 = pos_nodes[(edge[0][0],edge[0][1])]

    stripe_y = h%3
    stripe_x = w%3
    tiles_y = h//3
    tiles_x = w//3
   
    #find where the attacked edge is
    easy_case = False
    in_stripe_y = False
    stripe_tile_y = False
    bet_tiles_y = False
    in_stripe_x = False
    stripe_tile_x = False
    bet_tiles_x = False
    in_tile = False
    h_2 = False
    w_2 = False

    easy_case = pos_nodes[edge[0]] in list(pos.values()) and pos_nodes[edge[1]] in list(pos.values())
    #graph height is 2
    if h==2: h_2 =True
    #attacked edge is a between stripe and tile
    elif stripe_y == 1 and (pos1[1]==0 or pos2[0]==0):
        stripe_tile_y = True
        print("------------between stripe and tile------------")
    elif stripe_y == 2 and ((pos1[1]==-1 and pos2[1]==-2) or (pos2[1]==-1 and pos1[1]==-2)):
        stripe_tile_y = True
        print("------------between stripe and tile------------")
    #attacked edge is inside the orizontal stripe
    elif stripe_y ==2 and (pos1[1]==0 or pos1[1]==-1) and (pos2[1]==0 or pos2[1]==-1):
        in_stripe_y = True
        print("------------inside stripe y------------")
    else:
        for i in range(tiles_y):
            #attacked edge is between two tiles
            if (pos1[1]==-h+3*(i+1) and pos2[1]==pos1[1]+1) or (pos2[1]==-h+3*(i+1) and pos1[1]==pos2[1]+1):
                bet_tiles_y = True
                print("------------between tiles y------------")
                break
            #attacked edge is inside a tile
            else:
                in_tile = True   
                print("------------inside tile------------")
                break

    #graph width is 2
    if w==2: w_2 =True
    #attacked edge is a between stripe and tile
    elif stripe_x == 1 and (pos1[0]==w-1 or pos2[0]==w-1):
        stripe_tile_x = True
        print("------------between stripe and tile------------")
    elif stripe_x == 2 and ((pos1[0]==w-2 and pos2[0]==w-3) or (pos1[0]==w-3 and pos2[0]==w-2)):
        stripe_tile_x = True
        print("------------between stripe and tile------------")
    #attacked edge is inside the vertical stripe
    elif stripe_x ==2 and (pos1[0]==w-1 or pos1[0]==w-2) and (pos2[0]==w-1 or pos2[0]==w-2):
        in_stripe_x = True
        print("------------inside stripe x------------")
    else:
        for i in range(tiles_x):
            #attacked edge is between two tiles
            if (pos1[0]==3*(i+1)-1 and pos2[0]==pos1[0]+1) or (pos2[0]==3*(i+1)-1 and pos1[0]==pos2[0]+1):
                bet_tiles_x = True
                print("------------between tiles x------------")
                break
            #attacked edge is inside a tile
            else:
                in_tile = True   
                print("------------inside tile------------")
                break

    #chose the correct strategy according to the attacked edge
    dir_e = (pos2[0]-pos1[0], pos2[1]-pos1[1])
    strat = []
    #graph height is 2
    if h_2:
        x0 = pos1[0]//3*3
        y0 = -((-pos1[1]-stripe_y)//3*3)-stripe_y
       
        tile_12 = [(0, 0), (1,0), (2,0), (3, 0),(4, 0), (5,0),
                   (0, -1), (1,-1), (2,-1), (3, -1),(4, -1), (5,-1)]
       
        i_t = tile_12.index((pos1[0]%6, pos1[1]))
        if s1:
            print("s1")
            stripe_h2_s1
            for l in list(stripe_h2_s1.values()):
                if l[i_t]==dir_e:
                    strat = l       
        else:
            print("s2")
            for l in list(stripe_h2_s2.values()):
                if l[i_t]==dir_e:
                    strat = l
    #graph width is 2
    elif w_2:
        x0 = pos1[0]//3*3
        y0 = -((-pos1[1]-stripe_y)//3*3)-stripe_y
       
        tile_12 = [(w-2,0), (w-1,0), (w-2,1), (w-1,1), (w-2,2), (w-1,2),
                   (w-2,3), (w-1,3), (w-2,4), (w-1,4), (w-2,5), (w-1,5)]
        i_t = tile_12.index((pos1[0], -pos1[1]-stripe_y%6))
        print(tile_12)
        print(pos1)
        print((pos1[0], -pos1[1]-stripe_y%6))
        print(i_t, dir_e)
        if s1:
            for l in list(stripe_w2_s1.values()): 
                if l[i_t]==dir_e:
                    strat = l       
        else:
            for l in list(stripe_w2_s2.values()):
                if l[i_t]==dir_e:
                    strat = l
    #attacked edge is the orizontal stripe
    elif in_stripe_y:
        x0 = pos1[0]//3*3
        y0 = -((-pos1[1]-stripe_y)//3*3)-stripe_y
       
        tile_12 = [(0, 0), (1,0), (2,0), (3, 0),(4, 0), (5,0),
                   (0, -1), (1,-1), (2,-1), (3, -1),(4, -1), (5,-1)]
       
        i_t = tile_12.index((pos1[0]%6, pos1[1]))
        if s1:
            print("s1")
            for l in list(in_stripe_y_s1.values()):
                if l[i_t]==dir_e:
                    strat = l       
        else:
            print("s2")
            for l in list(in_stripe_y_s2.values()):
                if l[i_t]==dir_e:
                    strat = l
    #attacked edge is the vertical stripe
    elif in_stripe_x:
        x0 = pos1[0]//3*3
        y0 = -((-pos1[1]-stripe_y)//3*3)-stripe_y
       
        tile_12 = [(w-2,0), (w-1,0), (w-2,1), (w-1,1), (w-2,2), (w-1,2),
                   (w-2,3), (w-1,3), (w-2,4), (w-1,4), (w-2,5), (w-1,5)]
        i_t = tile_12.index((pos1[0], -pos1[1]-stripe_y%6))
        print(tile_12)
        print(pos1)
        print((pos1[0], -pos1[1]-stripe_y%6))
        print(i_t, dir_e)
        if s1:
            print("s1")
            for l in list(in_stripe_x_s1.values()):
                if l[i_t]==dir_e:
                    print("found")
                    strat = l       
        else:
            print("s2")
            for l in list(in_stripe_x_s2.values()):
                if l[i_t]==dir_e:
                    print("found")
                    strat = l
        print(strat)
    #attacked edge is between a stripe and a tile
    elif stripe_tile_x:
        x0 = pos1[0]//3*3
        y0 = -((-pos1[1]-stripe_y)//3*3)-stripe_y
        if dir_e[0]==1:
            tile_12 = [(x0, y0), (x0+1,y0), (x0+2,y0), (x0+3, y0),
                       (x0, y0-1), (x0+1,y0-1), (x0+2,y0-1), (x0+3, y0-1),
                       (x0, y0-2), (x0+1,y0-2), (x0+2,y0-2), (x0+3, y0-2)]
        else:
            tile_12 = [(x0-3, y0), (x0-2,y0), (x0-1,y0), (x0, y0),
                       (x0-3, y0-1), (x0-2,y0-1), (x0-1,y0-1), (x0, y0-1),
                       (x0-3, y0-2), (x0-2,y0-2), (x0-1,y0-2), (x0, y0-2)]
        i_t = tile_12.index(pos1)
        if s1:
            print("s1")
            for l in list(stripe_tile_x_s1.values()):
                if l[i_t]==dir_e:
                    strat = l       
        else:
            print("s2")
            for l in list(stripe_tile_x_s2.values()):
                if l[i_t]==dir_e:
                    strat = l
    #attacked edge is between a stripe and a tile
    elif stripe_tile_y:
        x0 = pos1[0]//3*3
        y0 = -((-pos1[1]-stripe_y)//3*3)-stripe_y
        if dir_e[1]==1:
            tile_12 = [(x0, 0-stripe_y+1), (x0+1,0-stripe_y+1), (x0+2,0-stripe_y+1), (x0, -1-stripe_y+1), (x0+1,-1-stripe_y+1), (x0+2,-1-stripe_y+1),
                       (x0, -2-stripe_y+1), (x0+1,-2-stripe_y+1), (x0+2,-2-stripe_y+1), (x0, -3-stripe_y+1), (x0+1,-3-stripe_y+1), (x0+2,-3-stripe_y+1)]
        else:
            tile_12 = [(x0, 0-stripe_y+1), (x0+1,0-stripe_y+1), (x0+2,0-stripe_y+1), (x0, -1-stripe_y+1), (x0+1,-1-stripe_y+1), (x0+2,-1-stripe_y+1),
                       (x0, -2-stripe_y+1), (x0+1,-2-stripe_y+1), (x0+2,-2-stripe_y+1), (x0, -3-stripe_y+1), (x0+1,-3-stripe_y+1), (x0+2,-3-stripe_y+1)]
        i_t = tile_12.index(pos1)
        if s1:
            print("s1")
            for l in list(stripe_tile_y_s1.values()):
                if l[i_t]==dir_e:
                    strat = l       
        else:
            print("s2")
            for l in list(stripe_tile_y_s2.values()):
                if l[i_t]==dir_e:
                    strat = l
    #attacked edge is between two tiles
    elif bet_tiles_y:
        x0 = pos1[0]//3*3
        y0 = -((-pos1[1]-stripe_y)//3*3)-stripe_y
        if dir_e[1]==-1:
            tile_18 = [(x0, y0), (x0+1,y0), (x0+2,y0), (x0, y0-1), (x0+1,y0-1), (x0+2,y0-1), (x0, y0-2), (x0+1,y0-2), (x0+2,y0-2),
                    (x0, y0-3), (x0+1,y0-3), (x0+2,y0-3), (x0, y0-4), (x0+1,y0-4), (x0+2,y0-4), (x0, y0-5), (x0+1,y0-5), (x0+2,y0-5)]
        else:
            tile_18 = [(x0, y0+3), (x0+1,y0+3), (x0+2,y0+3), (x0, y0+2), (x0+1,y0+2), (x0+2,y0+2), (x0, y0+1), (x0+1,y0+1), (x0+2,y0+1),
                    (x0, y0), (x0+1,y0), (x0+2,y0), (x0, y0-1), (x0+1,y0-1), (x0+2,y0-1), (x0, y0-2), (x0+1,y0-2), (x0+2,y0-2)]
        i_t = tile_18.index(pos1)
        if s1:
            print("s1")
            for l in list(bet_tiles_y_s1.values()):
                if l[i_t]==dir_e:
                    strat = l       
        else:
            print("s2")
            for l in list(bet_tiles_y_s2.values()):
                if l[i_t]==dir_e:
                    strat = l
    #attacked edge is between two tiles
    elif bet_tiles_x:
        x0 = pos1[0]//3*3
        y0 = -((-pos1[1]-stripe_y)//3*3)-stripe_y
        if dir_e[0]==1:
            tile_18 = [(x0, y0), (x0+1,y0), (x0+2,y0), (x0+3,y0), (x0+4,y0), (x0+5,y0), 
                       (x0, y0-1), (x0+1,y0-1), (x0+2,y0-1), (x0+3,y0-1), (x0+4,y0-1), (x0+5,y0-1), 
                       (x0, y0-2), (x0+1,y0-2), (x0+2,y0-2), (x0+3,y0-2), (x0+4,y0-2), (x0+5,y0-2)
                    ]
        else:
            tile_18 = [(x0-3, y0),(x0-2, y0), (x0-1, y0), (x0,y0), (x0+1, y0), (x0+2, y0),
                       (x0-3, y0-1),(x0-2, y0-1), (x0-1, y0-1), (x0,y0-1), (x0+1, y0-1), (x0+2, y0-1),
                       (x0-3, y0-2),(x0-2, y0-2), (x0-1, y0-2), (x0,y0-2), (x0+1, y0-2), (x0+2, y0-2)]
        i_t = tile_18.index(pos1)
        if s1:
            print("s1")
            for l in list(bet_tiles_x_s1.values()):
                if l[i_t]==dir_e:
                    strat = l       
        else:
            print("s2")
            for l in list(bet_tiles_x_s2.values()):
                if l[i_t]==dir_e:
                    strat = l
    #attacked edge is inside a tile
    elif in_tile:
        x0 = pos1[0]//3*3
        y0 = -((-pos1[1]-stripe_y)//3*3)-stripe_y
        tile = [(x0, y0), (x0+1,y0), (x0+2,y0), (x0, y0-1), (x0+1,y0-1), (x0+2,y0-1), (x0, y0-2), (x0+1,y0-2), (x0+2,y0-2)]
        i_t = tile.index(pos1)
        if s1:
            print("s1")
            for l in list(intile_s1.values()):
                if l[i_t]==dir_e:
                    strat = l       
        else:
            print("s2")
            for l in list(intile_s2.values()):
                if l[i_t]==dir_e:
                    strat = l

    #move each guard according to the correct strategy
    for x,y in G_guards.nodes():
        #graph height is 2
        if h_2:
            print(tile_12)
            print(strat)
            for i in range(len(strat)):
                if (pos[(x,y)][0]%6, pos[(x,y)][1]) == tile_12[i]:
                    pos[(x,y)] = (pos[(x,y)][0]+strat[i][0], pos[(x,y)][1]+strat[i][1])
                    break
        #graph width is 2
        elif w_2:
            print(tile_12)
            for i in range(len(strat)):
                    if (pos[(x,y)][0], -pos[(x,y)][1]-stripe_y%6) == tile_12[i]:
                        if strat[i]!=(None,None):
                            pos[(x,y)] = (pos[(x,y)][0]+strat[i][0], pos[(x,y)][1]+strat[i][1])
                            break
        #guards are in both ends of the edge                    
        elif easy_case:
            if pos[(x,y)]==pos1: pos[(x,y)]=pos2
            elif pos[(x,y)]==pos2: pos[(x,y)]=pos1
        #attacked edge is the orizontal stripe
        elif in_stripe_y:
            if (pos[(x,y)][1]==0 or pos[(x,y)][1]==-1) and pos[(x,y)][0]<w-stripe_x:
                for i in range(len(strat)):
                    if (pos[(x,y)][0]%6, pos[(x,y)][1]) == tile_12[i]:
                        if pos[(x,y)][0]+strat[i][0]<h and strat[i]!=(None,None):
                            pos[(x,y)] = (pos[(x,y)][0]+strat[i][0], pos[(x,y)][1]+strat[i][1])
                            break
            elif pos[(x,y)][0]>=w-stripe_x: 
                tile = [(w-2,0), (w-1,0), (w-2,1), (w-1,1), (w-2,2), (w-1,2),
                        (w-2,3), (w-1,3), (w-2,4), (w-1,4), (w-2,5), (w-1,5)]
                if s1: l_strat= in_stripe_x_s1[2]
                else: l_strat = in_stripe_x_s2[2]
                for i in range(len(l_strat)):
                    if (pos[(x,y)][0], -pos[(x,y)][1]-stripe_y%6) == tile[i]:
                        if l_strat[i]!=(None,None):
                            pos[(x,y)] = (pos[(x,y)][0]+l_strat[i][0], pos[(x,y)][1]+l_strat[i][1])
                            break
                continue
            else:
                x0 = pos[(x,y)][0]//3*3
                y0 = -((-pos[(x,y)][1]-stripe_y)//3*3)-stripe_y
                tile = [(x0, y0), (x0+1,y0), (x0+2,y0), (x0, y0-1), (x0+1,y0-1), (x0+2,y0-1), (x0, y0-2), (x0+1,y0-2), (x0+2,y0-2)]
                if s1: l_strat2= intile_s1[1]
                else: l_strat2 = intile_s2[1]
                for i in range(len(l_strat2)):
                    if pos[(x,y)] == tile[i] and l_strat2[i]!=(None,None):
                        pos[(x,y)] = (pos[(x,y)][0]+l_strat2[i][0], pos[(x,y)][1]+l_strat2[i][1])
                        break
        #attacked edge is the vertical stripe
        elif in_stripe_x:
            print(pos[(x,y)])
            if (pos[(x,y)][1]==0 or pos[(x,y)][1]==-1) and pos[(x,y)][0]<w-stripe_x:
                tile = [(0, 0), (1,0), (2,0), (3, 0),(4, 0), (5,0),
                        (0, -1), (1,-1), (2,-1), (3, -1),(4, -1), (5,-1)]
                if s1: l_strat= in_stripe_y_s1[3]
                else: l_strat = in_stripe_y_s2[3]
                for i in range(len(l_strat)):
                    if (pos[(x,y)][0]%6, pos[(x,y)][1]) == tile[i]:
                        if l_strat[i]!=(None,None):
                            if pos[(x,y)][0]+l_strat[i][0]<h:
                                pos[(x,y)] = (pos[(x,y)][0]+l_strat[i][0], pos[(x,y)][1]+l_strat[i][1])
                                break
            elif pos[(x,y)][0]==w-2 or pos[(x,y)][0]==w-1:
                print(strat)
                for i in range(len(strat)):
                    if (pos[(x,y)][0], -pos[(x,y)][1]-stripe_y%6) == tile_12[i]:
                        if strat[i]!=(None,None):
                            pos[(x,y)] = (pos[(x,y)][0]+strat[i][0], pos[(x,y)][1]+strat[i][1])
                            break
            else:
                x0 = pos[(x,y)][0]//3*3
                y0 = -((-pos[(x,y)][1]-stripe_y)//3*3)-stripe_y
                tile = [(x0, y0), (x0+1,y0), (x0+2,y0), (x0, y0-1), (x0+1,y0-1), (x0+2,y0-1), (x0, y0-2), (x0+1,y0-2), (x0+2,y0-2)]
                if s1: l_strat2= intile_s1[1]
                else: l_strat2 = intile_s2[1]
                for i in range(len(l_strat)):
                    if pos[(x,y)] == tile[i] and l_strat2[i]!=(None,None):
                        pos[(x,y)] = (pos[(x,y)][0]+l_strat2[i][0], pos[(x,y)][1]+l_strat2[i][1])
                        break
        #attacked edge is between a stripe and a tile
        elif stripe_tile_x or stripe_tile_y:  
            if pos[(x,y)] in tile_12:
                print(tile_12)
                if stripe_tile_y or stripe_tile_x:
                    for i in range(len(strat)):
                        if pos[(x,y)] == tile_12[i] and strat[i]!=(None,None):
                            pos[(x,y)] = (pos[(x,y)][0]+strat[i][0], pos[(x,y)][1]+strat[i][1])
                            break
            elif pos[(x,y)][1]>=-(stripe_y-1) and pos[(x,y)][0]<w-stripe_x:
                if stripe_y==1: continue
                tile = [(0, 0), (1,0), (2,0), (3, 0),(4, 0), (5,0),
                        (0, -1), (1,-1), (2,-1), (3, -1),(4, -1), (5,-1)]
                if s1: l_strat= in_stripe_y_s1[3]
                else: l_strat = in_stripe_y_s2[3]
                for i in range(len(l_strat)):
                    if (pos[(x,y)][0]%6, pos[(x,y)][1]) == tile[i]:
                        if l_strat[i]!=(None,None):
                            if pos[(x,y)][0]+l_strat[i][0]<h:
                                pos[(x,y)] = (pos[(x,y)][0]+l_strat[i][0], pos[(x,y)][1]+l_strat[i][1])
                            break
            elif pos[(x,y)][0]>=w-stripe_x:
                if stripe_x==1: continue
                tile = [(w-2,0), (w-1,0), (w-2,1), (w-1,1), (w-2,2), (w-1,2),
                        (w-2,3), (w-1,3), (w-2,4), (w-1,4), (w-2,5), (w-1,5)]
                if s1: l_strat2= in_stripe_x_s1[2]
                else: l_strat2 = in_stripe_x_s2[2]
                for i in range(len(l_strat2)):
                    if (pos[(x,y)][0], -pos[(x,y)][1]-stripe_y%6) == tile[i]:
                        if l_strat2[i]!=(None,None):
                            pos[(x,y)] = (pos[(x,y)][0]+l_strat2[i][0], pos[(x,y)][1]+l_strat2[i][1])
                            break
                continue
            else:
                x0 = pos[(x,y)][0]//3*3
                y0 = -((-pos[(x,y)][1]-stripe_y)//3*3)-stripe_y
                tile = [(x0, y0), (x0+1,y0), (x0+2,y0), (x0, y0-1), (x0+1,y0-1), (x0+2,y0-1), (x0, y0-2), (x0+1,y0-2), (x0+2,y0-2)]
                if s1: l_strat3= intile_s1[1]
                else: l_strat3 = intile_s2[1]
                for i in range(len(l_strat3)):
                    if pos[(x,y)] == tile[i] and l_strat3[i]!=(None,None):
                        pos[(x,y)] = (pos[(x,y)][0]+l_strat3[i][0], pos[(x,y)][1]+l_strat3[i][1])
                        break
        #attacked edge is between two tiles
        elif bet_tiles_y or bet_tiles_x:
            if pos[(x,y)] in tile_18:
                for i in range(len(strat)):
                    if pos[(x,y)] == tile_18[i] and strat[i]!=(None,None):
                        pos[(x,y)] = (pos[(x,y)][0]+strat[i][0], pos[(x,y)][1]+strat[i][1])
                        break
            elif pos[(x,y)][1]>=-(stripe_y-1):
                if stripe_y==1: continue
                tile = [(0, 0), (1,0), (2,0), (3, 0),(4, 0), (5,0),
                        (0, -1), (1,-1), (2,-1), (3, -1),(4, -1), (5,-1)]
                if s1: l_strat2= in_stripe_y_s1[3]
                else: l_strat2 = in_stripe_y_s2[3]
                for i in range(len(l_strat2)):
                    if (pos[(x,y)][0]%6, pos[(x,y)][1]) == tile[i]:
                        
                        if l_strat2[i]!=(None,None):
                            if pos[(x,y)][0]+l_strat2[i][0]<h:
                                pos[(x,y)] = (pos[(x,y)][0]+l_strat2[i][0], pos[(x,y)][1]+l_strat2[i][1])
                            break
            elif pos[(x,y)][0]>=w-stripe_x:
                if stripe_x==1: continue
                tile = [(w-2,0), (w-1,0), (w-2,1), (w-1,1), (w-2,2), (w-1,2),
                        (w-2,3), (w-1,3), (w-2,4), (w-1,4), (w-2,5), (w-1,5)]
                if s1: l_strat3= in_stripe_x_s1[2]
                else: l_strat3 = in_stripe_x_s2[2]
                for i in range(len(l_strat3)):
                    if (pos[(x,y)][0], -pos[(x,y)][1]-stripe_y%6) == tile[i]:
                        if l_strat3[i]!=(None,None):
                            pos[(x,y)] = (pos[(x,y)][0]+l_strat3[i][0], pos[(x,y)][1]+l_strat3[i][1])
                            break
                continue
            else:
                x0 = pos[(x,y)][0]//3*3
                y0 = -((-pos[(x,y)][1]-stripe_y)//3*3)-stripe_y
                tile = [(x0, y0), (x0+1,y0), (x0+2,y0), (x0, y0-1), (x0+1,y0-1), (x0+2,y0-1), (x0, y0-2), (x0+1,y0-2), (x0+2,y0-2)]
                if s1: l_strat4= intile_s1[1]
                else: l_strat4 = intile_s2[1]
                for i in range(len(l_strat4)):
                    if pos[(x,y)] == tile[i] and l_strat4[i]!=(None,None):
                        pos[(x,y)] = (pos[(x,y)][0]+l_strat4[i][0], pos[(x,y)][1]+l_strat4[i][1])
                        break
        #attacked edge is inside a tile
        elif in_tile:
            if pos[(x,y)][1]>=-(stripe_y-1):
                if stripe_y==1: continue
                tile = [(0, 0), (1,0), (2,0), (3, 0), (4, 0), (5,0),
                        (0,-1), (1,-1), (2,-1), (3,-1), (4,-1), (5,-1)]
                if s1: l_strat= in_stripe_y_s1[3]
                else: l_strat = in_stripe_y_s2[3]
                for i in range(len(l_strat)):
                    if (pos[(x,y)][0]%6, pos[(x,y)][1]) == tile[i]:
                        if l_strat[i]!=(None,None):
                            if pos[(x,y)][0]+l_strat[i][0]<w:
                                pos[(x,y)] = (pos[(x,y)][0]+l_strat[i][0], pos[(x,y)][1]+l_strat[i][1])
                                break
            elif pos[(x,y)][0]>=w-stripe_x:
                if stripe_x==1: continue
                tile = [(w-2,0), (w-1,0), (w-2,1), (w-1,1), (w-2,2), (w-1,2),
                        (w-2,3), (w-1,3), (w-2,4), (w-1,4), (w-2,5), (w-1,5)]
                if s1: l_strat2= in_stripe_x_s1[2]
                else: l_strat2 = in_stripe_x_s2[2]
                for i in range(len(l_strat2)):
                    if (pos[(x,y)][0], -pos[(x,y)][1]-stripe_y%6) == tile[i]:
                        if l_strat2[i]!=(None,None):
                            pos[(x,y)] = (pos[(x,y)][0]+l_strat2[i][0], pos[(x,y)][1]+l_strat2[i][1])
                            break
            else:
                x0 = pos[(x,y)][0]//3*3
                y0 = -((-pos[(x,y)][1]-stripe_y)//3*3)-stripe_y
                tile = [(x0, y0), (x0+1,y0), (x0+2,y0), (x0, y0-1), (x0+1,y0-1), (x0+2,y0-1), (x0, y0-2), (x0+1,y0-2), (x0+2,y0-2)]
                for i in range(len(strat)):
                    if pos[(x,y)] == tile[i] and strat[i]!=(None,None):
                        pos[(x,y)] = (pos[(x,y)][0]+strat[i][0], pos[(x,y)][1]+strat[i][1])
                        break

    return G_guards, G_edges, G_last_edge, pos, True


"""
Algoritm to move guards on a octagonal grids
"""                                   
def move_guards_o (G, G_guards, G_edges, G_last_edge, pos, edge, h, w):
    G_edges.add_edge(edge[0], edge[1])
    G_last_edge=nx.Graph()
    G_last_edge.add_edge(edge[0], edge[1])
    pos_nodes = get_pos(G)
    if pos_nodes[edge[0]] in list(pos.values()):
        pos1 = pos_nodes[(edge[0][0],edge[0][1])]
        pos2 = pos_nodes[(edge[1][0],edge[1][1])]
    else:
        pos1 = pos_nodes[(edge[1][0],edge[1][1])]
        pos2 = pos_nodes[(edge[0][0],edge[0][1])]

    easy_case = (pos_nodes[edge[0]] in list(pos.values()) and pos_nodes[edge[1]] in list(pos.values())) 
    case1 = (pos1[0]%2==0 and (pos2[1]==pos1[1]+1 or pos2[1]==pos1[1]-1))  
    case2 = (pos1[0]%2==0 and pos2[1]==pos1[1])   
    case3 = (pos1[0]%2==1 and pos2[0]==pos1[0])   
    casea = ((pos2[0],-1) in list(pos.values()))
    caseb = ((pos2[0],0) in list(pos.values()))

    #move the guards according to the cases
    for x,y in G_guards.nodes():
        dir_x = pos2[0]-pos1[0]
        if easy_case:
            if pos[(x,y)]==pos1: pos[(x,y)]=pos2
            elif pos[(x,y)]==pos2: pos[(x,y)]=pos1

        elif case1:
            if casea:
                #guard
                if pos[(x,y)] == pos1: pos[(x,y)] = pos2
                #SA
                elif pos[(x,y)][0]==pos1[0] and pos[(x,y)][1]<pos1[1]:
                    if pos[(x,y)][1]+1<=0:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                #SB
                elif pos[(x,y)][0]==pos1[0] and pos[(x,y)][1]>pos1[1]:
                    continue
                #SC
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]<pos2[1]:
                    if pos[(x,y)][1]==-h+1: pos[(x,y)] = (pos[(x,y)][0]-dir_x, pos[(x,y)][1])
                    elif pos[(x,y)][1]-1>-h: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                #SD
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]>pos2[1]:
                    if pos[(x,y)][1]+1<=0:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
            elif caseb:
                #guard
                if pos[(x,y)] == pos1: pos[(x,y)] = pos2
                #SA
                elif pos[(x,y)][0]==pos1[0] and pos[(x,y)][1]<pos1[1]:
                    continue
                #SB
                elif pos[(x,y)][0]==pos1[0] and pos[(x,y)][1]>pos1[1]:
                    if pos[(x,y)][1]-1>-h:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                #SC
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]<pos2[1]:
                    if pos[(x,y)][1]-1>-h:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                #SD
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]>pos2[1]:
                    if pos[x,y][1]==0: pos[(x,y)] = (pos[(x,y)][0]-dir_x, pos[(x,y)][1])
                    elif pos[(x,y)][1]+1<=0: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
        
        elif case2:
            if casea:
                #guard
                if pos[(x,y)] == pos1: pos[(x,y)] = pos2
                #SA
                elif pos[(x,y)][0]==pos1[0] and pos[(x,y)][1]<pos1[1]:
                    if pos[(x,y)][1]+1<=0:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                #SB
                elif pos[(x,y)][0]==pos1[0] and pos[(x,y)][1]>pos1[1]:
                    continue
                #SC
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]<pos2[1]:
                    if pos[(x,y)][1]==-h+1:
                        pos[(x,y)] = (pos[(x,y)][0]-dir_x, pos[(x,y)][1])
                    else:
                        if pos[(x,y)][1]-1>-h: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                #SD
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]>pos2[1]:
                    if pos[(x,y)][1]+1<=0:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
            elif caseb:
                #guard
                if pos[(x,y)] == pos1: pos[(x,y)] = pos2
                #SA
                elif pos[(x,y)][0]==pos1[0] and pos[(x,y)][1]<pos1[1]:
                    continue
                #SB
                elif pos[(x,y)][0]==pos1[0] and pos[(x,y)][1]>pos1[1]:
                    if pos[(x,y)][1]-1>-h:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                #SC
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]<pos2[1]:
                    if pos[(x,y)][1]-1>-h:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                #SD
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]>pos2[1]:
                    if pos[(x,y)][1]==0:
                        pos[(x,y)] = (pos[(x,y)][0]-dir_x, pos[(x,y)][1])
                    else:
                        if pos[(x,y)][1]+1<=0:
                            pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
        
        elif case3:
            if casea:
                #guard
                if pos[(x,y)] == pos1: pos[(x,y)] = pos2
                #SA
                elif pos[(x,y)][0]==pos1[0]-1 and pos[(x,y)][1]<pos1[1]:
                    if pos1[1]-pos2[1]==-1:
                        if pos[(x,y)][1]==pos1[1]-1:
                            pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1])
                        elif pos[(x,y)][1]+1<=0: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                    elif pos[(x,y)][1]+1<=0:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)

                #SB
                elif pos[(x,y)][0]==pos1[0]-1 and pos[(x,y)][1]>=pos1[1]:
                    if pos1[1]-pos2[1]==1:
                        if pos[(x,y)][1]==0:
                            pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1])
                        elif pos[(x,y)][1]+1<=0:
                            pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                #SC
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]<pos2[1]:
                    if pos[(x,y)][1]==-h+1:
                        pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1])
                    elif pos[(x,y)][1]-1>-h: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                #SD
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]>pos2[1]:
                    if pos1[1]-pos2[1]==-1:
                        if pos[(x,y)][1]+1<=0:
                            pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                    elif pos[(x,y)][1]-1>-h:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                    print("SD")
            elif caseb:
                #guard
                if pos[(x,y)] == pos1: pos[(x,y)] = pos2
                #SA
                elif pos[(x,y)][0]==pos1[0]-1 and pos[(x,y)][1]<=pos1[1]:
                    if pos1[1]-pos2[1]==-1:
                        if pos[(x,y)][1]==-h+1:
                            pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1])
                        else:
                            if pos[(x,y)][1]-1>-h: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                #SB
                elif pos[(x,y)][0]==pos1[0]-1 and pos[(x,y)][1]>pos1[1]:
                    if pos1[1]-pos2[1]==1:
                        if pos[(x,y)][1]==pos1[1]+1:
                            pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1])
                        else:
                            if pos[(x,y)][1]-1>-h: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                    else:
                        if pos[(x,y)][1]-1>-h: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                #SC
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]<pos2[1]:
                    if pos1[1]-pos2[1]==1:
                        if pos[(x,y)][1]-1>-h:
                            pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                    else:
                        if pos[(x,y)][1]+1<=0: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                #SD
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]>pos2[1]:
                    
                    if pos[(x,y)][1]==0:
                        pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1])
                    else:
                        if pos[(x,y)][1]+1<=0: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
    
    return G_guards, G_edges, G_last_edge, pos, True


"""
Algoritm to move guards on a square grids
"""
def move_guards_s (G, G_guards, G_edges, G_last_edge, pos, edge, h, w):
    G_edges.add_edge(edge[0], edge[1])
    G_last_edge=nx.Graph()
    G_last_edge.add_edge(edge[0], edge[1])
    pos_nodes = get_pos(G)
    if pos_nodes[edge[0]] in list(pos.values()):
        pos1 = pos_nodes[(edge[0][0],edge[0][1])]
        pos2 = pos_nodes[(edge[1][0],edge[1][1])]
    else:
        pos1 = pos_nodes[(edge[1][0],edge[1][1])]
        pos2 = pos_nodes[(edge[0][0],edge[0][1])]
    #if egde is vertical find the hamiltonian cycle on rotate the graph
    if pos1[1]!=pos2[1]:
        G1 = nx.grid_2d_graph(w, h, periodic=False)
        #map the attacked edge on the rotated graph
        edge1=((edge[0][1], w-edge[0][0]-1), (edge[1][1], w-edge[1][0]-1))
        cycle1 = hamilton(G1, edge1)
        cycle=[]
        #rotate back the resulting cycle
        for (x,y) in cycle1: cycle.append((w-1-y, x))
    #if egde is horizontal find the hamiltonian cycle on base the graph
    else: cycle = hamilton(G, edge)
    pos_cycle = []
    #find positions of the nodes
    for node in cycle:
        pos_cycle.append(pos_nodes[node])
    #get the direction of the cycle
    dir = pos_cycle.index(pos2)-pos_cycle.index(pos1)
    #move the guards along the hamiltonian cycle
    for x,y in G_guards.nodes():
        i = pos_cycle.index(pos[(x,y)])
        if dir == 1:
            if i==len(pos_cycle)-1:
                pos[(x,y)]=pos_cycle[0]
            else:
                pos[(x,y)]=pos_cycle[i+1]
        elif dir == -1:
            if i==0:
                pos[(x,y)]=pos_cycle[-1]
            else:
                pos[(x,y)]=pos_cycle[i-1]
    return G_guards, G_edges, G_last_edge, pos, True


"""
Hamiltonian path algorithm: https://gist.github.com/mikkelam/ab7966e7ab1c441f947b
modified to be a cycle going thought the attacked edge
"""
def hamilton(G, edge):
    F = [(G,[list(G.nodes())[0]])]
    n = G.number_of_nodes()
    while F:
        graph,path = F.pop()
        confs = []
        neighbors = (node for node in graph.neighbors(path[-1])
                     if node != path[-1]) #exclude self loops
        for neighbor in neighbors:
            conf_p = path[:]
            conf_p.append(neighbor)
            conf_g = nx.Graph(graph)
            conf_g.remove_node(path[-1])
            confs.append((conf_g,conf_p))
        for g,p in confs:
            if len(p)==n:
                i1 = p.index(edge[0])
                i2 = p.index(edge[1])
                #check if goes thought the edge
                if abs(i1-i2)==1 or abs(i1-i2)==n-1:
                    #check if is a cycle
                    if abs(p[0][0]-p[-1][0])<=1 and abs(p[0][0]-p[-1][0])>=-1:
                        if abs(p[0][1]-p[-1][1])<=1 and abs(p[0][1]-p[-1][1])>=-1:
                            return p
            else:
                F.append((g,p))
    return None