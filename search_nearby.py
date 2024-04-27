class Node:
    def __init__(self,data):
        self._data= data
        self._left = None
        self._right = None
        self._y_subtree = None 

    def is_Leaf(self):
        if self._left==None and self._right==None:
            return True
        return False

class PointDatabase():
    def y_order(self,pointlist):
        if len(pointlist)==0:
            return None
        elif len(pointlist)==1:
            return Node(pointlist[0])
        elif len(pointlist)==2:
            p = Node(pointlist[(len(pointlist)//2)-1])
            p._left = Node(pointlist[(len(pointlist)//2)-1])
            p._right = Node(pointlist[(len(pointlist)//2)])
            return p
        else:
            p = Node(pointlist[(len(pointlist)//2)-1])
            p._left = self.y_order(pointlist[:len(pointlist)//2])
            p._right = self.y_order(pointlist[len(pointlist)//2:])
            return p

    def x_order(self,pointlist,y_list):
        # pointlist.sort()
        # pointlist_copy = pointlist[:]
        # pointlist_copy.sort(key=lambda x:x[1])
        if len(pointlist)==0:
            return None
        elif len(pointlist)==1:
            m = Node(pointlist[0])
            m._y_subtree=m
            return m
        elif len(pointlist)==2:
            m = Node(pointlist[0])
            m._left = Node(pointlist[0])
            m._right = Node(pointlist[1])
            n = self.y_order(y_list)
            m._y_subtree = n
            return m
        else:
            y_list_copy = y_list[:]
            ly_list, ry_list = [], []
            for i in y_list_copy:
                if i[0]<=pointlist[(len(pointlist)//2)-1][0]:
                    ly_list.append(i)
                else:
                    ry_list.append(i)
            m = Node(pointlist[(len(pointlist)//2)-1])
            m._left = self.x_order(pointlist[:len(pointlist)//2],ly_list)
            m._right = self.x_order(pointlist[len(pointlist)//2:],ry_list)
            n = self.y_order(y_list)
            m._y_subtree = n 
            return m

    def __init__(self,pointlist):
        pointlist.sort()
        self.rep = self.x_order(pointlist,sorted(pointlist, key=lambda x:x[1]))

    def searchNearby(self,q,d):

        def get_all_leaves(root,l,q,d):
            if root is not None:
                if root.is_Leaf():
                    if q[0]-d<=root._data[0]<=q[0]+d and q[1]-d<=root._data[1]<=q[1]+d:
                        l.append(root._data)
                if root._left is not None:
                    get_all_leaves(root._left,l,q,d)
                if root._right is not None:
                    get_all_leaves(root._right,l,q,d)
            return l

        def junction(root,m1,m2,i):
            if root == None:
                return None
            elif (root._data[i]>m1._data[i] and root._data[i]>m2._data[i]):
                return junction(root._left,m1,m2,i)
            elif (root._data[i]<m1._data[i] and root._data[i]<m2._data[i]):
                return junction(root._right,m1,m2,i)
            return root

        def bounds(root,u,l,i):
        
            def upper_bound(root,u,i):
                if root == None:
                    return None
                elif root.is_Leaf():
                    return root
                elif root._data[i]>=u:
                    return upper_bound(root._left,u,i)
                elif root._data[i]<u:
                    if root._right.is_Leaf() and root._right._data[i]>u:
                            return upper_bound(root._left,u,i)
                    else:
                        return upper_bound(root._right,u,i)

            def lower_bound(root,l,i):
                if root == None:
                    return None
                elif root.is_Leaf():
                    return root
                elif root._data[i]>l:
                    if root._left.is_Leaf() and root._left._data[i]<l:
                            return lower_bound(root._right,l,i)
                    else:
                        return lower_bound(root._left,l,i)
                elif root._data[i]<=l:
                    return lower_bound(root._right,l,i)
        
            return upper_bound(root,u,i), lower_bound(root,l,i)

        def is_in_range(q,d,val):
            if q[0]-d<=val[0]<=q[0]+d and q[1]-d<=val[1]<=q[1]+d:
            # if max(abs(q[0]-val[0]),abs(q[1]-val[1]))<=d:
                return True
            return False

        def range_search_y(root,m,q,d,result,j):
            if m.is_Leaf():
                if is_in_range(q,d,m._data):
                    result.append(m._data)
            else:
                if j==0:
                    n = m._left
                else:
                    n = m._right
                if n!=None:
                    while  n.is_Leaf()==False:
                        if j==0:
                            if q[1]-d<n._data[1]:
                                result = get_all_leaves(n._right,result,q,d)
                                n = n._left
                            else:
                                n = n._right
                        elif j==1:
                            if q[1]+d>=n._data[1]:
                                result = get_all_leaves(n._left,result,q,d)
                                n = n._right
                            else:
                                n = n._left
                    if is_in_range(q,d,n._data):
                        result.append(n._data)
            return result

        def range_search_x(root,m,q,d,result,j):
            if m.is_Leaf():
                if is_in_range(q,d,m._data):
                    result.append(m._data)
            else:
                if j==0:
                    n = m._left
                else:
                    n = m._right
                if n!=None:
                    while n.is_Leaf()==False:
                        if j==0:
                            if q[0]-d<=n._data[0]:
                                if n._right.is_Leaf():
                                    if is_in_range(q,d,n._right._data):
                                        result.append(n._right._data)
                                result = linear_search(n._right._y_subtree,q,d,result)
                                n = n._left
                            else:
                                n = n._right
                        if j==1:
                            if q[0]+d>=n._data[0]:
                                if n._left.is_Leaf():
                                    if is_in_range(q,d,n._left._data):
                                        result.append(n._left._data)
                                result = linear_search(n._left._y_subtree,q,d,result)
                                n = n._right
                            else:
                                n = n._left
                    if is_in_range(q,d,n._data):
                        result.append(n._data)
            return result

        def linear_search(root,q,d,result):
            r1,r2 = bounds(root,q[1]+d,q[1]-d,1)
            m = junction(root,r1,r2,1)
            if m!=None:
                result = range_search_y(root,m,q,d,result,0)
                result = range_search_y(root,m,q,d,result,1)
            return result

        def binary_search(root,q,d,result):
            r1,r2 = bounds(root,q[0]+d,q[0]-d,0)
            m = junction(root,r1,r2,0)
            if m!=None:
                result = range_search_x(root,m,q,d,result,0)
                result = range_search_x(root,m,q,d,result,1)
            return result     

        p = list(set(binary_search(self.rep,q,d,[])))
        return p
    def height(self,node):
        if node is None:
            return 0
        else:
        
            lheight = self.height(node._left)
            rheight = self.height(node._right)

            if lheight > rheight:
                return lheight+1
            else:
                return rheight+1
    def printCurrentLevel(self,root, level):
        if root is None:
            return
        if level == 1:
            print(root._data, end="")
        elif level > 1:
            self.printCurrentLevel(root._left, level-1)
            self.printCurrentLevel(root._right, level-1)
    def printLevelOrder(self,root):
        h = self.height(root)
        for i in range(1, h+1):
            self.printCurrentLevel(root, i)

# --------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------

# pointDbObject = PointDatabase([(1,6), (2,4), (3,7), (4,9), (5,1), (6,3), (7,8), (8,10),(9,2), (10,5)])
# pointDbObject=PointDatabase([(21, 24), (9, 8), (13, 38), (17, 45), (35, 23), (5, 47), (46, 5), (38, 2), (4, 20), (22, 50), (40, 28), (43, 26), (31, 22), (8, 35), (27, 25)])
# print(pointDbObject.printLevelOrder(pointDbObject.rep._right._y_subtree))
# pointDbObject=PointDataBase([(38, 26), (43, 24), (5, 25), (30, 2), (29, 7), (37, 16), (51, 15), (40, 23), (23, 20), (8, 49), (34, 45), (42, 12), (32, 39), (17, 19), (12, 4)])
# print(pointDbObject.lower_bound(pointDbObject.rep,8.4,0)._data)
# print(pointDbObject.searchNearby((4,8),2))
# print(pointDbObject.rep._data)
# pointDbObject = PointDatabase([(1,6), (2,4), (3,7), (4,9), (5,1), (6,3), (7,8), (8,10),(9,2), (10,5),(0,13),(11,20),(12,-3),(17,-1)])
# pointDbObject = PointDatabase([])
# print(pointDbObject.searchNearby((7,8), 5))
# pointDbObject= PointDatabase([(-55530, -35688), (-55470, -35677), (-55427, -35766), (-55418, -35393), (-55218, -35977)])
# print(pointDbObject.searchNearby((-55470,-35677),300))
# print(pointDbObject.searchNearby((-55470,-35677),300))










        