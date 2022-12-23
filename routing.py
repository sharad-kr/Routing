def dik(l): # l is list of 3-sized tuples 
    x=dict()
    for i in range(len(l)):
        if not ((min(l[i][0],l[i][1]),max(l[i][0],l[i][1])) in x) :
            x[(min(l[i][0],l[i][1]),max(l[i][0],l[i][1]))] = l[i][2]
        else: 
            if l[i][2]>x[(min(l[i][0],l[i][1]),max(l[i][0],l[i][1]))]:
                x[(min(l[i][0],l[i][1]),max(l[i][0],l[i][1]))] = l[i][2]
    return x


class node:
    def __init__(self,index,cap,route_parent,heap_index,visited):
        self.index=index
        self.cap=cap
        self.route_parent=route_parent
        self.heap_index=heap_index
        self.visited=visited

def findMaxCapacity(n,links,s,t):
    cap_dik=dik(links)
    node_list=[]
    adj_list=[]
    for a in range(n):
        node_list.append((node(a,0,None,None,False)))
        adj_list.append([])

    for b in cap_dik:
        adj_list[b[0]].append(b[1])
        adj_list[b[1]].append(b[0])

    def heapdown(i,h):
        g = node_list[i].heap_index
        if (2*g+2)<len(h):
            if node_list[h[g]].cap < max(node_list[h[2*g+1]].cap,node_list[h[2*g+2]].cap):
                if node_list[h[2*g+1]].cap <= node_list[h[2*g+2]].cap:
                    node_list[h[g]].heap_index , node_list[h[2*g+2]].heap_index = node_list[h[2*g+2]].heap_index ,node_list[h[g]].heap_index 
                    h[g],h[2*g+2] = h[2*g+2],h[g]
                    heapdown(i,h)
                elif node_list[h[2*g+1]].cap > node_list[h[2*g+2]].cap:
                    node_list[h[g]].heap_index , node_list[h[2*g+1]].heap_index = node_list[h[2*g+1]].heap_index ,node_list[h[g]].heap_index 
                    h[g],h[2*g+1] = h[2*g+1],h[g]
                    heapdown(i,h)
        elif 2*g+2 == len(h):
            if node_list[h[g]].cap < node_list[h[2*g+1]].cap:
                node_list[h[g]].heap_index , node_list[h[2*g+1]].heap_index = node_list[h[2*g+1]].heap_index ,node_list[h[g]].heap_index 
                h[g],h[2*g+1] = h[2*g+1],h[g]
                
    def heapup(i,h):
        g = node_list[i].heap_index
        if (((g-1)//2) >= 0):
            if node_list[h[g]].cap > node_list[h[((g-1)//2)]].cap:
                node_list[h[g]].heap_index,node_list[h[((g-1)//2)]].heap_index = node_list[h[((g-1)//2)]].heap_index ,node_list[h[g]].heap_index
                h[g],h[((g-1)//2)] = h[((g-1)//2)] ,h[g]
                heapup(i,h)

    def insert(i,h):
        h.append(i)
        node_list[i].heap_index = len(h)-1
        heapup(i,h)
    
    def extract_max(h):
        if len(h) > 1 :
            x=h[0]
            h[0],h[-1]=h[-1],h[0]
            node_list[h[0]].heap_index = 0
            node_list[h[-1]].heap_index = None
            h.pop()
            heapdown(h[0],h)
        elif len(h) == 1:
            x=h[0]
            node_list[h[0]].heap_index = None
            h.pop()
        return x

    heap = [s]
    node_list[s].heap_index = 0
    node_list[s].visited = True
    node_list[s].cap = float('inf')

    while (node_list[t].visited == False) :
        q = extract_max(heap)
        nbr = adj_list[q]
        for p in range(len(nbr)):
            if node_list[nbr[p]].visited == False :
                if node_list[nbr[p]].cap < min(node_list[q].cap,cap_dik[(min(q,nbr[p]),max(q,nbr[p]))]):
                    node_list[nbr[p]].cap = min(node_list[q].cap,cap_dik[(min(q,nbr[p]),max(q,nbr[p]))])
                    node_list[nbr[p]].route_parent = node_list[q]
                    if node_list[nbr[p]].heap_index == None:
                        insert(nbr[p],heap)
                    else:
                        heapup(nbr[p],heap)
        node_list[q].visited = True

    v = node_list[t]
    path=[]
    while v.route_parent != None :
        path.append((v.index))
        v=v.route_parent
    path.append(v.index)
    ans = []
    while len(path)!=0:
        ans.append(path[-1])
        path.pop()

    return (node_list[t].cap,ans)




