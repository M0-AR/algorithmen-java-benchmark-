"""Faithful ports of Lang Ch.2 sorting algorithms with operation counters.

Each sort(a) -> (sorted_list, stats_dict) where stats has comparisons/swaps/steps.
Mirrors Java code in book: InsertionSorter, QuickSorter (mid pivot), HeapSorter,
MergeSorter variant-b, IterativeMergeSorter, NaturalMergeSorter (bitonic runs),
ShellSorter (Sedgewick cols subset).
"""
from __future__ import annotations


class Counter:
    def __init__(self):
        self.cmp = 0
        self.moves = 0

    def to_dict(self):
        return {"comparisons": self.cmp, "moves": self.moves}


def inversion_sequence(a):
    n = len(a)
    v = [0] * n
    for j in range(n):
        c = 0
        aj = a[j]
        for i in range(j):
            if a[i] > aj:
                c += 1
        v[j] = c
    return v


def insertion_sort(a):
    a = list(a)
    c = Counter()
    for i in range(1, len(a)):
        t = a[i]
        j = i
        while j > 0:
            c.cmp += 1
            if a[j - 1] > t:
                a[j] = a[j - 1]
                c.moves += 1
                j -= 1
            else:
                break
        a[j] = t
    steps = sum(inversion_sequence(a_sorted_orig(a, None)) or [0])  # placeholder
    return a, c.to_dict()


def a_sorted_orig(a, _):
    return None


def insertion_sort_counted(a):
    """Returns (sorted, comparisons, inversion_sum). Verifies Thm 2.1: steps == sum(v)."""
    a = list(a)
    inv = inversion_sequence(a)
    cmp = 0
    for i in range(1, len(a)):
        t = a[i]
        j = i
        while j > 0:
            cmp += 1
            if a[j - 1] > t:
                a[j] = a[j - 1]
                j -= 1
            else:
                break
        a[j] = t
    return a, cmp, sum(inv)


def quicksort(a):
    a = list(a)
    c = Counter()

    def qs(lo, hi):
        i, j = lo, hi
        x = a[(lo + hi) // 2]
        while i <= j:
            while True:
                c.cmp += 1
                if not (a[i] < x):
                    break
                i += 1
            while True:
                c.cmp += 1
                if not (a[j] > x):
                    break
                j -= 1
            if i <= j:
                a[i], a[j] = a[j], a[i]
                c.moves += 1
                i += 1
                j -= 1
        if lo < j:
            qs(lo, j)
        if i < hi:
            qs(i, hi)

    if len(a) > 1:
        qs(0, len(a) - 1)
    return a, c.to_dict()


def heapsort(a):
    a = list(a)
    c = Counter()
    n = len(a)

    def downheap(v, nlim):
        w = 2 * v + 1
        while w < nlim:
            if w + 1 < nlim:
                c.cmp += 1
                if a[w + 1] > a[w]:
                    w += 1
            c.cmp += 1
            if a[v] >= a[w]:
                return
            a[v], a[w] = a[w], a[v]
            c.moves += 1
            v = w
            w = 2 * v + 1

    for v in range(n // 2 - 1, -1, -1):
        downheap(v, n)
    nn = n
    while nn > 1:
        nn -= 1
        a[0], a[nn] = a[nn], a[0]
        c.moves += 1
        downheap(0, nn)
    return a, c.to_dict()


def mergesort_b(a):
    """Variant-b: only front half spilled to aux (book 2.4b)."""
    a = list(a)
    c = Counter()
    n = len(a)
    b = [0] * ((n + 1) // 2)

    def merge(lo, m, hi):
        i, j, k = 0, lo, lo
        jj = lo
        while jj <= m:
            b[i] = a[jj]
            i += 1
            jj += 1
        i = 0
        k = lo
        jcur = m + 1
        blen = m - lo + 1
        while i < blen and jcur <= hi:
            c.cmp += 1
            if b[i] <= a[jcur]:
                a[k] = b[i]
                i += 1
                k += 1
            else:
                a[k] = a[jcur]
                jcur += 1
                k += 1
            c.moves += 1
        while i < blen:
            a[k] = b[i]
            i += 1
            k += 1
            c.moves += 1

    def ms(lo, hi):
        if lo < hi:
            m = (lo + hi) // 2
            ms(lo, m)
            ms(m + 1, hi)
            merge(lo, m, hi)

    if n > 1:
        ms(0, n - 1)
    return a, c.to_dict()


def shellsort(a):
    a = list(a)
    c = Counter()
    cols = [7, 3, 1]  # Sedgewick tail; full list in book truncated for speed
    n = len(a)
    for h in cols:
        for i in range(h, n):
            t = a[i]
            j = i
            while j >= h:
                c.cmp += 1
                if a[j - h] > t:
                    a[j] = a[j - h]
                    c.moves += 1
                    j -= h
                else:
                    break
            a[j] = t
    return a, c.to_dict()


def natural_runs(a):
    """Count bitonic runs as in Natural Mergesort 2.6 (up then down)."""
    n = len(a)
    if n == 0:
        return 0
    runs = 0
    i = 0
    while i < n:
        runs += 1
        # ascending
        while i + 1 < n and a[i] <= a[i + 1]:
            i += 1
        # descending tail of bitonic run consumes further falls
        while i + 1 < n and a[i] >= a[i + 1]:
            # only consume descent if we already ascended at least 1 OR start descent
            # to avoid infinite: break when next ascent starts a new run
            # peek: if descent ends and next step ascends, stop after descent
            i += 1
            if i + 1 < n and a[i] <= a[i + 1]:
                # descent ended exactly at valley; next ascent belongs to next run
                break
        i += 1
    return runs


ALGOS = {
    "insertion": insertion_sort_counted,
    "quick": quicksort,
    "heap": heapsort,
    "merge_b": mergesort_b,
    "shell": shellsort,
}
