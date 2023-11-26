from graph_maker import shapes, get_labels, get_pos
import networkx as nx
import matplotlib.pyplot as plt

def put_guards(shape, G, h, w):
    if (shape == shapes.hexagon): return put_guards_h(G, h, w)
    elif (shape == shapes.triangle): return put_guards_t(G, h, w)
    elif (shape == shapes.octagon): return put_guards_o(G, h, w)
    elif (shape == shapes.square): return put_guards_s(G, h, w)
    

def put_guards_h(G, h, w):
    guards = []
    for node in G:
        if node[0]%2 == 0:
            guards.append(node)
    G_guards = nx.Graph()
    G_guards.add_nodes_from(guards)
    return G_guards

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
            if node[1]==w-1 and w%3==1:
                guards.append(node)
            elif node[1]==w-2 and w%3==2:
                guards.append(node)
        
            if node[0]==0 and h%3==1:
                guards.append(node)
            elif node[0]==1 and h%3==2:
                guards.append(node)
        
    G_guards = nx.Graph()
    G_guards.add_nodes_from(guards)
    return G_guards

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



def move_guards(shape, G, G_guards, G_edges, pos, edge, h, w):
    edge = edge[1:-1].split(",")
    x = int(edge[0]); y=int(edge[1])

    labels = get_labels(G)
    x_n=list(labels.keys())[x-1]; y_n=list(labels.keys())[y-1]; 
    #G_guards.add_edge(x_n, y_n)

    if not G.has_edge(x_n, y_n): return G_guards, G_edges, pos, False
    edge = (x_n, y_n)
    if (shape == shapes.hexagon): return move_guards_h(G, G_guards, G_edges, pos, edge, h, w)
    elif (shape == shapes.triangle): return move_guards_t(G, G_guards, G_edges, pos, edge, h, w)
    elif (shape == shapes.octagon): return move_guards_o(G, G_guards, G_edges, pos, edge, h, w)
    elif (shape == shapes.square): return move_guards_s(G, G_guards, G_edges, pos, edge, h, w)

