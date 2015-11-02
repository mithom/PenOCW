import sys, functionDivider

__ioStream__ = None
__webCaller__ = None


class Command:
    """
    the commands that are stored in the queue
    """
    __idGen__ = None

    def __init__(self, commandName, **params):
        if Command.__idGen__ is None:
            Command.__idGen__ = getNextId()
        self.id = Command.__idGen__.next()
        self.commandName = commandName
        if params is not None:
            if params.get('id') is not None:
                self.id = params['id']
            self.__params__ = params
        else:
            self.__params__ = {}

    def getId(self):
        return self.id

    def getCommandName(self):
        return self.commandName

    def getParam(self, param):
        if param == "id":
            return self.getId()
        if param == "commandName":
            return self.getCommandName()
        return self.__params__.get(param, None)

    def output(self):
        return {"id": self.getId(),"commandName": self.getCommandName()}

    def __str__(self):
        return str(self.output())

    def __repr__(self):
        return str(self)


class __IOStream__:
    """
    a class designed to communicate from the website to the BrickPi
    """
    manueelCommands = ["goForward","goBackward","goLeft","goRight"]

    def __init__(self):
        self.queue = []

    def pushCommand(self):
        if len(self.queue) > 0:
            toExecute = self.queue[0]
            if toExecute.getCommandName() in __IOStream__.manueelCommands and len(self.queue) == 1:
                #self.addCommandFrontQueue(toExecute.getCommandName(), **toExecute.__params__)
                pass
            elif len(self.queue) > 1 and self.queue[1].getCommandName() in __IOStream__.manueelCommands:
                return self._getCombinedCommand(toExecute, self.queue[1])
            else:
                del self.queue[0]
            return toExecute
        return None

    @classmethod
    def _getCombinedCommand(cls, command1, command2):
        return command1
    # TODO: implementeren!!!

    def addCommandToQueue(self, commandName, **kwargs):
        if len(self.queue) == sys.maxint:
            return Exception("queue too long")
        newFunction = Command(commandName, **kwargs)
        self.queue.append(newFunction)
        print str(self.queue)
        return newFunction.getId()


    def addCommandFrontQueue(self, commandName, **kwargs):
        if len(self.queue) == sys.maxint:
            return Exception("queue too long")
        newFunction = Command(commandName,**kwargs)
        self.queue.insert(0, newFunction)
        return newFunction.getId()

    def executeCommandImmediatly(self,commandName):
        pass

    def removeCommandFromQueue(self, commandId):
        for function in self.queue:
            if commandId == function.getId():
                self.queue.remove(function)
                return True
        return False

    def cancelCurrentCommand(self):
        if functionDivider.getFunctionDivider().interuptCurrentCommand() is not None and len(self.queue) > 0:
            self.queue.pop(0)

    def cancelWholeQueue(self):
        self.queue = []
        self.cancelCurrentCommand()

    def start(self):
        pass

    def pause(self):
        pass

    def stop(self):
        pass

    def setWebsite(self, mainUrl):
        print mainUrl
        pass

    def getAllCommandOutputsInQueue(self):
        return [command.output() for command in self.queue]

class __WebCaller__:
    """
    a class designed to comunicate from the BrickPi to the website
    """
    def __init__(self):
        pass

    def setPi(self):
        pass


def getIOStream():
    if __ioStream__ is None:
        print "None"
    return __ioStream__


def getWebCaller():
    return __webCaller__


def getNextId():
    i = 0
    while True:
        if i == sys.maxint:
            i = 0
        i += 1
        yield i

__ioStream__ = __IOStream__()
__webCaller__ = __WebCaller__()
