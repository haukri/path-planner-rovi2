import math
import random


class PathPlannerRRT:

    edges = []
    nodes = []

    ADVANCED = 1
    TRAPPED = 2
    REACHED = 3

    def __init__(self, height, width, inCollision, qinit, qgoal, epsilon):
        self.height = height
        self.width = width
        self.inCollision = inCollision
        self.qinit = qinit
        self.qgoal = qgoal
        self.epsilon = epsilon
        self.nodes.append(qinit)

    def getEdges(self):
        return self.edges

    def getPath(self):
        return []

    def add_node(self, q):
        self.nodes.append(q)

    def add_edge(self, q1, q2):
        self.edges.append((q1, q2))

    def nearestNeighbor(self, q):
        qnear = self.nodes[0]
        qdistance = self.distance(q, qnear)
        for node in self.nodes:
            if self.distance(q, node) < qdistance:
                qnear = node
                qdistance = self.distance(q, node)
        return qnear

    def distance(self, q1, q2):
        dx = q2[0] - q1[0]
        dy = q2[1] - q1[1]
        return math.sqrt(dx**2 + dy**2)

    def generateRandomNode(self):
        return (random.uniform(0, self.width), random.uniform(0, self.height))

    def newConfig(self, q, qnear):
        dx = q[0] - qnear[0]
        dy = q[1] - qnear[1]
        d = math.sqrt(dx**2+dy**2)
        if d > 0:
            qnew = q
            if d > self.epsilon:
                c = self.epsilon / d
                dx *= c
                dy *= c
                qnew = (qnear[0]+dx, qnear[1]+dy)
            if not self.inCollision(qnew):
                return qnew
        return False

    def extend(self, qrand):
        qnear = self.nearestNeighbor(qrand)
        qnew = self.newConfig(qrand, qnear)
        if qnew:
            self.add_node(qnew)
            self.add_edge(qnear, qnew)
            if self.distance(qnew, self.qgoal) < self.epsilon:
                self.add_edge(qnew, self.qgoal)
                return self.REACHED
            return self.ADVANCED
        return self.TRAPPED

    def nextStep(self):
        qrand = self.generateRandomNode()
        if self.extend(qrand) == self.REACHED:
            return False
        return True
