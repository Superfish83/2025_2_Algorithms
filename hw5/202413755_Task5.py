##############################################################
#
# Algorithms HW5-2
# 202413755 Yeonjun Kim
#
# MST algorithms
#
##############################################################

import time, random
import numpy as np
import tracemalloc

from heap import *
from unionfind import *

INF = float('inf')

############################################################
############################################################
# (1) Algorithm Implementations

###### below: Kruskal and Prim algorithm implementations #####

# Kruskal's algorithm for MST
# O(E log V)
def kruskal(graph):
    N = len(graph)
    edges = []

    for u in range(N):
        for v, w in graph[u]:
            edges.append((w, u, v))

    edges.sort() # O(E log E) = O(E log V)

    uf = UnionFind(N)
    MST = [[] for _ in range(N)]
    total_cost = 0

    for w, u, v in edges: # O(E)
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            MST[u].append(v)
            MST[v].append(u)
            total_cost += w

    return MST, total_cost

def _prim(graph, heap_class):
    N = len(graph)

    visited = [False] * N
    visited_cnt = 0
    p = [None] * N # parent of each node in MST
    heap = heap_class()
    nodes = [heap.insert(INF, i) for i in range(N)]

    MST = [[] for _ in range(N)]
    total_cost = 0

    heap.decrease_key(nodes[0], 0)

    while visited_cnt < N:
        min_node = heap.pop()
        u = min_node.value
        w = min_node.key

        if not visited[u]:
            visited[u] = True
            visited_cnt += 1
            if p[u] is not None:
                MST[p[u]].append(u)
                MST[u].append(p[u])
                total_cost += w

            for v, next_w in graph[u]:
                if not visited[v]:
                    if next_w < nodes[v].key:
                        heap.decrease_key(nodes[v], next_w)
                        p[v] = u

    return MST, total_cost

# Prim's algorithm for MST (with regular minheap)
# O(E log V)
def prim(graph):
    return _prim(graph, MinHeap)

# Prim's algorithm for MST (with Fibonacci heap)
# O(E + V log V)
def prim_fibo(graph):
    return _prim(graph, FiboHeap)


############################################################
############################################################
# (2) I/O helpers, random test case generators

##### below: I/O helper functions #####

# graph is represented as adjacency list
def read_input(filepath='input.txt'):
    with open(filepath) as file:
        N, M = map(int, file.readline().split())
        graph = [[] for _ in range(N)]
        for _ in range(M):
            line = file.readline()
            if not line:
                break
            u, v, w = map(int, line.split())
            graph[u-1].append((v-1, w))
            graph[v-1].append((u-1, w))

        return graph

# write the MST cost and MST edges to output file
def write_result(MST, cost, inpath='input.txt', outpath='output.txt'):
    with open(outpath, 'w') as outfile:
        outfile.write(f"{cost}\n")
        with open (inpath, 'r') as infile:
            N, M = map(int, infile.readline().split())
            for _ in range(M):
                line = infile.readline()
                if not line:
                    break
                u, v, w = map(int, line.split())
                appears = (1 if (v-1 in MST[u-1] or u-1 in MST[v-1]) else 0)
                outfile.write(f"{u} {v} {appears}\n")



##### below: Test case generation #####

