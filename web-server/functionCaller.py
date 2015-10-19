
__ioStream__ = None
__webCaller__ = None

"""
a class designed to communicate from the website to the BrickPi
"""
class __IOStream__:

    def __init__(self):
        self.queue = []
        pass

    def pushFunction(self):
        pass

    def addFunctionToQueue(self):
        pass

    def addFunctionFrontQueue(self):
        pass

    def removeFunctionFromQueue(self):
        pass

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

    def setWebsite(self,mainUrl):
        pass


"""
a class designed to comunicate from the BrickPi to the website
"""
class __WebCaller__:
    def __init__(self):
        pass

    def setPi(self):
        pass


def getIOStream():
    return __ioStream__


def getWebCaller():
    return __webCaller__


def init():
    global __ioStream__,__webCaller__
    __ioStream__ = __IOStream__()
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