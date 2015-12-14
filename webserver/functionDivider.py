"""
deze module neemt de functie die momenteel uitgevoerd wordt, en splitst deze
op in kleinere functies om zo te kunnen zorgen dat ze ter plekke afgebroken
kunnen worden
"""

import functionCaller
import time
from platform import system

car = None  # this is going to be the module Team_auto.car or a mockup for it.


# functionDivider = None


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
            self.function(duration=min(dt, self.time), **self.params)
            self.time, dt = self.time - dt, dt - self.time  # dit moet uitgebreider, bvb nooit onder 0
            return self.time <= 0, max(0, dt)

    def getParams(self):
        return self.params

    def set_params(self, **kwargs):
        #print 'params worden gezet op: '+ str(kwargs)
        for key, value in kwargs.iteritems():
            self.params[key] = value

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


class FunctionDivider:
    """
    transforms commands into functions that the Car can execute. Also allows interuption of these commands.
    """
    #    commandLib = {"goForward": [Function(haha, 100)], "goBackward": [Function(haha, 100)]} #the list contains the functions that should be executed in order to drive the car

    def __init__(self, firstCommand=None):
        self.currentCommand = None
        self.currentFunction = None
        functions = car.get_functions()
        self.functions = functions
        self.commandLib = {"goForward": [Function(functions.get('go_straight_manual'), duration=0.1, power=250)],
                           "goBackward": [Function(functions.get('go_straight_manual'), duration=0.1, power=-250)],
                           "goLeft": [Function(functions.get('rotate_left_duration'), duration=0.1, power=100)],
                           "goRight": [Function(functions.get('rotate_right_duration'), duration=0.1, power=100)],
                           "goForwardLeft": [
                               Function(functions.get('make_circle_left'), radius=50, power=150, degree=5)],
                           "goForwardRigth": [
                               Function(functions.get('make_circle_right'), radius=50, power=150, degree=5)],
                           "goBackwardLeft": [
                               Function(functions.get('make_circle_left'), radius=50, power=150, degree=-5)],
                           "goBackwardRight": [
                               Function(functions.get('make_circle_right'), radius=50, power=150, degree=-5)],
                           "pass": [Function(functions.get('sleep'), duration=0.1)],
                           "makeLine": [Function(functions.get('go_straight_distance'), distance=200, power=100)],
                           "makeSquare": [Function(functions.get('go_straight_distance'), distance=100, power=100),
                                          Function(functions.get('sleep'), duration=1),
                                          Function(functions.get('rotate_left_angle'), angle=90, power=100),
                                          Function(functions.get('sleep'), duration=1),
                                          Function(functions.get('go_straight_distance'), distance=100, power=100),
                                          Function(functions.get('sleep'), duration=1),
                                          Function(functions.get('rotate_left_angle'), angle=90, power=100),
                                          Function(functions.get('sleep'), duration=1),
                                          Function(functions.get('go_straight_distance'), distance=100, power=100),
                                          Function(functions.get('sleep'), duration=1),
                                          Function(functions.get('rotate_left_angle'), angle=90, power=100),
                                          Function(functions.get('sleep'), duration=1),
                                          Function(functions.get('go_straight_distance'), distance=100, power=100),
                                          Function(functions.get('sleep'), duration=1),
                                          Function(functions.get('rotate_left_angle'), angle=90, power=100)],
                           "makeCircle": [
                               Function(functions.get('make_circle_left'), radius=50, power=150, degree=310)],
                           "stop": [Function(functions.get("set_powers"), left=100, right=100, duration=0.1),
                                    Function(functions.get("sleep"), duration=100000)],
                           "left": [Function(functions.get("set_powers"), left=100, right=100, duration=0.1),
                                    Function(functions.get("rotate_left_angle"), angle=90, power=100)],
                           "right": [Function(functions.get("set_powers"), left=100, right=100, duration=0.1),
                                     Function(functions.get("rotate_right_angle"), angle=90, power=100)]}

        self.currentCommandObject = None
        if firstCommand is not None:
            self.executeCommand(firstCommand)

    def executeCommand(self, command):
        if command is not None and command.getCommandName() in self.commandLib.keys():
            self.currentCommandObject = command
            if not command.is_paused():
                self.currentCommand = [x.copy() for x in self.commandLib[command.getCommandName()]]
            else:
                self.currentCommand = command.get_functions()
        else:
            self.currentCommand = None
        if functionCaller.hostfile.beschrijving is not None:
            functionCaller.hostfile.beschrijving.update_route_description()

    def interuptCurrentCommand(self):
        """
        stops executing current command
        :return: the command with extra params to see how far it is already executed, it does finish the small functions
        """
        paused_command = self.currentCommandObject.pause_with_updated_params(self.currentCommand)
        self.currentCommand = []
        self.currentCommandObject = None
        return paused_command

    def interuptCurrentFunction(self):
        del self.currentCommand[0]

    def processTime(self, dt):
        """
        executes the current command for dt seconds
        :param dt: int telling how many ms the current command should run
        :return: None
        """
        #  print "processing time"
        while dt > 0:
            # print "isUpdated: ", car.isUpdated
            if self.currentCommand is not None:
                dt = self.processCommand(dt)
            else:
                self.executeCommand(functionCaller.getIOStream().pushCommand())
                #  print self.currentCommand, "current command"
                if self.currentCommand is None:  # geen commands in queue
                    time.sleep(0.1)
                    dt -= 0.1

    def processCommand(self, dt):
        #  print "processing command"
        while dt > 0:
            #  print "command time left: ", dt
            if self.currentFunction is not None:
                done, dt = self.procesFunction(dt)
                if done or dt > 0:
                    self.currentFunction = None
            elif len(self.currentCommand) > 0:
                self.currentFunction = self.currentCommand.pop(0)
                if self.currentFunction.getFunction() == self.functions.get("set_powers"):
                    self.currentCommand.insert(0, self.currentFunction.copy())
                params = {}
                for key, value in self.currentFunction.getParams().iteritems():
                    params[key]=self.currentCommandObject.getParam(key, value)
                self.currentFunction.set_params(**params)
            else:
                car.last_left_power = 0
                car.last_right_power = 0
                car.isUpdated = True
                self.currentCommand = None
                self.currentCommandObject = None
                return dt
        return 0

    def procesFunction(self, dt):
        print "executing now: " + str(self.currentFunction)
        return self.currentFunction.useTime(dt)


def getFunctionDivider():
    return functionDivider


if system() == 'Linux':  # import Team_auto.car as car
    print "using real car"
    car = __import__("Team_auto.Car").Car
else:
    print "using carMock"
    car = __import__("webserver.CarMock").CarMock
functionDivider = FunctionDivider()
