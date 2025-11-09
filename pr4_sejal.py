# Program: Implement Link State Routing (Dijkstra's Algorithm)
# Author: (Your Name)
# Subject: Computer Networks Laboratory

# Step 1: Create a simple network as an adjacency matrix
# Each value represents the cost (distance) between routers
# 0 means no direct connection

graph = {
    'A': {'A': 0, 'B': 2, 'C': 5, 'D': 0, 'E': 0},
    'B': {'A': 2, 'B': 0, 'C': 3, 'D': 4, 'E': 0},
    'C': {'A': 5, 'B': 3, 'C': 0, 'D': 2, 'E': 3},
    'D': {'A': 0, 'B': 4, 'C': 2, 'D': 0, 'E': 1},
    'E': {'A': 0, 'B': 0, 'C': 3, 'D': 1, 'E': 0}
}

# Step 2: Take the source router as input
source = input("Enter the source router (A-E): ").upper()

# Step 3: Initialize distances and visited sets
unvisited = list(graph.keys())
distances = {node: float('inf') for node in graph}
distances[source] = 0
previous = {node: None for node in graph}

# Step 4: Dijkstra’s algorithm
while unvisited:
    # Pick the unvisited node with smallest distance
    current = min(unvisited, key=lambda node: distances[node])
    unvisited.remove(current)

    for neighbor, cost in graph[current].items():
        if cost > 0:  # If there is a link
            new_distance = distances[current] + cost
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current

# Step 5: Display shortest paths
print("\n--- Shortest Paths from Router", source, "---")
for node in graph:
    if node == source:
        continue
    path = []
    current = node
    while current is not None:
        path.insert(0, current)
        current = previous[current]
    print(f"{source} → {node}: {' -> '.join(path)} (Cost = {distances[node]})")
