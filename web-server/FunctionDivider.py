"""
deze module neemt de functie die momenteel uitgevoerd wordt, en splitst deze
op in kleinere functies om zo te kunnen zorgen dat ze ter plekke afgebroken
kunnen worden
"""

import functionCaller, time
#import Team_auto.Car as car

class Function:
    """
    the functions that are stored in the queue
    """

    def __init__(self, function, time=1000):
        if(type(function) == Function):
            self.function = function.getFunction()
            self.time = function.getTime()
        else:
            self.function = function
            self.time = time

    def getFunction(self):
        return self.function

    def getTime(self):
        return self.time

    def useTime(self, dt):
        self.time -= dt #dit moet uitgebreider, bvb nooit onder 0


def haha(power=1):
    print "power: ", power


class FunctionDivider:
    """
    transforms commands into functions that the Car can execute. Also allows interuption of these commands.
    """
    commandLib={"goForward": [Function(haha, 100)], "goBackward":[]} #the list contains the functions that should be executed in order to drive the car

    def __init__(self, firstCommand = None):
        self.currentCommand = None
        self.currentFunction = None
        if firstCommand is not None:
            self.executeCommand(firstCommand)

    def executeCommand(self,command):
        if command is not None and command.getCommandName() in FunctionDivider.commandLib.keys():
            self.currentCommand = [Function(x) for x in FunctionDivider.commandLib[command.getCommandName()]]
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
            if self.currentCommand is not None and len(self.currentCommand)>0:
                dt = self.processCommand(dt)
            else:
                self.executeCommand(functionCaller.getIOStream().pushCommand())
                print self.currentCommand, "current command"
                if self.currentCommand == None: #geen commands in queue
                    time.sleep(1)
                    dt -= 1

    def processCommand(self,dt):
        print "processing command"
        while dt>0:
            print "command: ", dt
            if self.currentFunction is not None:
                dt = self.procesFunction(dt)
            elif len(self.currentCommand)>0:
                self.currentFunction = self.currentCommand.pop(0)
            else:
                return dt
        return 0

    def procesFunction(self,dt):
        a = self.currentFunction.getFunction()
        a(100)
        return 0