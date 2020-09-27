import math
from controller import PIDcontroller
frictionDivisor = 1.1
turnController = PIDcontroller(1,0,0)
class robot:

    def __init__(self, windowSizeX, windowSizeY, robotX=100, robotY=100, robotOrientation=90, scalar=0.1):
        self.windowSizeX = windowSizeX
        self.windowSizeY = windowSizeY
        self.robotX = robotX
        self.robotY = robotY
        self.robotOrientation = robotOrientation
        self.scalar = scalar
        self.robotRadius = ((self.windowSizeX + self.windowSizeY) / 2) * self.scalar
        self.angleKp = 0.1
        self.angleKd = 0
        self.angleKi = 0
        self.lastSpeedX = 0
        self.lastSpeedY = 0
    def drawRobotSimpleGUI(self, canvas):
        canvas.draw_circle((self.robotX, self.robotY), self.robotRadius, 12, 'Green', 'Green')
        canvas.draw_circle((self.robotX + (self.robotRadius * math.cos(self.robotOrientation)),
                            self.robotY + (self.robotRadius * math.sin(self.robotOrientation))),
                           self.robotRadius / 5, 12, 'Blue')

    def interpolatePoisitionByFrame(self, x, y, robotSpeedX=0, robotSpeedY=0, angleSpeed=1, telemetry = False):
        # turn robot
        target_angle = math.atan2(y - self.robotY, x - self.robotX)
        orientation = self.robotOrientation

        turn_response = turnController.update(orientation,target_angle)
        while math.degrees(self.robotOrientation) <= -180:
            self.robotOrientation += math.pi
        while math.degrees(self.robotOrientation) >= 180:
            self.robotOrientation -= math.pi
        self.robotOrientation += turn_response
        robotSpeedX += self.lastSpeedX / frictionDivisor
        robotSpeedY += self.lastSpeedY / frictionDivisor
        # drive forward based on the current heading of the robot as this is a differential drive roomba
        self.robotX += robotSpeedX
        self.robotY += robotSpeedY

        self.lastSpeedX = robotSpeedX
        self.lastSpeedY = robotSpeedY

        if telemetry:
            print(f"output: {turn_response} theta: {math.degrees(self.robotOrientation)} target: {math.degrees(target_angle)}")