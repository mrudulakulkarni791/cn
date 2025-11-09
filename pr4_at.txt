# Enter the number of routers (nodes): 4
# Enter the number of edges (connections between routers): 5
# Enter the edges in the format 'u v weight' (e.g., 0 1 2):
# 0 1 1
# 0 2 4
# 1 2 2
# 1 3 6
# 2 3 3

class DistanceVectorRouting:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.graph = [[float('inf')] * num_nodes for _ in range(num_nodes)]
        self.distances = [[float('inf')] * num_nodes for _ in range(num_nodes)]
        self.next_hop = [[-1] * num_nodes for _ in range(num_nodes)]
        
    def add_edge(self, u, v, weight):
        self.graph[u][v] = weight
        self.graph[v][u] = weight

    def initialize_routing_table(self):
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if i == j:
                    self.distances[i][j] = 0
                elif self.graph[i][j] != float('inf'):
                    self.distances[i][j] = self.graph[i][j]
                    self.next_hop[i][j] = j

    def bellman_ford(self):
        for k in range(self.num_nodes):
            for i in range(self.num_nodes):
                for j in range(self.num_nodes):
                    if self.distances[i][k] + self.distances[k][j] < self.distances[i][j]:
                        self.distances[i][j] = self.distances[i][k] + self.distances[k][j]
                        self.next_hop[i][j] = self.next_hop[i][k]

    def print_routing_table(self):
        print("\nRouting Table (Distance Vector):")
        for i in range(self.num_nodes):
            print(f"Router {i}:")
            for j in range(self.num_nodes):
                if self.distances[i][j] == float('inf'):
                    print(f"  To {j}: No Path")
                else:
                    print(f"  To {j}: Distance = {self.distances[i][j]}, Next Hop = {self.next_hop[i][j]}")
            print()

def main():
    num_nodes = int(input("Enter the number of routers (nodes): "))
    dvr = DistanceVectorRouting(num_nodes)
    
    # Get edges between routers (u, v, cost)
    num_edges = int(input("Enter the number of edges (connections between routers): "))
    
    print("Enter the edges in the format 'u v weight' (e.g., 0 1 2):")
    for _ in range(num_edges):
        u, v, weight = map(int, input().split())
        dvr.add_edge(u, v, weight)

    # Initialize the routing table
    dvr.initialize_routing_table()

    # Perform Bellman-Ford algorithm to update routing tables
    dvr.bellman_ford()

    # Print the final routing table
    dvr.print_routing_table()

if __name__ == "__main__":
    main()