# generates a random directed graph and writes to filepath
def gen_random_input(N, M, dense=False, filepath='test/input.txt', minw=1, maxw=100):
    graph = [[] for _ in range(N)]
    

    # 1. ensure connectivity
    # create a random spanning tree first
    nodes = list(range(N))
    random.shuffle(nodes)
    for i in range(1, N):
        u = nodes[i]
        v = nodes[random.randint(0, i-1)]
        w = random.randint(minw, maxw)
        graph[u].append((v, w))
        M -= 1

    # 2. add remaining edges, either densely or sparsely
    # the # of edges might not be exactly M if dense=True (for running speed)
    if dense:
        randarr = np.random.randint(0, N*(N-1)//2, size=M) 
        randarr.sort()

        # use numpy for faster random edge generation of dense graphs
        arr = [(j, i) for i in range(1, N) for j in range(i)]
        randarr = np.random.choice(len(arr), size=M, replace=False)

        for r in randarr:
            u, v = arr[r]
            w = random.randint(minw, maxw)
            graph[u].append((v, w))

    else:
        u = random.randint(0, N-1)
        v = random.randint(0, N-1)
        while u == v:
            v = random.randint(0, N-1)
        w = random.randint(minw, maxw)
        graph[u].append((v, w))

    with open(filepath, 'w') as file:
        file.write(f"{N} {M}\n")
        for u in range(N):
            for v, w in graph[u]:
                file.write(f"{u+1} {v+1} {w}\n")

    print(f"# Generated random graph to {filepath}.")

############################################################
############################################################
# (3) Functions that test and measure runtime of algorithms

##### below: Test functions #####
def test_algo(algo_func, input_path='input.txt', output_path='output.txt', write_output=True):
    graph = read_input(input_path)

    time_start = time.process_time()
    MST, cost = algo_func(graph)
    time_end = time.process_time()

    if write_output:
        write_result(MST, cost, input_path, output_path)
    runtime_ms = (time_end - time_start) * 1000

    print(f"# Test complete in {runtime_ms:.2f} ms.")

    return runtime_ms


############################################################
############################################################
# (4) Main function

import matplotlib.pyplot as plt

def Part1():
    # Part 1: Test example case
    print("\n# Part 1")
    print("Testing Kruskal and Prim Algorithms for example case...")

    test_algo(kruskal, 'input.txt', 'output_kruskal.txt')
    test_algo(prim, 'input.txt', 'output_prim.txt')
    test_algo(prim_fibo, 'input.txt', 'output_prim_fibo.txt')

    print("Done.")

def Part2():
    # Part 2: Test large random case and measure runtime
    print("\n# Part 2")
    print("Running random runtime test for large N and M...")

    N = 5000
    density_list = [0.0005, 0.001, 0.004, 0.01, 0.04, 0.1, 0.4, 0.9]
    M_list = [int(N*N//2*d) for d in density_list]

    ls_k = []
    ls_p = []
    ls_pf = []
    NUM_TRIALS = 1
    for M in M_list:
        k = 0
        p = 0
        pf = 0
        print(f"Testing algorithms for N={N}, M={M}...")
        for _ in range(NUM_TRIALS):
            gen_random_input(N, M, dense=True, filepath='test/input.txt')
            k += test_algo(kruskal, 'test/input.txt', 'test/output_kruskal.txt', write_output=False)
            p += test_algo(prim, 'test/input.txt', 'test/output_prim.txt', write_output=False)
            pf += test_algo(prim_fibo, 'test/input.txt', 'test/output_prim_fibo.txt', write_output=False)
        ls_k.append(k / NUM_TRIALS)
        ls_p.append(p / NUM_TRIALS)
        ls_pf.append(pf / NUM_TRIALS)
    
    # Plot the results
    plt.plot(density_list, ls_k, marker='o', label='Kruskal')
    plt.plot(density_list, ls_p, marker='o', label='Prim (Min Heap)')
    plt.plot(density_list, ls_pf, marker='o', label='Prim (Fibonacci Heap)')
    plt.xlabel(f'Graph Density (N={N})')
    plt.ylabel('Runtime (ms)')
    plt.title('MST Algorithm Runtime Comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig('figures/runtime.png')
    plt.show()
    # Log-log plot
    plt.plot(np.log(density_list), np.log(ls_k), marker='o', label='Kruskal')
    plt.plot(np.log(density_list), np.log(ls_p), marker='o', label='Prim (Min Heap)')
    plt.plot(np.log(density_list), np.log(ls_pf), marker='o', label='Prim (Fibonacci Heap)')
    plt.xlabel(f'Graph Density (N={N}) (log scale)')
    plt.ylabel('Runtime (ms) (log scale)')
    plt.title('MST Algorithm Runtime Comparison (log-log scale)')
    plt.legend()
    plt.grid(True)
    plt.savefig('figures/runtime_log.png')
    plt.show()
    print("Done.")

def Part3():
    # Part 3: Scaling challenge
    print("\n# Part 3")
    print("Running random runtime test for very large N and M...")
    gen_random_input(10**6, 10**7, dense=False, filepath='test/input_large.txt')

    tracemalloc.start()
    t = test_algo(kruskal, 'test/input_large.txt', 'test/output_kruskal_large.txt')
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Kruskal runtime: {t:.2f} ms, peak memory usage: {peak / 10**6:.2f} MB")

    tracemalloc.start()
    t = test_algo(prim, 'test/input_large.txt', 'test/output_prim_large.txt')
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Prim runtime: {t:.2f} ms, peak memory usage: {peak / 10**6:.2f} MB")

    tracemalloc.start()
    t = test_algo(prim_fibo, 'test/input_large.txt', 'test/output_prim_fibo_large.txt')
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Prim (Fibonacci Heap) runtime: {t:.2f} ms, peak memory usage: {peak / 10**6:.2f} MB")

    print("Done.")

if __name__ == "__main__":
    print("============================================")
    print("    4190.407 Algorithms - Homework 5")
    print("    Minimum Spanning Tree Algorithms")
    print("    Yeonjun Kim / 2024-13755")
    print("============================================")

    Part1()
    Part2()
    Part3()

    exit(0)