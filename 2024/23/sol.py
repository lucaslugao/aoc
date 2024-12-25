import sys
import networkx as nx


def find_connected_triplets_starting_with(G, letter="t"):
    triplets = set()
    for nodeA in G.nodes():
        if nodeA.startswith(letter):
            neighborsA = set(G[nodeA])
            for nodeB in neighborsA:
                common_neighbors = neighborsA.intersection(G[nodeB])
                for nodeC in common_neighbors:
                    triplet = tuple(sorted([nodeA, nodeB, nodeC]))
                    triplets.add(triplet)
    return triplets


def find_largest_connected_subset(G):
    largest_clique = max(nx.find_cliques(G), key=len)
    return largest_clique


if __name__ == "__main__":
    lines = [line.strip() for line in sys.stdin]

    G = nx.Graph()
    for line in lines:
        nodeA, nodeB = line.split("-")
        G.add_edge(nodeA, nodeB)

    triplets = find_connected_triplets_starting_with(G, "t")
    print(len(triplets))

    largest_clique = find_largest_connected_subset(G)
    print(",".join(sorted(largest_clique)))
