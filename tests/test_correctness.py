import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from benchmarks.sorting.sorting import insertion_sort_counted, quicksort, heapsort, mergesort_b, shellsort, inversion_sequence
from benchmarks.textsearch.textsearch import naive_search, kmp_search, horspool_search, sunday_search
from benchmarks.graph.graph import floyd, dijkstra, prim_mst


def test_h1_inversion_theorem():
    for a in [[5, 7, 0, 3, 4, 2, 6, 1], [3, 2, 1], [1, 2, 3], [2, 2, 1]]:
        s, cmp, inv = insertion_sort_counted(a)
        assert s == sorted(a)
        # Lang Thm 2.1: insertion comparisons == sum(v) + (n-1 - trailing?) bound: cmp >= inv
        assert cmp >= inv
        assert sum(inversion_sequence(a)) == inv


def test_sorts_correct():
    import random
    rnd = random.Random(0)
    for _ in range(20):
        a = [rnd.randint(0, 50) for _ in range(30)]
        for fn in [quicksort, heapsort, mergesort_b, shellsort]:
            s, _ = fn(a)
            assert s == sorted(a)


def test_textsearch_agree():
    t = "aaabaaabaacababa text algorithm sorting " * 20
    for p in ["aaba", "algorithm", "aaab", "text"]:
        o0, _ = naive_search(t, p)
        for fn in [kmp_search, horspool_search, sunday_search]:
            o, _ = fn(t, p)
            assert o == o0, (p, fn.__name__)


def test_floyd_eq_dijkstra():
    n = 6
    import random
    rnd = random.Random(1)
    w = [[0 if i == j else rnd.randint(1, 9) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            w[i][j] = w[j][i] = min(w[i][j], w[j][i])
    d = floyd(n, w)
    adj = [[(j, w[i][j]) for j in range(n) if j != i] for i in range(n)]
    for s in range(n):
        assert dijkstra(n, adj, s) == d[s]
    tot, _ = prim_mst(n, w)
    assert tot > 0
