## Find the K-Cores clusters
import networkx as nx
import matplotlib.pyplot as plt 

## Read .graphml file into a NetworkX Graph object
def initializeG():
    G = nx.read_graphml('bfmaier_post_FA.graphml', node_type=int)
    ## nx.draw(G)
    return G

## =========================================================================================
## Community Detection Algorithm: Louvain
## =========================================================================================

##
## IMPORTANT NOTE!!
##      These next two functions were acquired from Professor Tsung Heng Wu's 
## .../src/05_community.html example file with minor alterations.  Our team
## claims no credit for the development of these functions.
##
def draw_communities(G, communities):
    cmap = ['grey' for n in range(0,lengthG)]
    cmap[0:6] = ['red', 'blue', 'green', 'orange', 'cyan', 'pink', 'black']
    colors = ['red' for n in G.nodes]
    for j, n in enumerate(G.nodes):
        for i, c in enumerate(communities):
            if n in c:
                colors[j] = cmap[i]
                break
        
    nx.draw(G, with_labels=False, node_color=colors)
    return colors

##
## A Quick Sort implementation to sort the set of communities from largest to smallest.
##
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        left = [x for x in arr[1:] if len(x) >= len(pivot)]
        right = [x for x in arr[1:] if len(x) < len(pivot)]
        return quicksort(left) + [pivot] + quicksort(right)


## Find and display the communities within the graph using Louvain's algorithm
def findCommunities(G, draw=True):
    community = nx.community.louvain_communities(G, seed=1)
    community = quicksort(community)

    nx.community.modularity(G, communities=community)
    if draw == True:
        colors = draw_communities(G, community)
        return colors

## =========================================================================================
## Community Search Algorithm: K-Cores
## =========================================================================================

## Get a set of maximal K values for each node of the graph
## Pre-computing Core Numbers reduces load on process when finding Optimal K considerably
def getCores(G):
    cores = nx.core_number(G)
    return cores

## Get the highest valid K value out of all the nodes in the graph
def getMaxDegree(cores):
    return max(cores.values())

## Iterate through all possible values for K, from K=0 to K=MaxDegree
def findOptimalK(G, cores):
    Gs = {}
    retK = 0
    maxK = getMaxDegree(cores)

    print("To Find the \"Most Optimal\" K value for our purposes, check each of the\n\
K-values in sequence until you encounter a K value that produces an inferior\n\
graph to the one that came before it.")
    for k in range(0, maxK):
        Gs[k] = nx.k_core(G, k, cores)
        findCommunities(Gs[k], draw=True)
        print(str(k) + '-Core Communities')
        plt.show()
        breakout = False
        while(breakout != True):
            print('Is this K-Core worse than the last one? (y/n)')
            userinput = input()
            if userinput == 'y':
                return retK
            elif userinput == 'n':
                retK = k
                breakout = True

## Run the finalized K-Core analysis on the graph using the Optimal K
def analyzeKCore(G, K, cores):
    G = nx.k_core(G, K, cores)
    print("This is the user-defined \"Most Optimal\" K-Core that attempts to preserve the\n\
    4 primary communities of our graph, the ",K,"-Core.")
    findCommunities(G, draw=True)
    plt.show()








if __name__ == "__main__":
    ## First, load in the graph
    G = initializeG()
    lengthG = len(G)
    ##nx.draw(G)

    ## Then, identify communities
    colors = findCommunities(G)
    plt.show()

    ## Now, confirm community presence
    cores = getCores(G)
    K = findOptimalK(G, cores)
    #K=10
    print(K)
    analyzeKCore(G, K, cores)