import math
import random


class PathPlannerRRTConnect:

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
        self.graphNodesA = []
        self.graphEdgesA = []
        self.graphNodesB = []
        self.graphEdgesB = []
        self.graphNodesA.append(qinit)
        self.graphNodesB.append(qgoal)
        self.qnew = (0, 0)
        self.path = []
        random.seed(0)

    def getEdges(self):
        return self.graphEdgesA + self.graphEdgesB

    def getPath(self):
        if len(self.path) > 0:
            print(self.path)
        return self.path

    def add_node(self, q, graph):
        graph.append(q)

    def add_edge(self, q1, q2, graph):
        graph.append((q1, q2))

    def nearestNeighbor(self, q, graph):
        qnear = graph[0]
        qdistance = self.distance(q, qnear)
        for node in graph:
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
            self.qnew = q
            if d > self.epsilon:
                c = self.epsilon / d
                dx *= c
                dy *= c
                self.qnew = (qnear[0]+dx, qnear[1]+dy)
            if not self.inCollisionInterpolated(self.qnew, qnear, self.epsilon/10.0):
                return self.qnew
        return False

    def extend(self, qrand, graphNodes, graphEdges):
        qnear = self.nearestNeighbor(qrand, graphNodes)
        self.qnew = self.newConfig(qrand, qnear)
        if self.qnew:
            self.add_node(self.qnew, graphNodes)
            self.add_edge(qnear, self.qnew, graphEdges)
            if self.distance(self.qnew, qrand) < self.epsilon:
                return self.REACHED
            return self.ADVANCED
        return self.TRAPPED

    def connect(self, q):
        S = self.extend(q, self.graphNodesB, self.graphEdgesB)
        while S == self.ADVANCED:
            S = self.extend(q, self.graphNodesB, self.graphEdgesB)
        return S

    def inCollisionInterpolated(self, q1, q2, epsilon):
        dq = (q2[0]-q1[0], q2[1]-q1[1])
        n = max(math.ceil(self.distance(q1, q2)/epsilon)-1, 0)
        step = (dq[0]/(n+1), dq[1]/(n+1))
        for i in range(1, n):
            qi = (i*step[0]+q1[0], i*step[1]+q1[1])
            if self.inCollision(qi):
                return True
        return False

    def linearPath(self, q1, q2, epsilon):
        dq = (q2[0]-q1[0], q2[1]-q1[1])
        n = max(math.ceil(self.distance(q1, q2)/epsilon)-1, 0)
        step = (dq[0]/(n+1), dq[1]/(n+1))
        path = []
        path.append(q1)
        for i in range(1, n+1):
            qi = (i*step[0]+q1[0], i*step[1]+q1[1])
            path.append(qi)
        path.append(q2)
        return path

    def findPath(self):
        self.path = [self.graphNodesA[-1]]
        for edge in reversed(self.graphEdgesA):
            child = edge[1]
            parent = edge[0]
            if child == self.path[-1]:
                self.path.append(parent)
        self.path = list(reversed(self.path))
        self.path.append(self.graphNodesB[-1])
        for edge in reversed(self.graphEdgesB):
            child = edge[1]
            parent = edge[0]
            if child == self.path[-1]:
                self.path.append(parent)

    def prunePath(self, path):
        i = 0
        while i < len(path)-2:
            if not self.inCollisionInterpolated(path[i], path[i+2], self.epsilon/10.0):
                del path[i+1]
                if i > 0:
                    i -= 1
            else:
                i += 1
        return path

    def pathShortcut(self, path, iterations):
        for i in range(iterations):
            a = 1
            b = 0
            while a >= b:
                a = random.randint(0, len(path)-1)
                b = random.randint(0, len(path)-1)
            if not self.inCollisionInterpolated(path[a], path[b], self.epsilon/10.0):
                newPath = []
                if a > 0:
                    newPath += path[0:a]
                newPath += self.linearPath(path[a], path[b], self.epsilon)
                if b < len(path) - 1:
                    newPath += path[b+1:]
                path = newPath
        return path

    def nextStep(self):
        qrand = self.generateRandomNode()
        if self.extend(qrand, self.graphNodesA, self.graphEdgesA) != self.TRAPPED:
            oldqnew = self.qnew
            if self.connect(self.qnew) == self.REACHED:
                self.findPath()
                self.path = self.prunePath(self.path)
                # self.path = self.pathShortcut(self.path, 10000)
                self.add_edge(oldqnew, self.qnew, self.graphEdgesA)
                return False
        self.swap()
        return True

    def swap(self):
        self.graphNodesA, self.graphNodesB = self.graphNodesB, self.graphNodesA
        self.graphEdgesA, self.graphEdgesB = self.graphEdgesB, self.graphEdgesA
