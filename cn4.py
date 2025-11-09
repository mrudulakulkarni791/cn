# distance_vector.py
# Distance Vector routing simulator (per-router Bellman-Ford style)
INF = 10**9

def read_int(prompt=""):
    return int(input(prompt).strip())

def read_cost_matrix(n):
    print(f"Enter the cost matrix ({n} x {n}).")
    print("Use a large number (e.g. 999) or 0 for no direct link except diagonal (self=0).")
    mat = []
    for i in range(n):
        row = list(map(int, input().strip().split()))
        if len(row) != n:
            raise ValueError(f"Expected {n} values on row {i+1}")
        # convert sentinel (like 999) to INF internally (except diagonal stays 0)
        for j in range(n):
            if i != j and row[j] >= 999:
                row[j] = INF
        mat.append(row)
    return mat

def compute_routing_table_for_source(src, cost):
    """
    Run Bellman-Ford style relaxation from source `src` using adjacency cost matrix.
    Return (dist[], pred[]) where pred[v] stores the predecessor of v on the shortest path from src.
    """
    n = len(cost)
    # initialize
    dist = [INF] * n
    pred = [-1] * n

    dist[src] = 0
    pred[src] = -1

    # direct neighbors initialization
    for v in range(n):
        if v != src and cost[src][v] < INF:
            dist[v] = cost[src][v]
            pred[v] = src

    # relax up to (n-1) times (Bellman-Ford)
    for _ in range(n-1):
        updated = False
        for u in range(n):
            if dist[u] == INF:
                continue
            for v in range(n):
                if cost[u][v] == INF or u == v:
                    continue
                if dist[v] > dist[u] + cost[u][v]:
                    dist[v] = dist[u] + cost[u][v]
                    pred[v] = u
                    updated = True
        if not updated:
            break

    return dist, pred

def first_hop_from_pred(src, dest, pred):
    """
    Given predecessor array `pred` for paths from src, find the first hop from src to dest.
    - If dest==src -> return src (or '-')
    - If pred[dest] == -1 and dest != src -> unreachable
    - Else walk backwards from dest using pred until predecessor is src: that node is next hop.
    """
    if dest == src:
        return src
    if pred[dest] == -1:
        return None  # unreachable
    cur = dest
    # follow predecessors until predecessor is src
    while pred[cur] != src:
        cur = pred[cur]
        # defensive check
        if cur == -1:
            return None
    return cur

def print_routing_tables(cost):
    n = len(cost)
    for src in range(n):
        dist, pred = compute_routing_table_for_source(src, cost)
        print(f"\nRouting table for router {src+1}:")
        print("{:>12} {:>12} {:>12}".format("Destination", "NextHop", "Distance"))
        for dest in range(n):
            if dist[dest] >= INF:
                dist_str = "INF"
                next_hop = None
            else:
                dist_str = str(dist[dest])
                next_hop = first_hop_from_pred(src, dest, pred)
            nh_str = "-" if next_hop is None else str(next_hop+1)  # +1 for human-friendly
            if dest == src:
                nh_str = "-"  # no next hop for itself
                dist_str = "0"
            print("{:>12} {:>12} {:>12}".format(dest+1, nh_str, dist_str))

def main():
    print("----- Distance Vector Routing Simulator (Python) -----")
    n = read_int("Enter number of nodes: ")
    cost = read_cost_matrix(n)
    print_routing_tables(cost)

if __name__ == "__main__":
    main()
