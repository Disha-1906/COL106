# Priority Queue using min heap implementation using min heap has been used.
# Given below is the item class whose object consists of two values -_rel_time(time taken for (i)th and (i+1)th particle to collide) and _mass which stores the index i of the  particle.

class Priority_Queue_Base:
    class _Item:
        __data__ ='_rel_time','_mass'
        def __init__(self,t,m):
            self._rel_time = t
            self._mass = m       
        def __compare__(self, other):
            return self._rel_time < other._rel_time
        def is_empty(self):
            return len(self)==0

# Below class is the priority queue which uses _rel_time as its key and _mass as its value.

class Priority_Queue(Priority_Queue_Base):
    # Returns Parent
    def _parent(self,j):
        return (j-1)//2
    # Returns Left Child/ Right Child
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
    def _swap(self,i,j):
        self._data[i],self._data[j]=self._data[j],self._data[i]
    # Shifts current item up if its key value is less than it parent
    def _upheap(self, j, arr):
        parent = self._parent(j)
        if j>0 and self._data[j]._rel_time < self._data[parent]._rel_time:
            self._swap(j, parent)
            arr[self._data[j]._mass],arr[self._data[parent]._mass]= arr[self._data[parent]._mass],arr[self._data[j]._mass]
            self._upheap(parent, arr)   
    # Shifts current item down if its key value is graeter than parent   
    def _downheap(self, j, arr):
        if self._has_left(j):
            left = self._left(j)
            small_child = left 
            if self._has_right(j):
                right = self._right(j)
                if self._data[right]._rel_time < self._data[left]._rel_time:
                    small_child = right           
            if self._data[small_child]._rel_time < self._data[j]._rel_time:
                self._swap(j, small_child)
                arr[self._data[j]._mass],arr[self._data[small_child]._mass]= arr[self._data[small_child]._mass],arr[self._data[j]._mass]
                self._downheap(small_child , arr) 
    # The function below is used to change the value of key (here _rel_time) of the required particles once a collision takes place. The correct positions of these particles are being accessed using the array arr which stores the index of the particles in queue. Whatever swapping takes place in queue, also takes place in the array arr and hence it has been given as argument in upheap and downheap, updating it as required.
    def change_time(self,i,new,arr):
        self._data[arr[i]]._rel_time = new
    def __init__(self):
        self._data = [ ]
    # Returns length
    def __len__(self):
        return len(self._data)
    # Inserts item
    def insert(self, t, m):
        self._data.append(self._Item(t,m))
        self._upheap(len(self._data)-1)
    # Returns the top item (which is minimum) 
    def min(self):
        # if self.is_empty( ):
        #     raise Empty( 'Priority queue is empty.' )
        item = self._data[0]
        return (item._rel_time, item._mass)
    # Removes the minimum item
    def remove_min(self):
        # if self.is empty( ):
        #     raise Empty( Priority queue is empty. )
        self._swap(0, len(self._data)-1)
        item = self._data.pop( ) 
        self._downheap(0) 
        return (item._rel_time, item._mass)
    # Prints the contents of the queue 
    def show(self):
        for i in range(len(self._data)):
            print(self._data[i]._rel_time, self._data[i]._mass)
    # Does heapdown for every node, starting from the second last level
    def _heapify(self,arr):
        start = self._parent(len(self)-1)
        for j in range(start,-1,-1):
            self._downheap(j,arr)
    # Builds queue give a list of tuples (t,m) after converting them into item
    def build_queue(self,lis = []):
        self._data=[self._Item(t,m) for t,m in lis]
        if len(self._data)>1:
            self._heapify([0]*(len(lis)))
        
my_queue = Priority_Queue()

