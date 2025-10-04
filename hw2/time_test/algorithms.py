import random   # for quicksort


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