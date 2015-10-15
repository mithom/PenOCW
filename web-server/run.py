import hostfile, functionDivider, functionCaller, sys, os, threading
#import Team_auto.Car as car

__author__ = 'Thomas'
    

def proces_forever():
    while True:
        print "running"
        FD.processTime(100)


if __name__ == "__main__":
    FD = functionDivider.FunctionDivider()
    proces = threading.Thread(target=proces_forever, name='processing')
    proces.setDaemon(True)
    proces.start()
    #add other proces for adjusting to obstacles etc
    hostfile.http.serve_forever()