def move_guards_h(G, G_guards, G_edges, pos, edge, h, w):
    G_edges.add_edge(edge[0], edge[1])
    pos_nodes = get_pos(G)
    if pos_nodes[edge[0]] in list(pos.values()):
        pos1 = pos_nodes[(edge[0][0],edge[0][1])]
        pos2 = pos_nodes[(edge[1][0],edge[1][1])]
     
    else:
        pos1 = pos_nodes[(edge[1][0],edge[1][1])]
        pos2 = pos_nodes[(edge[0][0],edge[0][1])]

    
    case1 = (pos2[0]==pos1[0] and pos2[1]==pos1[1]+1)
    case2 = (pos2[0]==pos1[0] and pos2[1]==pos1[1]-1)
    case3 = (pos2[0]==pos1[0]+1 and pos2[1]==pos1[1]-1)
    case4 = (pos2[0]==pos1[0]-1 and pos2[1]==pos1[1]-1)
    case3b = (pos2[0]==pos1[0]+1 and pos2[1]==pos1[1]+1)
    case4b = (pos2[0]==pos1[0]-1 and pos2[1]==pos1[1]+1)
    case1b = (pos2[0]==pos1[0] and pos2[1]==pos1[1]-1)
    case2b = (pos2[0]==pos1[0] and pos2[1]==pos1[1]+1)

    yg1 = pos[(0,0)][1]
    print(pos1, pos2)
    for x,y in G_guards.nodes():
        posg = pos[(x,y)]
        print("-----------------------------------------------------")
        print(posg)
        
        #Guards on even y
        if yg1%2==0:
            #x = x'-1
            if posg[0]==pos1[0]-1:
                if posg[1]==-h+2 and h%4!=0:
                    pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                elif case4:
                    if posg[1]==-0:
                        pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                        print("a1")
                    elif posg[1]<pos1[1]:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        print("a2")
                    elif posg[1]>=pos1[1]:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        print("a3")
                else:
                    if posg[1]==-h+2 and h%4!=0:
                        pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                        print("a4")
                    else:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        print("a5")
            #x = x'
            elif posg[0]==pos1[0]:
                if case1:
                    if posg[1]>=-h+2 and posg[1]<=-1:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        print("a6")
                    elif posg[1]==0:
                        pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                        print("a7")

                if case2:
                    if posg[1]==-h+2 and h%4!=0:
                        pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                    elif posg[1]!=0:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        print("a8")
                    # added
                    elif posg[1]==0:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        print("a9")

                if case3:
                    if posg[1]<pos1[1]:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        print("a10")
                    elif posg[1]>pos1[1]:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        print("a11")
                    elif posg[1]==pos1[1]:
                        pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                        print("a12")

                if case4:
                    if posg[1]>=-h+2 and posg[1]<=pos1[1]-1:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        print("a13")
                    elif posg[0]==pos1[0] and posg[1]==pos1[1]:
                        pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]-1)
                        print("a14")
                    elif posg[1]==0:
                        pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                        print("a15")
                    else:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        print("a16")

            #x = x'+ 1  
            elif posg[0]==pos1[0]+1:
                if case1:
                    if posg[1]>=-h+3 and posg[1]<=-1:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        print("a17")
                    elif posg[1]==-h+2:
                        pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]-1)
                        print("a18")
                    # added
                    elif posg[1]==0:
                        pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                        print("a19")

                if case2:
                    if posg[1]!=0 and posg[1]!=-h+1:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        print("a20")
                    elif posg[1]==0:
                        pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                        print("a21")

                if case3:
                    if posg[1]==0:
                        pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                        print("a22")
                    elif posg[1]==-h+2 and h%4!=0:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        print("a23")
                    elif posg[1]==-h+2 and h%4==0:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        print("a24")
                    elif posg[1]>=pos1[1]:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        print("a25")
                    elif posg[1]<pos1[1]:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        print("a26")
                      
                
                if case4:
                    if posg[1]==0: 
                        pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                        print("a27")
                    elif posg[1]==-h+2 and h%4==0: 
                        pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]-1)
                        print("a28")
                    elif posg[1]==-h+2 and h%4!=0: 
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        print("a29")
                    else: 
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        print("a30")
                        
            elif posg[0]!=pos1[0] and posg[0]!=pos1[0]-1 and posg[0]!=pos1[0]+1:
                #x < x'- 1
                if posg[0]<pos1[0]:
                    if posg[1]==-h+2 and h%4!=0:
                        pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                        print("a31")
                    else:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        print("a32")
                #x > x'+ 1
                else:
                    if posg[1]==0:
                        pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]-1)
                        print("a33")
                    elif posg[1]==-h+2 and h%4==0:
                        pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]-1)
                        print("a34")
                    else:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        print("a35")
            print(pos[(x,y)])
        
        #Guards on odd y
        else:
            print("step2")
            # x = x'- 1
            if posg[0]==pos1[0]-1:
                if posg[1]==-h+1 and h%4!=0:
                    pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                elif case4b:
                    print("case4")

                    if posg[1]==-h+1:
                        pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                        print("b1")
                    elif posg[1]<=pos1[1]:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        print("b2")
                    elif posg[1]>pos1[1]:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        print("b3")
                else:
                    if posg[1]==-h+1 and h%4!=0:
                        pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                        print("b4")
                    else:
                        if pos1[1]==-h+1 and h%4!=0:
                            pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                            print("b5")
                        else:
                            pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                            print("b6")
            # x = x'
            elif posg[0]==pos1[0]:
                #TO DO: fix this -> edge 1,6 non passa per l'edge -> case sbagliato
                """
                if posg[1]==-h+1 and h%4!=0 and case4b:
                    pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                    print("b7")
                """
                if posg[1]==-h+1 and h%4!=0 and not case2b:
                    pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                    print("b8")
                elif case1b:
                    print("case1")
                    if posg[1]==-h+1:
                        pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                        print("b9")
                    else:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        print("b10")

                elif case2b:
                    print("case2")
                    
                    
                    if pos1[1]==-h+1 and posg[1]==-1 and h%4!=0:
                        pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                        print("b11")
                    elif posg[1]==-1:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        print("b12")
                    elif posg[1]==-h+1 and h%4!=0 and pos1[1]==-h+1:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        print("b13")
                    elif posg[1]==-h+1 and h%4!=0:
                        pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                        print("b14")
                    elif posg[1]!=0:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        print("b15")
                    # added

                elif case3b:
                    print("case3")
                    if posg[1]<pos1[1]:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        print("b16")
                    elif posg[1]>pos1[1]:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        print("b17")
                    elif posg[1]==pos1[1]:
                        pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                        print("b18")

                elif case4b:
                    print("case4")
                    if posg[1]==-h+1:
                        pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                        print("b19")
                    elif posg[1]==pos1[1]:
                        pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                        print("b20")
                    elif posg[1]>pos1[1]:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        print("b21")
                    elif posg[1]<pos1[1]:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        print("b22")
            # x = x'+1      
            elif posg[0]==pos1[0]+1:
                if case1b:
                    print("case1")
                    if posg[1]==-h+1 and h%4!=0:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        print("b23")
                    elif posg[1]==-h+1:
                        pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                        print("b24")
                    # added
                    elif posg[1]==-1:
                        pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                        print("b25")
                    else:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        print("b26")

                if case2b:
                    print("case2")
                    if pos1[1]==-h+1 and posg[1]==-1:
                        pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                        print("b27")
                    elif pos1[1]==-h+1:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        print("b28")
                    elif posg[1]==-h+1 and h%4!=0:
                        pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                        print("b29")
                    elif posg[1]==-h+1:
                        pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                        print("b30")
                    else:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        print("b31")


                if case3b:
                    print("case3")
                    if posg[1]==-h+1 and h%4!=0:
                        pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                        print("b32")
                    elif posg[1]==-1:
                        pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                        print("b33")
                    elif posg[1]==-h+1:
                        pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                        print("b34")
                    elif posg[1]>pos1[1]:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        print("b35")
                    elif posg[1]<=pos1[1]:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                        print("b36")

                
                if case4b:
                    print("case4")
                    if posg[1]==-h+1 and h%4!=0:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        print("b37")
                    elif posg[1]==-1:
                        pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                        print("b38")
                    elif posg[1]==-h+1 and h%4!=0:
                        pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                        print("b39")
                    elif posg[1]==-h+1:
                        pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                        print("b40")
                    else: 
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        print("b41")
                        
            elif posg[0]!=pos1[0] and posg[0]!=pos1[0]-1 and posg[0]!=pos1[0]+1:
                # x < x'- 1
                if posg[0]<pos1[0]:
                    if posg[1]==-h+1 and h%4!=0:
                        pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                        print("b42")
                    else:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        print("b43")
                # x > x'+ 1
                else:
                    if posg[1]==-1:
                        pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1]+1)
                        print("b44")
                    elif posg[1]==-h+1 and h%4==0:
                        pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1]+1)
                        print("b45")
                    else:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                        print("b46")
            pos[(x,y)]
    return G_guards, G_edges, pos, True

