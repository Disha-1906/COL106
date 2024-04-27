class Node:
    def __init__(self, id, edge_weight):
        self.id = id
        self.edge_weight = edge_weight
        self.next = None
        self.parent = None
        self.label = None
class Graph:
    def __init__(self, num):
        self.V = num
        self.graph = [[] for i in range(num)]

    def insert_edge(self, s, id,w):
        self.graph[s].append((id,w))
        self.graph[id].append((s,w))

class Priority_Queue():
    def __init__(self):
        self._data = []
    def _parent(self,j):
        return (j-1)//2
    def _left(self,j):
        return 2*j+1
    def _right(self,j):
        return 2*j+2
    # Returns True/False depending on whether j has left/right child
    def _has_left(self,j):
        return self._left(j)<len(self._data)
    def _has_right(self,j):
        return self._right(j)<len(self._data)
    # Swaps positions of Items i and j
    def getparent(self, index):   #returns the index of parent of a given index
        return (index - 1) // 2
    def getleftchild(self, index): #returns the index of left child of a given index
        return (2 * index) + 1
    def getrightchild(self, index): #returns the index of right child of a given index
        return (2 * index) + 2
    def hasparent(self, index):  # says whether a given index has a parent or not
        return self.getparent(index) >= 0
    def hasleftchild(self, index): #says whether a given index has a left child or not
        return self.getleftchild(index) < len(self._data)
    def hasrightchild(self, index): #says whether a given index has a right child or not
        return self.getrightchild(index) < len(self._data)  
    def _swap(self,i,j):
        self._data[i],self._data[j]=self._data[j],self._data[i]
    # def _upheap(self, j,arr1,arr2):
    #     print(self._data,arr1, arr2)
    #     parent = self.getparent(j)
    #     if j>0 and (self._data[j])[1] > (self._data[parent])[1]:
    #         self._swap(j, parent)
    #         arr2[self._data[j][0]],arr2[self._data[parent][0]]= arr2[self._data[parent][0]],arr2[self._data[j][0]]
    #         self._upheap(parent,arr1,arr2)       
    # def _downheap(self, j,arr1,arr2):
    #     if self._has_left(j):
    #         left = self._left(j)
    #         small_child = left 
    #         if self._has_right(j):
    #             right = self._right(j)
    #             if arr1[self._data[right][0]] > arr1[self._data[left][0]]:
    #                 small_child = right           
    #         if arr1[self._data[small_child][0]] > arr1[self._data[j][0]]:
    #             self._swap(j, small_child)
    #             arr2[self._data[j]._mass],arr2[self._data[small_child]._mass]= arr2[self._data[small_child]._mass],arr2[self._data[j]._mass]
    #             self._downheap(small_child,arr1,arr2)   
    def upheap(self,index,arr):   #given a index, it traverses up the heap until the heap property is restored
                                  # if the key of the child is smaller than its parent then it swaps the two traverses up
                                  #correspondingly it also swaps the same values in the given array
        if(self.hasparent(index) and self._data[self.getparent(index)][1]<self._data[index][1]):
            self._swap(self.getparent(index),index)  
            arr[self._data[self.getparent(index)][0]],arr[self._data[index][0]]=arr[self._data[index][0]],arr[self._data[self.getparent(index)][0]]
            self.upheap(self.getparent(index),arr)

    def downheap(self, j,arr):   #given a index , it traverses down the heap until the heap property is restored 
                                   #if the parent node has a greater key value than its child it swaps the parent item with the minimum of the two children 
                                   #correspondingly it also swaps the same values in the given array
        if self.hasleftchild(j):
            left = self.getleftchild(j)
            large_child = left
            if self.hasrightchild(j):
                right = self.getrightchild(j)
                if self._data[right][1] > self._data[left][1]:
                    large_child = right
            if self._data[large_child][1] > self._data[j][1]:
                self._swap(j, large_child)
                arr[self._data[j][0]], arr[self._data[large_child][0]] = arr[self._data[large_child][0]],arr[self._data[j][0]]
                self.downheap(large_child,arr)
    # def change_time(self,i,new,arr):
    #     self._data[arr[i]]._rel_time = new
    # Returns length
    def __len__(self):
        return len(self._data)

    # Does heapdown for every node, starting from the second last level
    def _heapify(self,arr1):
        start = self._parent(len(self)-1)
        for j in range(start,-1,-1):
            self.downheap(j,arr1)
    # Builds queue give a list of tuples (t,m) after converting them into item
    # def build_queue(self,lis = []):
    #     self._data=[self._Item(t,m) for t,m in lis]
    #     if len(self._data)>1:
    #         self._heapify([0]*(len(lis)))
    def enqueue(self,id,arr1):
        n=len(self._data)
        if len(self._data)==0:
            self._data.append([id,arr1[id]])
        else:
            self._data.append([id,arr1[id]])
            self.upheap(len(self._data)-1,arr1)
    def dequeue(self):   #this gives the item at root of the heap
        n = len(self._data)
        if len(self._data) == 0:
            print(" Priority queue is empty.")
        it = self._data[0]
        return (it.id, it.edge_weight)
    def extractMax(self,arr1):
 
        # Return NULL wif heap is empty
        if len(self._data )== 0:
            return
 
        # Store the root node
        root = self._data[0]
        # print('root is', root)
        # print('heap is', self._data)
 
        # Replace root node with last node
        lastNode = self._data[len(self._data) - 1]
        self._data[0] = lastNode
        self._data.pop()
        # Update position of last node
        arr1[lastNode[0]] = 0
        arr1[root[0]] = '*'
 
        # Reduce heap size and heapify root
        self.downheap(0,arr1)
 
        return root

    # def _heapify(self,arr):
    #     start = self._parent(len(self)-1)
    #     for j in range(start,-1,-1):
    #         self._downheap(j,arr)
    # # Builds queue give a list of tuples (t,m) after converting them into item
    # def build_queue(self,lis = []):
    #     self._data=[Node(t,m) for t,m in lis]
    #     if len(self._data)>1:
    #         self._heapify([0]*(len(lis)))

    def update(self, to_be,arr1,arr2): # given an index and a value, it updates the value at the index with the new given value
        # print(arr2)
        if self._data[arr2[to_be]][1] <arr1[self._data[arr2[to_be]][0]]:
            self._data[arr2[to_be]][1] = arr1[self._data[arr2[to_be]][0]]
            self.upheap(arr2[to_be],arr2)  

