"""
deze module neemt de functie die momenteel uitgevoerd wordt, en splitst deze
op in kleinere functies om zo te kunnen zorgen dat ze ter plekke afgebroken
kunnen worden
"""

import functionCaller, time
from platform import system
import math

car = None  # this is going to be the module Team_auto.car or a mockup for it.

functionDivider = None

class Function:
    """
    the functions that are stored in the queue
    """

    def __init__(self, function, **kwargs):
        self.function = function
        self.time = kwargs.get('duration', None)
        kwargs.pop('duration', None)
        self.params = kwargs

    def getFunction(self):
        return self.function

    def getTime(self):
        return self.time

    def useTime(self, dt):
        if self.time is None:
            self.function(**self.params)
            return True, 0
        else:
            self.function(duration= min(dt, self.time), **self.params)
            self.time, dt = self.time - dt, dt - self.time   # dit moet uitgebreider, bvb nooit onder 0
            return self.time <= 0, max(0, dt)

    def getParams(self):
        return self.params

    def copy(self):
        return Function(self.function, duration=self.time, **self.params)

    def __str__(self):
        stri = ""
        stri += str(self.function) + ', '
        if self.time is not None:
            stri += "duration: " + str(self.time) + ", "
        stri += str(self.params)
        return stri

    def __repr__(self):
        return str(self)

def haha(power=1):
    print "power: ", power


class FunctionDivider:
    """
    transforms commands into functions that the Car can execute. Also allows interuption of these commands.
    """
#    commandLib = {"goForward": [Function(haha, 100)], "goBackward": [Function(haha, 100)]} #the list contains the functions that should be executed in order to drive the car

    def __init__(self, firstCommand=None):
        self.currentCommand = None
        self.currentFunction = None
        functions = car.get_functions()
        self.commandLib = {"goForward": [Function(functions.get('go_straight_pid'), duration=10, power=250)],
                           "goBackward": [Function(functions.get('go_straight_pid'), duration=10, power=-250)],
                           "goLeft": [Function(functions.get('turn_straight_left'), duration=10, power=250)],
                           "goRight": [Function(functions.get('turn_straight_right'), duration=10, power=250)],
                           #			"goForwardLeft"
                           #			"goForwardRigth"
                           #			"goBackwardLeft"
                           #			"goBackwardRight"
                           "makeLine": [Function(functions.get('go_straight_distance'), distance=200, power=200)],
                           "makeSquare": [Function(functions.get('go_straight_distance'), distance=100, power=150),
                                          Function(functions.get('rotate_angle_left'), angle=math.pi, power=150),
                                          Function(functions.get('go_straight_distance'), distance=100, power=150),
                                          Function(functions.get('rotate_angle_left'), angle=math.pi, power=150),
                                          Function(functions.get('go_straight_distance'), distance=100, power=150),
                                          Function(functions.get('rotate_angle_left'), angle=math.pi, power=150),
                                          Function(functions.get('go_straight_distance'), distance=100, power=150),
                                          Function(functions.get('rotate_angle_left'), angle=math.pi, power=150)],
                           "makeCircle": [Function(functions.get('make_circle_left'), radius=50, power=200)]}
        self.currentCommandObject = None
        if firstCommand is not None:
            self.executeCommand(firstCommand)

    def executeCommand(self, command):#TODO: take params into account
        if command is not None and command.getCommandName() in self.commandLib.keys():
            self.currentCommand = [x.copy() for x in self.commandLib[command.getCommandName()]]
            self.currentCommandObject = command
        else:
            self.currentCommand = None

    def interuptCurrentCommand(self):
        """
        stops executing current command
        :return: the command with extra params to see how far it is already executed
        """
        pass

    def processTime(self,dt):
        """
        executes the current command for dt seconds
        :param dt: int telling how many ms the current command should run
        :return: None
        """
        #  print "processing time"
        while dt >0:
            #print "time: ", dt, self.currentCommand
            if self.currentCommand is not None:
                dt = self.processCommand(dt)
            else:
                self.executeCommand(functionCaller.getIOStream().pushCommand())
                #  print self.currentCommand, "current command"
                if self.currentCommand == None: #geen commands in queue
                    time.sleep(1)
                    dt -= 1

    def processCommand(self, dt): #TODO: fix dubbele true prints
        #  print "processing command"
        while dt > 0:
            #  print "command time left: ", dt
            if self.currentFunction is not None:
                done, dt = self.procesFunction(dt)
                if done or dt > 0:
                    self.currentFunction = None
            elif len(self.currentCommand) > 0:
                self.currentFunction = self.currentCommand.pop(0)
            else:
                self.currentCommand = None
                return dt
        return 0

    def procesFunction(self, dt):
        print "executing now: " + str(self.currentFunction)
        return self.currentFunction.useTime(dt)


def getFunctionDivider():
    return functionDivider

if system() == 'Linux': #import Team_auto.car as car
    print "using real car"
    car = __import__("Team_auto.Car").Car
else:
    print "using carMock"
    car = __import__("webserver.CarMock").CarMock
functionDivider = FunctionDivider()
