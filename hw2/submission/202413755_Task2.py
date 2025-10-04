import random   # for quicksort
import time

############### below: sorting algorithm implementations #############

# Insertion Sort
def Insert_Sort(arr):
    N = len(arr)
    for i in range(1, N):
        for j in range(i, 0, -1):
            # if the latter element is smaller, bring it forward
            if arr[j] < arr[j-1]:
                arr[j], arr[j-1] = arr[j-1], arr[j]
            # otherwise, stop bringing the element
            else:
                break
    return

# Merge Sort (in-place)
def _Merge_Sort(arr, l, r):
    if r <= l: # base case
        return

    # Recurse 
    mid = (l + r) // 2
    _Merge_Sort(arr, l, mid)
    _Merge_Sort(arr, mid + 1, r)
    
    # Merge
    part1 = arr[l:mid]
    part2 = arr[mid+1:r]
    p = 0
    q = 0
    k = l
    while p < len(part1) and q < len(part2):
        if part1[p] < part2[q]:
            arr[k] = part1[p]
            p += 1
        else:
            arr[k] = part2[q]
            q += 1
        k += 1
    while p < len(part1):
        arr[k] = part1[p]
        p += 1
        k += 1
    while q < len(part2):
        arr[k] = part2[q]
        q += 1
        k += 1

def Merge_Sort(arr):
    _Merge_Sort(arr, 0, len(arr)-1)


# Quick Sort (in-place)
def _Quick_Sort(arr, l, r):
    if r <= l: # base case
        return
    
    # choose random pivot
    i = random.randint(l, r)
    pivot = arr[i]

    # partition the array
    arr[i], arr[r] = arr[r], arr[i] # swap(i, r)
    p = l # leading pointer
    q = l
    while p <= r-1:
        p += 1
        if arr[p] < pivot:
            arr[p], arr[q] = arr[q], arr[p] # swap(p, q)
            q += 1
    # bring pivot back to position
    arr[q], arr[r] = arr[r], arr[q] # swap(q, r)

    # recurse
    _Quick_Sort(arr, l, q)
    _Quick_Sort(arr, q+2, r)

def Quick_Sort(arr):
    _Quick_Sort(arr, 0, len(arr)-1)


# Dual-Pivot Quick Sort (in-place)
def _Quick_DualPivot_Sort(arr, l, r):
    if r <= l: # base case
        return
    
    # randomly choose two pivots
    i1 = random.randint(l, r)
    i2 = random.randint(l, r)
    arr[i1], arr[l] = arr[l], arr[i1] # swap(i1, l)
    arr[i2], arr[r] = arr[r], arr[i2] # swap(i2, r)
    if arr[l] > arr[r]:
        arr[l], arr[r] = arr[r], arr[l] # swap(l, r)
    pivot1 = arr[l]
    pivot2 = arr[r]
    
    # partition the array (Yaroslavskiy's partitioning algorithm)
    i = l+1
    j = r-1
    k = i
    while k <= j:
        if arr[k] < pivot1:
            arr[k], arr[i] = arr[i], arr[k] # swap(k, i)
            i += 1
        elif arr[k] >= pivot2:
            while arr[j] > pivot2 and k < j:
                j -= 1
            arr[k], arr[j] = arr[j], arr[k] # swap(k, j)
            j -= 1
            if arr[k] < pivot1:
                arr[k], arr[i] = arr[i], arr[k] # swap(k, i)
                i += 1
        k += 1  
    
    # bring pivots back to position
    i -= 1
    j += 1
    arr[l], arr[i] = arr[i], arr[l] # swap(l, i)
    arr[r], arr[j] = arr[j], arr[r] # swap(r, j)

    # recurse
    _Quick_DualPivot_Sort(arr, l, i-1)
    _Quick_DualPivot_Sort(arr, i+1, j-1)
    _Quick_DualPivot_Sort(arr, j+1, r)

def Quick_DualPivot_Sort(arr):
    _Quick_DualPivot_Sort(arr, 0, len(arr)-1)


############# below: I/O helper functions #############

def read_input(path):
    try:
        with open(path, "r") as f:
            N = int(f.readline())
            arr = [int(x) for x in f.read().strip().split()]
        return N, arr
    except:
        return None, None

def write_output(path, arr):
    with open(path, 'w') as f:
        for x in arr:
            f.write(f"{x} ")
        f.write("\n")

def print_time(algo_name, runtime):
    print("----- RUNTIME MEASUREMENTS -----")
    for i in range(len(algo_name)):
        print(f"{algo_name[i]} Sort: took {runtime[i]:.3f} ms.")

def write_time(path, algo_name, runtime):
    with open(path, "a") as f:
        f.write("\n----- RUNTIME MEASUREMENTS -----\n")
        for i in range(len(algo_name)):
            f.write(f"{algo_name[i]} Sort: {runtime[i]:.3f} ms.\n")


################ below: main function ##################

ALGO_LIST = [Insert_Sort, Merge_Sort, Quick_Sort, Quick_DualPivot_Sort]
ALGO_NAME_LIST = ["Insert", "Merge", "Quick", "QuickDualPivot"]

if __name__ == "__main__":
    print("============================================")
    print("    4190.407 Algorithms - Homework 2")
    print("    Sorting Algorithms Implementation")
    print("    Yeonjun Kim / 2024-13755")
    print("============================================")
    print("\n")

    # (1) Read input
    print("Reading input from 'input.txt'...\n")
    N, arr = read_input("input.txt")
    if N is None or arr is None or len(arr) != N:
        print("[Error] failed to read input.")
        print("You should provide an input file named 'input.txt' in the current directory.")
        print("The first line should contain a single integer N (number of integers to sort).")
        print("The second line should contain N integers separated by spaces.")
        print("\n(example)\n5")
        print("3 5 1 4 2\n")
        exit(-1)

    print(f"Successfully read {N} numbers.")

    # (2) Run sorting algorithms and measure runtime
    print("\nRunning sorting algorithms...")

    runtime = []
    target = None
    for i, algo in enumerate(ALGO_LIST):
        target = arr.copy()
        time_start = time.process_time()
        
        algo(target)
        
        time_end = time.process_time()

        runtime_ms = (time_end - time_start) * 1000
        runtime.append(round(runtime_ms, 3))

        print(f"* {ALGO_NAME_LIST[i]} completed in {runtime_ms:.3f} ms.")

    # (3) write output and runtime measurements
    print("\nWriting output to 'output.txt'...")
    write_output("output.txt", target)
    write_time("output.txt", ALGO_NAME_LIST, runtime)
    print("All done.")

    exit(0)