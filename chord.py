from node import *
import random
import matplotlib.pyplot as plt

class Chord:

    def __init__(self):
        self.network = []
    
    def addNode(self, nodeId):
        n = Node(nodeId)
        if(len(self.network) == 0):
            n.join(None)
        else:
            n.join( self.network[random.randrange(len(self.network))] )
            s = n.successor()
            p = n.predecessor
            for key in s.keys:
                # if contains_left_open(key, p.id, n.id):
                if inOut(key, p.id, n.id, 1):
                    n.keys.append(key)
            newKey = []
            for key in s.keys:
                if not inOut(key, p.id, n.id, 1):
                    newKey.append(key)
            s.keys = newKey
        self.network.append(n)

    
    def deleteNode(self, id):
        if len(self.network) == 0:
            print("No node in the network")
        # flag = False
        for node in self.network:
            if id == node.id:
                # print("delete ", node.id)
                node.deleteOthers()
                node.moveKeys()
                self.network.remove(node)
                del node
                return
        print("Node doesn't exist")

    def lookUp(self, keyVal):
        index = random.randrange(len(self.network))
        # index = 2
        print("Lookup starts ", self.network[index].getId())
        return self.network[index].findSuccessor(keyVal, 1).id

    def insert(self, keyVal):
        # print("adding ", keyVal)
        index = random.randrange(len(self.network))
        # print("index ", index)
        node = self.network[index].findSuccessor(keyVal, 0)
        # print(node.id)
        node.insertKey(keyVal)

    def printNetwork(self):
        for i in self.network:
            i.printNode()
            i.printKeys()

c = Chord()
n = 100
nodesAdded = []
for i in range(1,n):
    nodeId = "Node " + str(i)
    c.addNode(compute_hash(nodeId))
    nodesAdded.append(compute_hash(nodeId))

keysInserted = []
for i in range(100):
    keyId = "Key " + str(i)
    temp = compute_hash(keyId)
    keysInserted.append(temp)
    c.insert(temp)

for i in range(100):
    c.lookUp(random.randrange(0, 100))

plt.bar(hopsGraph.keys(), hopsGraph.values(), 1.0, color='r')

plt.xlabel("Hop count")
plt.ylabel("Seach queries")
plt.title("Hops distribution")
plt.savefig("Chord" + str(n) + "_p.eps", format = "eps")

# hopsGraph = {}

# for i in range(n/2):
#     c.deleteNode(random.randrange(0, n))

# for i in range(1000000):
#     c.lookUp(random.randrange(0, 10000))

# plt.bar(hopsGraph.keys(), hopsGraph.values(), 1.0, color='r')

# plt.xlabel("Hop count")
# plt.ylabel("Seach queries")
# plt.title("Hops distribution after deletion")
# plt.savefig("Chord" + str(n) +  "_del.eps", format = "eps")
