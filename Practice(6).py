import re
file = open('D:/Network/Network 3_new.txt', 'r')
net3 = file.read()


## 6-1
# Do condensation for the digraph network 3
split = re.split('\n', net3)
split.remove('')
edges = []
for i in range(0,len(split)):
    num = re.sub('\t','',split[i])
    edges.append(num)
    
nodes = []
for k in edges:
    if k[0] not in nodes:
        nodes.append(k[0])
    if k[1] not in nodes:
        nodes.append(k[1])

# Use Tarjan's algorithm to find strongly connected components 
# Reference: https://iq.opengenus.org/tarjans-algorithm/
from collections import defaultdict

class Condense:
    def __init__(self, nodes, edges):
        self.graph = defaultdict(list)
        self.nodes = nodes
        
    def DFS(self, node, index, low, dfs_num, stack, on_stack):
        index += 1
        low[node] = index
        dfs_num[node] = index
        stack.append(node)
        on_stack[node] = True
    
        for neighbor in self.graph.get(node, []):
            if not dfs_num.get(neighbor):
                self.DFS(neighbor, index, low, dfs_num, stack, on_stack)
                low[node] = min(low[node], low[neighbor])
            elif on_stack[neighbor]:
                # Update the lower index for the current node based on the neighbor
                low[node] = min(low[node], dfs_num[neighbor])
    
        # Is a strongly connected loop
        if low[node] == dfs_num[node]:
            scc = []
            while True:
                current = stack.pop()
                on_stack[current] = False
                scc.append(current)
                if current == node:
                    break
            strongly_connected_components.append(scc)
            
    def find_SCC(self):
        for node in self.graph:
            if not dfs_num.get(node):
                # Call DFS on unvisited nodes to find strongly connected components
                self.DFS(node, index, low, dfs_num, stack, on_stack)
    
        return strongly_connected_components

# Initialize
index = 0
low = {}
dfs_num = {}
stack = []
on_stack = {}
strongly_connected_components = []

strong = Condense(nodes, edges) 
for k in range(0,len(edges)):
    strong.graph[edges[k][0]].append(edges[k][1])
strongly_connected_components = strong.find_SCC()

# Strongly Connected Components of the graph
for component in strongly_connected_components:
    if len(component) > 1:
        SCC = component
#print(SCC)

# Condensation
condense_label = {}
for x in nodes:
    if x in SCC:
        condense_label[x] = "s"
    else:
        condense_label[x] = x
#print(condense_label)

# Change edges and nodes
condense_edges = []
for string in edges:
    name = condense_label.get(string[0]),condense_label.get(string[1])
    changed = "".join(name)
    # Remove the replicated edges and nodes   
    if changed not in condense_edges:
        condense_edges.append(changed)
condense_edges.remove("ss")
print("Edge list after condensation:",condense_edges)

condense_nodes = []
for node in nodes:
    name = condense_label.get(node[0])
    changed = "".join(name)
    if changed not in condense_nodes:
        condense_nodes.append(changed)
print("Node list after condensation:", condense_nodes)


## 6-2
# Treat networks 3 as a undirected graph
import itertools

undict_list = []
for edge in edges:
    alldict = [edge, edge[1]+edge[0]]
    undict_list.append(alldict)
#print(undict_list)

possibles = list(itertools.product(undict_list[0],undict_list[1],undict_list[2],undict_list[3],undict_list[4],undict_list[5],undict_list[6],undict_list[7],undict_list[8],undict_list[9],undict_list[10],undict_list[11],undict_list[12],undict_list[13],undict_list[14]))
#print(possibles)  # 2^15 = 32768 possibilities        

# Is it strongly orientable?
# If yes, find the strongly oriented graph
is_SCC = False
for poss in possibles:
    # Initialize
    undigraph = Condense(condense_nodes, condense_edges)
    index = 0
    low = {}
    dfs_num = {}
    stack = []
    on_stack = {}
    strongly_connected_components = []
    
    # Import different direct edges 
    for k in range(0,len(poss)):
        undigraph.graph[poss[k][0]].append(poss[k][1])    
    #print(poss)
    
    # Find SCC
    strongly_connected_components = undigraph.find_SCC()
    if len(strongly_connected_components) == 1:
        strong_ori_graph = undigraph.graph
        #print(strong_ori_graph)
        is_SCC = True
        break
        
if is_SCC == False:
    print("No, it is not strongly orientable.")
else:
    print("Yes, it is strongly orientable. The example is listed below:")
    strong_ori_edges = []
    for key in strong_ori_graph:
        for value in strong_ori_graph[key]:
            dict_name = key+value
            strong_ori_edges.append(dict_name)
    print("Strongly oriented edge list:", strong_ori_edges)

    strong_ori_nodes = []
    for k in strong_ori_edges:
        if k[0] not in strong_ori_nodes:
            strong_ori_nodes.append(k[0])
        if k[1] not in strong_ori_nodes:
            strong_ori_nodes.append(k[1])
    print("Strongly oriented node list:", strong_ori_nodes)           

# Find the vertex-cut and its vertex-connectivity
# Vertex-cut subset
pick_list = []
for node in strong_ori_nodes:
    pick_node = [node, ""]
    pick_list.append(pick_node)
#print(pick_list)

remove_possibles = list(itertools.product(pick_list[0],pick_list[1],pick_list[2],pick_list[3],pick_list[4],pick_list[5],pick_list[6],pick_list[7]))
remove_possible_list = [[item for item in element if item != ''] for element in remove_possibles]
#print(remove_possible_list)  # 2^8 = 256 possibilities

vcut_SCC_list = []
vertex_cut = []
for remove_element in remove_possible_list:
    # Remove edge
    vcut_edges = []
    for edge in strong_ori_edges:
        if not any(item in edge for item in remove_element):
            vcut_edges.append(edge)
    #print(remove_element, vcut_edges)    

    # Remove vertex
    vcut_nodes = []
    for node in strong_ori_nodes:
        if not any(item in node for item in remove_element):
            vcut_nodes.append(node)
    #print(remove_element, vcut_nodes)
    
    # Initialize
    vcut = Condense(vcut_nodes, vcut_edges) 
    index = 0
    low = {}
    dfs_num = {}
    stack = []
    on_stack = {}
    strongly_connected_components = []

    for k in range(0,len(vcut_edges)):
        vcut.graph[vcut_edges[k][0]].append(vcut_edges[k][1])
    # Append isolated nodes (No edges)
    if len(vcut_edges) == 0:
        for k in range(0,len(vcut_nodes)):
            vcut.graph[vcut_nodes[k]].append("")
    #print(vcut.graph)
    
    # Find strongly connected component
    new_vcut_SCC = []
    vcut_SCC = vcut.find_SCC()
    for sublist in vcut_SCC:
        if sublist != ['']:
            new_vcut_SCC.append(sublist)
    #print(remove_element, new_vcut_SCC)
    
    # If not strongly connected (SCC_num > 1), then it is in vertex-cut subset
    if len(new_vcut_SCC) > 1:
        vcut_SCC_list.append(new_vcut_SCC)
        vertex_cut.append(remove_element)
        #print(vertex_cut)
        #print(vcut_SCC_list)

print("Vertex-cut subset:", vertex_cut)
#print(vcut_SCC_list)

# Vertex-connectivity
min_size = len(vertex_cut[0])
for j in range(1,len(vertex_cut)):
    if len(vertex_cut[j]) < min_size: 
        min_size = len(vertex_cut[j])
print("Vertex-connectivity =", min_size)
