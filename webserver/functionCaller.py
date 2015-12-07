import sys
import functionDivider
import hostfile

__ioStream__ = None
__webCaller__ = None


class Command:
    """
    the commands that are stored in the queue
    """
    __idGen__ = None

    def __init__(self, commandName, **params):
        if Command.__idGen__ is None:
            Command.__idGen__ = Command.getNextId()
        self.id = Command.__idGen__.next()
        self.commandName = commandName
        self.functions = None  # only used when command is interupted
        if params is not None:
            if params.get('id') is not None:
                self.id = params['id']
            self.__params__ = params
        else:
            self.__params__ = {}

    @staticmethod
    def getNextId():
        i = 0
        while True:
            if i == sys.maxint:
                i = 0
            i += 1
            yield i

    def getId(self):
        return self.id

    def getCommandName(self):
        return self.commandName

    def getParam(self, param, default_value):
        if param == "id":
            return self.getId()
        if param == "commandName":
            return self.getCommandName()
        return self.__params__.get(param, default_value)

    def output(self):
        return {"id": self.getId(), "commandName": self.getCommandName(), "params": self.__params__}

    def __str__(self):
        return str(self.output())

    def __repr__(self):
        return str(self)

    def is_paused(self):
        return self.functions is not None

    def get_functions(self):
        return self.functions

    def pause_with_updated_params(self, functions):
        self.functions = functions


class __IOStream__:
    """
    a class designed to communicate from the website to the BrickPi
    """
    manueelCommands = ["goForward", "goBackward", "goLeft", "goRight"]
    manueelValues={"goForward":1, "goBackward":-1, "goLeft":10, "goRight":-10, "pass":0}
    combinedValues={0: "pass", 11: "goForwardLeft", -9: "goForwardRight", 9: "goBackwardLeft", -11: "goBackwardRight", 1: "goForward", -1: "goBackward", 10: "goLeft", -10: "goRight"}

    def __init__(self):
        self.queue = []

    def pushCommand(self):
        if len(self.queue) > 0:
            toExecute = self.queue.pop(0)
            if toExecute.getCommandName() in __IOStream__.manueelCommands and len(self.queue) == 0:
                self.queue.insert(0, toExecute)
                # self.addCommandFrontQueue(toExecute.getCommandName(), **toExecute.__params__)
            elif len(self.queue) > 0 and self.queue[0].getCommandName() in __IOStream__.manueelCommands:
                self.queue.insert(0,toExecute)
                toExecute = self._getCombinedCommand(toExecute, self.queue[1])
            return toExecute
        return None

    @classmethod
    def _getCombinedCommand(cls, command1, *args):
        naam = command1.getCommandName()
        for command in args:
            naam = cls.combinedValues[cls.manueelValues[naam] + cls.manueelValues[command.getCommandName()]]
        return Command(naam)

    def addCommandToQueue(self, commandName, **kwargs):
        if len(self.queue) == sys.maxint:
            return Exception("queue too long")
        if commandName in self.manueelCommands:
            for command in self.queue:
                if command.getCommandName() == commandName:
                    return command.getId()
        newFunction = Command(commandName, **kwargs)
        self.queue.append(newFunction)
        print str(self.queue)
        return newFunction.getId()

    def addCommandFrontQueue(self, commandName, **kwargs):
        if len(self.queue) == sys.maxint:
            return Exception("queue too long")
        newFunction = Command(commandName, **kwargs)
        self.queue.insert(0, newFunction)
        return newFunction.getId()

    def executeCommandImmediatly(self, commandName):
        pass

    def removeCommandFromQueue(self, commandId):
        for function in self.queue:
            if commandId == function.getId():
                self.queue.remove(function)
                return True
        current = functionDivider.getFunctionDivider().currentCommandObject
        if current.getId() == commandId:
            functionDivider.getFunctionDivider().interuptCurrentCommand()
            return True
        return False

    def cancelCurrentCommand(self):
        if functionDivider.getFunctionDivider().interuptCurrentCommand() is not None and len(self.queue) > 0:
            self.queue.pop(0)

    def cancelWholeQueue(self):
        self.queue = []
        self.cancelCurrentCommand()

    def setWebsite(self, mainUrl):
        print mainUrl
        pass

    def getAllCommandOutputsInQueue(self):
        output = [command.output() for command in self.queue]
        current = functionDivider.getFunctionDivider().currentCommandObject
        if current is not None:
            output.insert(0, current.output())
        return output


class __WebCaller__:
    """
    a class designed to comunicate from the BrickPi to the website
    """

    def __init__(self):
        pass

    def isUpdateAvailable(self):
        while True:
            yield functionDivider.car.isUpdated


def getIOStream():
    if __ioStream__ is None:
        print "None"
    return __ioStream__


def getWebCaller():
    return __webCaller__


__ioStream__ = __IOStream__()
__webCaller__ = __WebCaller__()
