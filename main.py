import simpleguitk as simplegui
import math
from robot import robot
from pathRender import pathRenderer
from controller import PIDcontroller
import time
frameX, frameY = 1000, 1000

mecanumRobot = robot(frameX, frameY, 100, 100, math.radians(180), 0.05)

path = [(100, 100), (500, 100), (500, 500), (100, 500), (350, 0), (100, 100)]
pathRender = pathRenderer(path)
currentPointInPath = 0
advancePointDistance = 10
kp = 0.007
ki = 0
kd = 0.009
driveControllerX = PIDcontroller(kp, ki, kd)
driveControllerY = PIDcontroller(kp, ki, kd)
atPoint = False
atPointForRequiredDuration = False
timeAtPoint = 0
timeAtPointArrival = 0
def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def followPath(canvas):
    global atPoint
    global atPointForRequiredDuration
    global timeAtPointArrival
    global currentPointInPath
    global timeAtPoint
    distance = calculateDistance(mecanumRobot.robotX, mecanumRobot.robotY,
                                 path[currentPointInPath][0], path[currentPointInPath][1])
    xDist = mecanumRobot.robotX - path[currentPointInPath][0]
    yDist = mecanumRobot.robotY - path[currentPointInPath][1]

    robotSpeedX = driveControllerX.update(xDist,0)
    robotSpeedY = driveControllerY.update(yDist,0)
    mecanumRobot.drawRobotSimpleGUI(canvas)
    if currentPointInPath != len(path):
        mecanumRobot.interpolatePoisitionByFrame(path[currentPointInPath][0], path[currentPointInPath][1],
                                                 robotSpeedX=robotSpeedX, robotSpeedY = robotSpeedY, telemetry=True)
    if distance <= advancePointDistance and currentPointInPath < len(path) - 1:
        if not atPoint:
            timeAtPointArrival = time.time()
        atPoint = True
        timeAtPoint = (time.time()) - timeAtPointArrival
        print(timeAtPoint)
        if timeAtPoint > 1:
            atPointForRequiredDuration = True
        if atPointForRequiredDuration and atPoint:
            atPoint = False
            atPointForRequiredDuration = False
            timeAtPoint = 0
            currentPointInPath += 1
    if currentPointInPath == len(path) - 1:
        currentPointInPath = 0


def draw(canvas):
    followPath(canvas)
    pathRender.renderPath(canvas)


if __name__ == "__main__":
    frame = simplegui.create_frame("simulator", frameX, frameY)
    frame.set_draw_handler(draw)

    frame.start()
