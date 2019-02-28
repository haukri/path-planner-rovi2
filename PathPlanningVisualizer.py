import pyglet
from pyglet import clock
from PathPlannerRRT import PathPlannerRRT
from PathPlannerRRTConnect import PathPlannerRRTConnect

width, height = 600, 600
window = pyglet.window.Window(width=width, height=height)
obstacles = [[100, 0, 200, 200], [300, 200, 400, 600], [300, 0, 400, 150]]


@window.event
def on_draw():
    window.clear()
    drawRectangle(0, 0, width, height, [255, 255, 255])
    for obstacle in obstacles:
        drawRectangle(obstacle[0], obstacle[1], obstacle[2]-obstacle[0], obstacle[3]-obstacle[1], [0, 0, 0])
    for edge in PathPlanner.getEdges():
        drawLine(edge[0], edge[1], [0, 0, 255])
    path = PathPlanner.getPath()
    for i in range(len(path)-1):
        drawLine(path[i], path[i+1], [255, 0, 0])
    drawRectangle(PathPlanner.qinit[0]-5, PathPlanner.qinit[1]-5, 10, 10, [0, 255, 0])
    drawRectangle(PathPlanner.qgoal[0]-5, PathPlanner.qgoal[1]-5, 10, 10, [255, 0, 0])


@window.event
def on_key_press(symbol, modifiers):
    if symbol == 32:
        pathPlanningStep(1)


def initialize():
    global window
    pyglet.gl.glLineWidth(2)
    pyglet.app.run()


def drawRectangle(x, y, dx, dy, color):
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [x, y, x, y + dy, x + dx, y + dy, x + dx, y]), ('c3B', tuple(color*4)))


def drawLine(q1, q2, color):
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2f", (q1[0], q1[1], q2[0], q2[1])), ('c3B', tuple(color*2)))


def pathPlanningStep(dt):
    if PathPlanner.nextStep():
        clock.schedule_once(pathPlanningStep, 0.01)


def inCollision(q):
    for obstacle in obstacles:
        if q[0] >= obstacle[0] and q[0] <= obstacle[2]:
            if q[1] >= obstacle[1] and q[1] <= obstacle[3]:
                return True
    return False


PathPlanner = PathPlannerRRTConnect(height, width, inCollision, (50, 90), (500, 500), 20)
initialize()
