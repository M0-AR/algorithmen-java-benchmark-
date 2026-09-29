"""Lang Ch.5: Floyd-Warshall, Prim O(n^2), Dijkstra."""
from __future__ import annotations
import heapq

INF = float("inf")


def floyd(n, w):
    d = [row[:] for row in w]
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik == INF:
                continue
            di = d[i]
            for j in range(n):
                nd = dik + dk[j]
                if nd < di[j]:
                    di[j] = nd
    return d


def dijkstra(n, adj, s):
    dist = [INF] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        du, u = heapq.heappop(pq)
        if du != dist[u]:
            continue
        for v, wgt in adj[u]:
            nd = du + wgt
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


def prim_mst(n, w):
    in_t = [False] * n
    d = [INF] * n
    parent = [-1] * n
    d[0] = 0
    total = 0.0
    for _ in range(n):
        u = -1
        best = INF
        for v in range(n):
            if not in_t[v] and d[v] < best:
                best = d[v]
                u = v
        if u == -1:
            break
        in_t[u] = True
        total += best
        for v in range(n):
            if not in_t[v] and w[u][v] < d[v]:
                d[v] = w[u][v]
                parent[v] = u
    return total, parent