def minima(a,b):
    if b==0:
        return a
    else:
        return min(a,b)

def findMaxCapacity(n,links,s,t):
    packet_size = [float('-inf') for i in range(n)]
    prev = [None for i in range(n)]
    packet_size[s]=float('inf')
    network = Graph(n)
    index_list = [0] * (n)
    for i in (links):
        (a,b,c) = (i[0],i[1],i[2])
        network.insert_edge(a,b,c)
    heap = Priority_Queue()
    for j in range(0,n):
        if j == s:
            heap.enqueue(s,packet_size)
        else:
            heap.enqueue(j,packet_size)
        index_list[heap._data[j][0]] = j
    # size = len(heap._data)
    while len(heap._data)!=0:
        # if size==3 :
        #     print(heap._data)
        curr_vertex = heap.extractMax(index_list)
        # print(curr_vertex)
        # if curr_vertex!=None:
        neighbour = network.graph[curr_vertex[0]]
        # print('neighbour is',neighbour)
        for v in neighbour:
            if index_list[v[0]]!='*':
                new_cap = minima(curr_vertex[1],v[1])
                # if v[0]==12:
                    # print('new_cap is',new_cap)
                    # print(packet_size[curr_vertex[0]])
                    # print(v[1])
                if new_cap> packet_size[v[0]]:
                    packet_size[v[0]]= new_cap
                    prev[v[0]] = curr_vertex[0]
                    # print(v)
                    heap.update(v[0],packet_size,index_list)
    path = []
    u = t 
    # print(prev)
    # print(u)
    while u!=None:
        path.append(u)
        u = prev[u]
    path.reverse() 
    return (packet_size[t], path)
    # print
        
# print(findMaxCapacity(3,[(0,1,1),(1,2,1)],0,1))
# print(findMaxCapacity(4,[(0,1,30),(0,3,10),(1,2,40),(2,3,50),(0,1,60),(1,3,50)],0,3))
# print(findMaxCapacity(4,[(0,1,30),(1,2,40),(2,3,50),(0,3,10)],0,3))
# print(findMaxCapacity(5,[(0,1,3),(1,2,5),(2,3,2),(3,4,3),(4,0,8),(0,3,7),(1,3,4)],0,2))
# print(findMaxCapacity(7,[(0,1,2),(0,2,5),(1,3,4), (2,3,4),(3,4,6),(3,5,4),(2,6,1),(6,5,2)],0,5))
# print(findMaxCapacity(7,[(0,1,2),(0,2,5),(1,3,4), (2,3,4),(3,4,6),(3,5,4),(2,6,1),(6,5,2)],0,5))