def listCollisions(M,x,v,m,T):

    # Below loop traverses along the list of particles and calculates time for each pair of consecutive particles to collide, and storing this time and the index of particle i in a tuple called my_pair. Finally this tuple is appended to final list which is then used to build queue.
    final_list = [] 
    for i in range(0,len(M)-1):
        mm = i
        if v[i]-v[i+1]>0:
            tt = abs((x[i+1]-x[i])/(v[i]-v[i+1]))
        else:
            tt = float('inf')
        my_pair = (tt,mm)
        final_list.append(my_pair)

    # Building my_queue from final list
    my_queue.build_queue(final_list)

    # This ar is used to access the paticle whose rel_time needs to be updated. The values in this array in such a way that at index of ar equal to the _mass of the particle, the value of its index in the queue.
    ar=[0]*(len(M)-1)
    for i in range(0,len(my_queue._data)):
        ar[my_queue._data[i]._mass]=i

    # This list keeps a track of time upto which the position of the particle has been updated.
    new_time = []   
    for i in range(0,len(M)):
        new_time.append(0)

    # Tracker stores the previous collision time and checks whether the next collision is also taking place at same time or not.
    tracker = []
    tracker.append(0)
    time = 0
    count = 0
    final=[]
    col=[]
    t_coll=0

    # This is the main loop which runs until time becomes greater than req time or count >m. First, the queue contains the particle whose collision is going to take place, at the top. The final velocities of these particles is calculated and their positions and velocities are updated. The rel_time of adjacent particles is updated. Finally, rel_time of the particle that kust collided is made inf. Each time an update is made heapup or heapdown is done as required. Finally the required output is returned.
    while t_coll<T and count<m  :
        t_coll = my_queue._data[0]._rel_time
        if t_coll!= tracker[0]:
            time = time+t_coll
            tracker.pop()
            tracker.append(t_coll)
        m_index = my_queue._data[0]._mass
        m1 = M[m_index]
        m2 = M[m_index+1]
        u1 = v[m_index]
        u2 = v[m_index+1]
        v1 = (((m1-m2)*u1)+2*m2*u2)/(m1+m2)
        v2 = (((m2-m1)*u2)+2*m1*u1)/(m1+m2)
        v[m_index]=v1
        v[m_index+1]=v2
        x[m_index]+=u1*(t_coll - new_time[m_index])
        coll_1 = (t_coll,m_index,x[m_index])
        if coll_1[0]<=T:
            col.append(coll_1)
        coll = (round(t_coll,4),m_index,round(x[m_index],4))
        if coll[0]<=T:
            final.append(coll)
        new_time[m_index]=t_coll
        x[m_index+1]=x[m_index]
        new_time[m_index+1]=t_coll
        # change_priority at m[index-1]
        if m_index-1>=0:
            if v[m_index-1]-v[m_index]>0:
                n1 = x[m_index-1] + v[m_index-1]*(t_coll-new_time[m_index-1])
                n_t = abs((x[m_index]-n1)/(v[m_index-1]-v[m_index]))+ t_coll
            else:
                n_t = float('inf')
            k = my_queue._data[ar[m_index-1]]._rel_time
            my_queue.change_time(m_index-1,n_t,ar)
            if n_t>k:
                my_queue._downheap(ar[m_index-1],ar)
            else:
                my_queue._upheap(ar[m_index-1],ar)
        # change_priority at m[index+1]
        if m_index <len(M)-2:
            if v[m_index+1]-v[m_index+2]>0:
                n3 = x[m_index+2] + v[m_index+2]*(t_coll-new_time[m_index+2])
                n_u = abs((n3-x[m_index+1])/(v[m_index+1]-v[m_index+2])) + t_coll
            else:
                n_u = float('inf')
            q = my_queue._data[ar[m_index+1]]._rel_time
            my_queue.change_time(m_index+1,n_u,ar)
            if n_u>q:
                my_queue._downheap(ar[m_index+1],ar)
            else:
                my_queue._upheap(ar[m_index+1],ar)
        my_queue.change_time(m_index,float('inf'),ar)
        my_queue._downheap(0,ar)
        count = count +1
    return final
