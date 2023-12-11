## Find the K-Cores clusters
## decided to not use this code
import networkx as nx
import matplotlib.pyplot as plt 
G = nx.read_graphml('bfmaier_anonymized_fb_network.graphml')
nx.draw(G)

cores = nx.core_number(G)

#print(cores)

Gs = {}

for i in 0:10
    Gs[i] = nx.k_core(G, i, cores)
    nx.draw(Gs[i])
