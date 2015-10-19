"""
deze module neemt de functie die momenteel uitgevoerd wordt, en splitst deze
op in kleinere functies om zo te kunnen zorgen dat ze ter plekke afgebroken
kunnen worden
"""

import functionCaller, time
import Team_auto.Car as car



functionDivider = None

class Function:
    """
    the functions that are stored in the queue
    """

    def __init__(self, function, duration=None, **kwargs):
        self.function = function
        self.params = kwargs
        self.time = duration

    def getFunction(self):
        return self.function

    def getTime(self):
        return self.time

    def useTime(self, dt):
        if self.time is None:
            return 0
        self.time -= dt #dit moet uitgebreider, bvb nooit onder 0
        return max(0, dt-self.time)

    def getParams(self):
        return self.params

    def copy(self):
        return Function(self.function, self.time)


def haha(power=1):
    print "power: ", power


class FunctionDivider:
    """
    transforms commands into functions that the Car can execute. Also allows interuption of these commands.
    """
#    commandLib = {"goForward": [Function(haha, 100)], "goBackward": [Function(haha, 100)]} #the list contains the functions that should be executed in order to drive the car

    def __init__(self, firstCommand = None):
        self.currentCommand = None
        self.currentFunction = None
        function_ids = car.get_function_ids()
        self.commandLib = {"goForward": [Function(function_ids['go_straight'], duration=10, power=250)],
                           "goBackward": [Function(function_ids['go_straight'], duration=10, power=-250)]}
        self.currentCommandObject = None
        if firstCommand is not None:
            self.executeCommand(firstCommand)

    def executeCommand(self, command):
        if command is not None and command.getCommandName() in FunctionDivider.commandLib.keys():
            self.currentCommand = [x.copy() for x in FunctionDivider.commandLib[command.getCommandName()]]
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
        print "processing time"
        while dt >0:
            print "time: ", dt, self.currentCommand
            if self.currentCommand is not None:
                dt = self.processCommand(dt)
            else:
                self.executeCommand(functionCaller.getIOStream().pushCommand())
                print self.currentCommand, "current command"
                if self.currentCommand == None: #geen commands in queue
                    time.sleep(1)
                    dt -= 1

    def processCommand(self, dt):
        print "processing command"
        while dt>0:
            print "command: ", dt
            if self.currentFunction is not None:
                dt = self.procesFunction(dt)
                if dt > 0:
                    self.currentFunction = None
            elif len(self.currentCommand) > 0:
                self.currentFunction = self.currentCommand.pop(0)
            else:
                self.currentCommand = None
                return dt
        return 0

    def procesFunction(self, dt):
        function = self.currentFunction.getFunction()
        params = self.currentFunction.getParams()
        if self.currentFunction.getTime() is not None:
            car.execute_function_with_id(function, duration = min(self.currentFunction.getTime(), dt), **params)
        else:
            car.execute_function_with_id(function, **params)
        return self.currentFunction.useTime(dt)


def getFunctionDivider():
    return functionDivider

functionDivider = FunctionDivider()