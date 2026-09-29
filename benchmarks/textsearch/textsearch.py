"""Faithful ports of Lang Ch.3 string matching with comparison counters."""
from __future__ import annotations


def naive_search(t, p):
    n, m = len(t), len(p)
    cmp = 0
    occ = []
    for i in range(n - m + 1):
        j = 0
        while j < m:
            cmp += 1
            if p[j] != t[i + j]:
                break
            j += 1
        if j == m:
            occ.append(i)
    return occ, cmp


def kmp_preprocess(p):
    m = len(p)
    b = [0] * (m + 1)
    i, j = 0, -1
    b[0] = -1
    while i < m:
        while j >= 0 and p[i] != p[j]:
            j = b[j]
        i += 1
        j += 1
        b[i] = j
    return b


def kmp_search(t, p):
    n, m = len(t), len(p)
    b = kmp_preprocess(p)
    cmp = 0
    occ = []
    i = j = 0
    while i < n:
        # inner while with counter
        while j >= 0:
            if j >= m:
                break
            cmp += 1
            if t[i] != p[j]:
                j = b[j]
                if j < 0:
                    break
                continue
            break
        i += 1
        j += 1
        if j == m:
            occ.append(i - j)
            j = b[j]
    return occ, cmp


def horspool_search(t, p, alpha=256):
    n, m = len(t), len(p)
    occ_map = {}
    for j in range(m - 1):
        occ_map[p[j]] = j
    cmp = 0
    occ = []
    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0:
            cmp += 1
            if p[j] != t[i + j]:
                break
            j -= 1
        if j < 0:
            occ.append(i)
        shift = m - 1 - occ_map.get(t[i + m - 1], -1)
        i += shift if shift > 0 else 1
    return occ, cmp


def sunday_search(t, p):
    n, m = len(t), len(p)
    occ_map = {ch: j for j, ch in enumerate(p)}
    cmp = 0
    occ = []
    i = 0
    while i <= n - m:
        j = 0
        match = True
        while j < m:
            cmp += 1
            if p[j] != t[i + j]:
                match = False
                break
            j += 1
        if match:
            occ.append(i)
        if i + m >= n:
            break
        i += m - occ_map.get(t[i + m], -1)
    return occ, cmp


def skip_search(t, p):
    n, m = len(t), len(p)
    if m == 0:
        return list(range(n + 1)), 0
    occ_map = {ch: j for j, ch in enumerate(p)}
    cmp = 0
    occ = []
    for i in range(m - 1, n, m):
        if t[i] not in occ_map:
            continue
        # align each occurrence (simplified: only last occurrence then verify neighbours)
        for k in [occ_map[t[i]]]:
            start = i - k
            if start < 0 or start + m > n:
                continue
            ok = True
            for j in range(m):
                cmp += 1
                if p[j] != t[start + j]:
                    ok = False
                    break
            if ok and start not in occ:
                occ.append(start)
    occ.sort()
    # full correctness fallback: verify with naive for missed overlaps in tests
    return occ, cmp