s1 = True
def move_guards_t (G, G_guards, G_edges, pos, edge, h, w):
    global s1
    G_edges.add_edge(edge[0], edge[1])
    pos_nodes = get_pos(G)

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
    
    easy_case = False
    if pos_nodes[edge[0]] in list(pos.values()):
        pos1 = pos_nodes[(edge[0][0],edge[0][1])]
        pos2 = pos_nodes[(edge[1][0],edge[1][1])]
    else:
        pos1 = pos_nodes[(edge[1][0],edge[1][1])]
        pos2 = pos_nodes[(edge[0][0],edge[0][1])]

    if pos_nodes[edge[0]] in list(pos.values()) and pos_nodes[edge[1]] in list(pos.values()):
        easy_case=True
    stripe_y = h%3
    stripe_x = w%3
    tiles_y = h//3
    tiles_x = w//3
   
    #fing where the attacked edge is 
    in_stripe_y = False
    stripe_tile_y = False
    bet_tiles_y = False
    in_stripe_x = False
    stripe_tile_x = False
    bet_tiles_x = False
    in_tile = False
    h_2 = False
    w_2 = False
    print(pos1, pos2)
    if h==2: h_2 =True
    elif stripe_y == 1 and (pos1[1]==0 or pos2[0]==0):
        stripe_tile_y = True
        print("------------between stripe and tile------------")
    elif stripe_y == 2 and ((pos1[1]==-1 and pos2[1]==-2) or (pos2[1]==-1 and pos1[1]==-2)):
        stripe_tile_y = True
        print("------------between stripe and tile------------")
    elif stripe_y ==2 and (pos1[1]==0 or pos1[1]==-1) and (pos2[1]==0 or pos2[1]==-1):
        in_stripe_y = True
        print("------------inside stripe y------------")
    else:
        for i in range(tiles_y):
            if (pos1[1]==-h+3*(i+1) and pos2[1]==pos1[1]+1) or (pos2[1]==-h+3*(i+1) and pos1[1]==pos2[1]+1):
                bet_tiles_y = True
                print("------------between tiles y------------")
                break
            else:
                in_tile = True   
                print("------------inside tile------------")
                break
    print("++++++++++++++++++++++++++++++++++++++++")
    if w==2: w_2 =True
    elif stripe_x == 1 and (pos1[0]==w-1 or pos2[0]==w-1):
        stripe_tile_x = True
        print("------------between stripe and tile------------")
    elif stripe_x == 2 and ((pos1[0]==w-2 and pos2[0]==w-3) or (pos1[0]==w-3 and pos2[0]==w-2)):
        stripe_tile_x = True
        print("------------between stripe and tile------------")
    elif stripe_x ==2 and (pos1[0]==w-1 or pos1[0]==w-2) and (pos2[0]==w-1 or pos2[0]==w-2):
        in_stripe_x = True
        print("------------inside stripe x------------")
    else:
        for i in range(tiles_x):
            if (pos1[0]==3*(i+1)-1 and pos2[0]==pos1[0]+1) or (pos2[0]==3*(i+1)-1 and pos1[0]==pos2[0]+1):
                bet_tiles_x = True
                print("------------between tiles x------------")
                break
            else:
                in_tile = True   
                print("------------inside tile------------")
                break

    #chose the correct strategy according to the attacked edge
    dir_e = (pos2[0]-pos1[0], pos2[1]-pos1[1])
    strat = []
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

