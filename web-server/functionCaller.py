import sys

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
    def __init__(self):
        self.queue = []

    def pushCommand(self):
        if len(self.queue) > 0:
            return self.queue.pop(0)
        return None

    def addCommandToQueue(self, commandName):
        if len(self.queue) == sys.maxint:
            return Exception("queue too long")
        newFunction = Command(commandName)
        self.queue.append(newFunction)
        print str(self.queue)
        return newFunction.getId()


    def addCommandFrontQueue(self, commandName):
        if len(self.queue) == sys.maxint:
            return Exception("queue too long")
        newFunction = Command(commandName)
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
        pass

    def cancelWholeQueue(self):
        pass

    def start(self):
        pass

    def pause(self):
        pass

    def stop(self):
        pass

    def setWebsite(self, mainUrl):
        print mainUrl
        pass


class __WebCaller__:
    """
    a class designed to comunicate from the BrickPi to the website
    """
    def __init__(self):
        pass

    def setPi(self):
        pass


def getIOStream():
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


def init():
    global __ioStream__, __webCaller__
    if __ioStream__ is None:
        __ioStream__ = __IOStream__()
    if __webCaller__ is None:
        __webCaller__ = __WebCaller__()


def testinit():
    ioStream = __IOStream__()
    webCaller = __WebCaller__()
    print "created all instances"

"""if this module is run as main module, it will be tested"""
if __name__ == "__main__":
    testinit()

"""if the module is imported, this will configure everything"""
if __name__ == "functionCaller":
    init()