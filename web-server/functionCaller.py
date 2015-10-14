import sys

__ioStream__ = None
__webCaller__ = None


class Function:
    """
    the functions that are stored in the queue
    """
    __idGen__ = None

    def __init__(self, functionName, **params):
        if Function.__idGen__ is None:
            Function.__idGen__ = getNextId()
        self.id = Function.__idGen__.next()
        self.functionName = functionName
        if params is not None:
            self.__params__ = params
        else:
            self.__params__ = {}

    def getId(self):
        return self.id

    def getFunctionName(self):
        return self.functionName

    def getParam(self, param):
        if param == "id":
            return self.getId()
        if param == "functionName":
            return self.getFunctionName()
        return self.__params__.get(param, None)

    def output(self):
        return {"id": self.getId(),"functionName": self.getFunctionName()}


class __IOStream__:
    """
    a class designed to communicate from the website to the BrickPi
    """
    def __init__(self):
        self.queue = []

    def pushFunction(self):
        if len(self.queue) > 0:
            return self.queue.pop(0)

    def addFunctionToQueue(self, functionName):
        if len(self.queue) == sys.maxint:
            return Exception("queue too long")
        newFunction = Function(functionName)
        self.queue.append(newFunction)
        return newFunction.getId()


    def addFunctionFrontQueue(self, functionName):
        if len(self.queue) == sys.maxint:
            return Exception("queue too long")
        newFunction = Function(functionName)
        self.queue.insert(0, newFunction)
        return newFunction.getId()

    def executeFunctionImmediatly(self,functionName):
        pass

    def removeFunctionFromQueue(self, functionId):
        for function in self.queue:
            if functionId == function.getId():
                self.queue.remove(function)
                return True
        return False

    def cancelCurrentFucntion(self):
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