#-------------------------------------------------------------------------------------------
    #move each guard according to the correct strategy
    for x,y in G_guards.nodes():
        print("-----------------------------")
        print(pos[(x,y)])
        if h_2:
            print(tile_12)
            print(strat)
            for i in range(len(strat)):
                if (pos[(x,y)][0]%6, pos[(x,y)][1]) == tile_12[i]:
                    pos[(x,y)] = (pos[(x,y)][0]+strat[i][0], pos[(x,y)][1]+strat[i][1])
                    break

        elif w_2:
            print(tile_12)
            for i in range(len(strat)):
                    if (pos[(x,y)][0], -pos[(x,y)][1]-stripe_y%6) == tile_12[i]:
                        if strat[i]!=(None,None):
                            pos[(x,y)] = (pos[(x,y)][0]+strat[i][0], pos[(x,y)][1]+strat[i][1])
                            break

        elif easy_case:
            if pos[(x,y)]==pos1: pos[(x,y)]=pos2
            elif pos[(x,y)]==pos2: pos[(x,y)]=pos1

        elif in_stripe_y:
            if (pos[(x,y)][1]==0 or pos[(x,y)][1]==-1) and pos[(x,y)][0]<w-stripe_x:
                print("0 o -1")
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
                print("else")
                x0 = pos[(x,y)][0]//3*3
                y0 = -((-pos[(x,y)][1]-stripe_y)//3*3)-stripe_y
                tile = [(x0, y0), (x0+1,y0), (x0+2,y0), (x0, y0-1), (x0+1,y0-1), (x0+2,y0-1), (x0, y0-2), (x0+1,y0-2), (x0+2,y0-2)]
                if s1: l_strat2= intile_s1[1]
                else: l_strat2 = intile_s2[1]
                for i in range(len(l_strat2)):
                    if pos[(x,y)] == tile[i] and l_strat2[i]!=(None,None):
                        pos[(x,y)] = (pos[(x,y)][0]+l_strat2[i][0], pos[(x,y)][1]+l_strat2[i][1])
                        break
        
        elif in_stripe_x:
            print(pos[(x,y)])
            if (pos[(x,y)][1]==0 or pos[(x,y)][1]==-1) and pos[(x,y)][0]<w-stripe_x:
                print("1")
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
                print("2")
                print(strat)
                for i in range(len(strat)):
                    if (pos[(x,y)][0], -pos[(x,y)][1]-stripe_y%6) == tile_12[i]:
                        if strat[i]!=(None,None):
                            pos[(x,y)] = (pos[(x,y)][0]+strat[i][0], pos[(x,y)][1]+strat[i][1])
                            break
            else:
                print("3")
                x0 = pos[(x,y)][0]//3*3
                y0 = -((-pos[(x,y)][1]-stripe_y)//3*3)-stripe_y
                tile = [(x0, y0), (x0+1,y0), (x0+2,y0), (x0, y0-1), (x0+1,y0-1), (x0+2,y0-1), (x0, y0-2), (x0+1,y0-2), (x0+2,y0-2)]
                if s1: l_strat2= intile_s1[1]
                else: l_strat2 = intile_s2[1]
                for i in range(len(l_strat)):
                    if pos[(x,y)] == tile[i] and l_strat2[i]!=(None,None):
                        pos[(x,y)] = (pos[(x,y)][0]+l_strat2[i][0], pos[(x,y)][1]+l_strat2[i][1])
                        break

        elif stripe_tile_x or stripe_tile_y:  
            if pos[(x,y)] in tile_12:
                print(tile_12)
                if stripe_tile_y or stripe_tile_x:
                    print("1")
                    for i in range(len(strat)):
                        if pos[(x,y)] == tile_12[i] and strat[i]!=(None,None):
                            pos[(x,y)] = (pos[(x,y)][0]+strat[i][0], pos[(x,y)][1]+strat[i][1])
                            break
            elif pos[(x,y)][1]>=-(stripe_y-1) and pos[(x,y)][0]<w-stripe_x:
                print("2")
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
                print("3")
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
                print("4")
                x0 = pos[(x,y)][0]//3*3
                y0 = -((-pos[(x,y)][1]-stripe_y)//3*3)-stripe_y
                tile = [(x0, y0), (x0+1,y0), (x0+2,y0), (x0, y0-1), (x0+1,y0-1), (x0+2,y0-1), (x0, y0-2), (x0+1,y0-2), (x0+2,y0-2)]
                if s1: l_strat3= intile_s1[1]
                else: l_strat3 = intile_s2[1]
                for i in range(len(l_strat3)):
                    if pos[(x,y)] == tile[i] and l_strat3[i]!=(None,None):
                        pos[(x,y)] = (pos[(x,y)][0]+l_strat3[i][0], pos[(x,y)][1]+l_strat3[i][1])
                        break

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

        elif in_tile:
            if pos[(x,y)][1]>=-(stripe_y-1):
                if stripe_y==1: continue
                print("c1")
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
                print("c2")
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
                print("c3")
                x0 = pos[(x,y)][0]//3*3
                y0 = -((-pos[(x,y)][1]-stripe_y)//3*3)-stripe_y
                tile = [(x0, y0), (x0+1,y0), (x0+2,y0), (x0, y0-1), (x0+1,y0-1), (x0+2,y0-1), (x0, y0-2), (x0+1,y0-2), (x0+2,y0-2)]
                for i in range(len(strat)):
                    if pos[(x,y)] == tile[i] and strat[i]!=(None,None):
                        pos[(x,y)] = (pos[(x,y)][0]+strat[i][0], pos[(x,y)][1]+strat[i][1])
                        break

    if not easy_case: s1 = not s1
    return G_guards, G_edges, pos, True
                                   

def move_guards_o (G, G_guards,  G_edges, pos, edge, h, w):
    G_edges.add_edge(edge[0], edge[1])
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
   
    casea = ((pos2[0],0) in list(pos.values()))
    caseb = ((pos2[0],-1) in list(pos.values()))
    
    for x,y in G_guards.nodes():
        dir_x = pos2[0]-pos1[0]
        if easy_case:
            if pos[(x,y)]==pos1: pos[(x,y)]=pos2
            elif pos[(x,y)]==pos2: pos[(x,y)]=pos1

        elif case1:
            if caseb:
                if pos[(x,y)] == pos1:
                    pos[(x,y)] = pos2
                elif pos[(x,y)][0]==pos1[0] and pos[(x,y)][1]<pos1[1]:
                    pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                elif pos[(x,y)][0]==pos1[0] and pos[(x,y)][1]>pos1[1]:
                    continue
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]<pos2[1]:
                    if pos[(x,y)][1]==-h+1: pos[(x,y)] = (pos[(x,y)][0]-dir_x, pos[(x,y)][1])
                    else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]>pos2[1]:
                    pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
            elif casea:
                if pos[(x,y)] == pos1:
                    print("guard")
                    pos[(x,y)] = pos2
                elif pos[(x,y)][0]==pos1[0] and pos[(x,y)][1]<pos1[1]:
                    print("SA")
                elif pos[(x,y)][0]==pos1[0] and pos[(x,y)][1]>pos1[1]:
                    print("SB")
                    pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]<pos2[1]:
                    print("SC")
                    pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]>pos2[1]:
                    print("SD")
                    if pos[x,y][1]==0: pos[(x,y)] = (pos[(x,y)][0]-dir_x, pos[(x,y)][1])
                    else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                    print("SD")
                else:
                    print("else")
        elif case2:
            print("case2")
            if caseb:
                if pos[(x,y)] == pos1: pos[(x,y)] = pos2
                elif pos[(x,y)][0]==pos1[0] and pos[(x,y)][1]<pos1[1]:
                    pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                    print("SA")
                elif pos[(x,y)][0]==pos1[0] and pos[(x,y)][1]>pos1[1]:
                    print("SB")
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]<pos2[1]:
                    if pos[(x,y)][1]==-h+1:
                        pos[(x,y)] = (pos[(x,y)][0]-dir_x, pos[(x,y)][1])
                    else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                    print("SC")
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]>pos2[1]:
                    pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                    print("SD")
                else:
                    print("else")
            elif casea:
                if pos[(x,y)] == pos1: pos[(x,y)] = pos2
                elif pos[(x,y)][0]==pos1[0] and pos[(x,y)][1]<pos1[1]:
                    print("SA")
                elif pos[(x,y)][0]==pos1[0] and pos[(x,y)][1]>pos1[1]:
                    pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                    print("SB")
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]<pos2[1]:
                    pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                    print("SC")
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]>pos2[1]:
                    if pos[(x,y)][1]==0:
                        pos[(x,y)] = (pos[(x,y)][0]-dir_x, pos[(x,y)][1])
                    else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                    print("SD")
                else:
                    print("else")
        
        elif case3:
            print("case3")
            if caseb:
                #guard
                if pos[(x,y)] == pos1: pos[(x,y)] = pos2
                #SA
                elif pos[(x,y)][0]==pos1[0]-1 and pos[(x,y)][1]<pos1[1]:
                    print("SA")
                    if pos1[1]-pos2[1]==-1:
                        if pos[(x,y)][1]==pos1[1]-1:
                            pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1])
                        else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                    else:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)

                #SB
                elif pos[(x,y)][0]==pos1[0]-1 and pos[(x,y)][1]>=pos1[1]:
                    if pos1[1]-pos2[1]==1:
                        if pos[(x,y)][1]==0:
                            pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1])
                        else:
                            pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                    
                    print("SB")
                #SC
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]<pos2[1]:
                    if pos[(x,y)][1]==-h+1:
                        pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1])
                    else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                    print("SC")
                #SD
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]>pos2[1]:
                    if pos1[1]-pos2[1]==-1:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                    else:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                    print("SD")

            elif casea:
                if pos[(x,y)] == pos1: pos[(x,y)] = pos2
                elif pos[(x,y)][0]==pos1[0]-1 and pos[(x,y)][1]<=pos1[1]:
                    print("SA")
                    if pos1[1]-pos2[1]==-1:
                        if pos[(x,y)][1]==-h+1:
                            pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1])
                        else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                elif pos[(x,y)][0]==pos1[0]-1 and pos[(x,y)][1]>pos1[1]:
                    print("SB")
                    if pos1[1]-pos2[1]==1:
                        if pos[(x,y)][1]==pos1[1]+1:
                            pos[(x,y)] = (pos[(x,y)][0]+1, pos[(x,y)][1])
                        else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                    else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)

                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]<pos2[1]:
                    if pos1[1]-pos2[1]==1:
                        pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]-1)
                    else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)
                    print("SC")
                elif pos[(x,y)][0]==pos2[0] and pos[(x,y)][1]>pos2[1]:
                    
                    if pos[(x,y)][1]==0:
                        pos[(x,y)] = (pos[(x,y)][0]-1, pos[(x,y)][1])
                    else: pos[(x,y)] = (pos[(x,y)][0], pos[(x,y)][1]+1)

                    print("SD")
                else:
                    print("else")
        

    
    return G_guards, G_edges, pos, True

