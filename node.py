import hashlib
import random
m = 160
hopsGraph = {}

def in1(id, start, end):
    if((id == start) or (id == end) or (start == end)):
        return True
    if(start > end):
        return not in1(id, end, start)

    if(id > start and id < end):
        return True
    return False

def inOut(id, start, end, type):
    nequ = (id == end)
    neql = (id == start)
    inRange = in1(id, start, end)

    if type == 0:
        return (not nequ) and (not neql) and inRange
    elif type == 1:
         return (not neql) and inRange
    elif type == 2:
        return (not nequ) and inRange
    else:
        return inRange

# def contains(node_id_int, start_int , end_int):
#     if(start_int == end_int or start_int == node_id_int or end_int == node_id_int):
#         return True
#     if(start_int > end_int):
#         return (not contains(node_id_int, end_int, start_int)  )
#     else:
#         if(node_id_int > start_int and node_id_int < end_int):
#             return True
#         return False


# def contains_both_open(node_id, start_id, end_id):
#     if(contains(node_id, start_id, end_id) and node_id != start_id and node_id != end_id):
#         return True
#     else:
#         return False


# def contains_right_open(node_id, start_id, end_id):
#     if(contains(node_id, start_id, end_id) and node_id != end_id):
#         return True
#     else:
#         return False

# def contains_left_open(node_id, start_id, end_id):
#     if(contains(node_id, start_id, end_id) and node_id != start_id ):
#         return True
#     else:
#         return False


class Node:
    m = 160
    def __init__(self, id):
        self.id = id
        # self.index = index
        self.finger = []
        self.predecessor = None
        self.keys = []
        for i in range(0, Node.m):
            temp = []
            temp.append( (id + pow(2, i)) % pow(2, m) ) 
            temp.append(None)
            self.finger.append(temp)

    def distance(self, a, b):
        if a == b:
            return pow(2, Node.m)
        return (b - a + pow(2, m)  ) % pow(2, m)

    def check(self, id1, id2, id3, flag):
        # d1 = self.distance(id2, id3)
        # d2 = self.distance(id2, id1)
        return inOut(id1, id2, id3, flag)
        # if flag == 0:
        #     return contains_left_open(id1, id2, id3)
        # elif flag == 1:
        #     return contains_both_open(id1, id2, id3)
        # elif flag == 2:
        #     return contains_right_open(id1, id2, id3)

    def getId(self):
        return self.id

    def successor(self):
        return self.finger[0][1]

    def closestPrecedingFinger(self, id):
        for i in range(Node.m - 1, -1, -1):
            if self.check(self.finger[i][1].id, self.id, id, 1):
                return self.finger[i][1]
        return self

    def findPredecessor(self, id, mode = 0):
        np = self
        path = []
        hops = 0
        while not self.check(id, np.id, np.successor().id, 0):
            np = np.closestPrecedingFinger(id)
            path.append(np.id)
            hops += 1

        if(mode == 1):
            hops += 1
            path.append(np.successor().id)
            # print("Path", path)
            # print("Number of Hops: ", hops)
            if hops in hopsGraph:
                hopsGraph[hops] += 1
            else:
                hopsGraph[hops]  = 1
        return np

    def findSuccessor(self, id, mode = 0):
        np = self.findPredecessor(id, mode)
        return np.successor()

    def initFingerTable(self, n):
        self.finger[0][1] = n.findSuccessor(self.finger[0][0])
        self.predecessor = self.finger[0][1].predecessor
        self.finger[0][1].predecessor = self
        self.predecessor.finger[0][1] = self
        for i in range(0, Node.m - 1):
            if self.check(self.finger[i+1][0] , self.id, self.finger[i][1].id, 2 ):
                self.finger[i+1][1] = self.finger[i][1]
            else:
                self.finger[i+1][1] = n.findSuccessor(self.finger[i+1][0])

    def updateFingerTable(self, n, i):
        if self.id == n.id:
            return
        if self.check(n.id, self.id, self.finger[i][1].id, 2):
            self.finger[i][1] = n
            p = self.predecessor
            p.updateFingerTable(n, i)

    def updateOthers(self):
        for i in range(0, Node.m):
            id1 = (self.id - pow(2, i)) % pow(2, Node.m)
            nodePre = self.findSuccessor(id1)
            if(nodePre.id != id1):
                nodePre = self.findPredecessor((self.id - pow(2, i)) % pow(2, Node.m) )
            if(nodePre.id == self.id):
                continue
            nodePre.updateFingerTable(self, i)

    def join(self, n):
        if(n is None):
            for i in range(0, Node.m):
                self.finger[i][1] = self
            self.predecessor = self
        else:
            self.initFingerTable(n)
            self.updateOthers()

    def printNode(self):
        print("id " + str(self.id) ) 
        print("predecessor " + str (self.predecessor.id) )
        print("table ------------------ ")
        # print(self.finger)
        for i in self.finger:
            print(str(i[0]) + "    " + str(i[1].id) )
    
    def printKeys(self):
        print("keys---------------------")
        print(self.keys)
        print("\n\n")
    
    def insertKey(self, keyVal):
        self.keys.append(keyVal)

    def onDelUpdateFingerTable(self, n , i):
        if self.id == n.id:
            return
        if(self.finger[i][1].id == n.id):
            self.finger[i][1] = n.successor()
            p = self.predecessor
            p.onDelUpdateFingerTable(n, i)

    def deleteOthers(self):
        self.successor().predecessor = self.predecessor
        for i in range(0, Node.m):
            id1 = (self.id - pow(2, i)) % pow(2, Node.m)
            nodePre = self.findSuccessor(id1)
            if(nodePre.id != id1):
                nodePre = self.findPredecessor((self.id - pow(2, i)) % pow(2, Node.m) )
            if(nodePre.id == self.id):
                continue
            nodePre.onDelUpdateFingerTable(self, i)

    def moveKeys(self):
        succ = self.successor()
        allKeys = self.keys
        succ.keys = succ.keys + allKeys


def compute_hash(node):
    result = hashlib.sha1(node.encode())
    return int(result.hexdigest(),16) % (pow(2,m))
