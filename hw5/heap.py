##############################################################
#
# Algorithms HW5-2
# 202413755 Yeonjun Kim
#
# heap class implementation: MinHeap, FiboHeap
#
##############################################################

import math

class MinHeapNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class MinHeap:
    def __init__(self):
        self.heap = []  # list to store the binary heap
        self.idxdict = {} # maps a MinHeapNode reference to index in heap list

    def insert(self, key, value):
        node = MinHeapNode(key, value)
        self.heap.append(node)
        self.idxdict[node] = len(self.heap) - 1
        self._sift_up(len(self.heap) - 1)
        return node

    def _sift_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[index].key < self.heap[parent].key:
                self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
                self.idxdict[self.heap[index]] = index
                self.idxdict[self.heap[parent]] = parent
                index = parent
            else:
                break

    def decrease_key(self, node: MinHeapNode, new_key: int):
        index = self.idxdict[node]
        if new_key < node.key:
            node.key = new_key
            self._sift_up(index)

    def pop(self):
        if not self.heap:
            return None
        min_node = self.heap[0]
        del self.idxdict[min_node]

        last_node = self.heap.pop()
        if self.heap:
            self.heap[0] = last_node
            self.idxdict[last_node] = 0
            self._sift_down(0)
        return min_node

    def _sift_down(self, index):
        size = len(self.heap)
        while True:
            smallest = index
            left = 2 * index + 1
            right = 2 * index + 2

            if left < size and self.heap[left].key < self.heap[smallest].key:
                smallest = left
                self.idxdict[self.heap[smallest]] = smallest
            if right < size and self.heap[right].key < self.heap[smallest].key:
                smallest = right
                self.idxdict[self.heap[smallest]] = smallest

            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                self.idxdict[self.heap[index]] = index
                self.idxdict[self.heap[smallest]] = smallest
                index = smallest
            else:
                break

class FiboHeapNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        
        self.parent = None  # parent node
        self.child = None   # first child node
        self.left = self    # siblings
        self.right = self   # siblings

        self.degree = 0  # number of children
        self.marked = False

class FiboHeap:
    def __init__(self):
        self.min_node = None    # reference to the node with minimum key
        self.num_nodes = 0

    def _insert_new_root(self, node):
        node.left = node.right = node
        node.parent = None
        if self.min_node is None:
            self.min_node = node
        else:
            # insert node into double linked list of root nodes
            node.left = self.min_node
            node.right = self.min_node.right
            self.min_node.right.left = node
            self.min_node.right = node

            # update min_node if necessary
            if node.key < self.min_node.key:
                self.min_node = node

    def _remove_root(self, node):
        if node.right == node:  # only one node in root list
            self.min_node = None
        else:
            node.left.right = node.right
            node.right.left = node.left
            if self.min_node == node:
                self.min_node = node.right

    def _cut(self, x, parent):  # remove x from parent's child list
        if x.right != x:  # x has siblings
            x.right.left = x.left
            x.left.right = x.right
        if parent.child == x:
            if x.right != x:
                parent.child = x.right
            else:
                parent.child = None
        x.left = x.right = x
        x.parent = None
        x.marked = False
        parent.degree -= 1

    def _link(self, x, parent): # make x a child of parent
        x.left = x.right = x
        if parent.child is None:
            parent.child = x
        else:
            x.left = parent.child
            x.right = parent.child.right
            parent.child.right.left = x
            parent.child.right = x
        x.parent = parent
        parent.degree += 1
        parent.marked = False

    def _consolidate(self):
        if self.min_node is None:
            return
        
        nodes = [] # list of root nodes to iterate over
        start = self.min_node
        cur = start
        while True:
            nodes.append(cur)
            cur = cur.right
            if cur == start:
                break

        # combine trees
        max_degree = int(math.log(self.num_nodes) * 2) + 1
        A = [None] * max_degree
        for node in nodes:
            d = node.degree
            while A[d] is not None: # if there is another tree with same degree -> merge
                other = A[d]
                if node.key > other.key:
                    node, other = other, node
                self._remove_root(other)
                self._link(other, node)
                A[d] = None
                d += 1
            A[d] = node

        # rebuild root list and find new min_node
        # haha I trust the garbage collector
        self.min_node = None
        for i in range(max_degree):
            if A[i] is not None:
                self._insert_new_root(A[i])
                if A[i].key <= self.min_node.key:
                    self.min_node = A[i]

    def insert(self, key, value):  # O(1)
        node = FiboHeapNode(key, value)
        self._insert_new_root(node)
        self.num_nodes += 1
        return node

    def decrease_key(self, node: FiboHeapNode, new_key: int): # O(1) amortized
        # 1. update key
        node.key = new_key

        # 2. cut node from its parent if necessary
        x = node
        y = x.parent
        while y is not None and x.key < y.key: # if x violates min heap property
            # cut x from y
            self._cut(x, y)

            # add x to root list
            self._insert_new_root(x)
            
            if not y.marked:
                y.marked = True
                break
            x, y = y, y.parent

        # 3. update min_node if necessary
        if self.min_node is None or node.key < self.min_node.key:
            self.min_node = node

    def pop(self): # O(log n) amortized
        if self.min_node is None:
            return None
        min_node = self.min_node
        ret = min_node
        
        # 1. remove min_node and add its children to root list
        child = min_node.child
        while child is not None:
            child_next = child.right
            self._insert_new_root(child)
            if child_next == min_node.child:
                break
            child = child_next

        self._remove_root(min_node)
        self.num_nodes -= 1

        # 2. consolidate trees in root list         -> O(log n) amortized
        if self.min_node is not None:
            self._consolidate()
        return ret

# for testing correctness
if __name__ == "__main__":
    # simple test
    fheap = FiboHeap()
    fheap.insert(5, 'A')
    fheap.insert(3, 'B')
    fheap.insert(8, 'C')
    fheap.insert(2, 'D')

    print(fheap.pop().value)  # (2, 'D')
    print(fheap.pop().value)  # (3, 'B')
    print(fheap.pop().value)  # (5, 'A')
    print(fheap.pop().value)  # (8, 'C')