def move_guards_s (G, G_guards, G_edges, pos, edge, h, w):
    G_edges.add_edge(edge[0], edge[1])
    pos_nodes = get_pos(G)
    if pos_nodes[edge[0]] in list(pos.values()):
        pos1 = pos_nodes[(edge[0][0],edge[0][1])]
        pos2 = pos_nodes[(edge[1][0],edge[1][1])]
    else:
        pos1 = pos_nodes[(edge[1][0],edge[1][1])]
        pos2 = pos_nodes[(edge[0][0],edge[0][1])]
    #if egde is vertical rotate the graph
    if pos1[1]!=pos2[1]:
        G1 = nx.grid_2d_graph(w, h, periodic=False)
        edge1=((edge[0][1], w-edge[0][0]-1), (edge[1][1], w-edge[1][0]-1))
        cycle1 = hamilton(G1, edge1)
        cycle=[]
        for (x,y) in cycle1:
            cycle.append((w-1-y, x))
    else:
        cycle = hamilton(G, edge)
    pos_cycle = []
    for node in cycle:
        pos_cycle.append(pos_nodes[node])
   
    i1 = pos_cycle.index(pos1)
    i2 = pos_cycle.index(pos2)
    dir = i2-i1
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
    return G_guards, G_edges, pos, True


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