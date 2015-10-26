import webserver.hostfile as hostfile
import webserver.functionDivider as functionDivider
import sys, os, threading
#import Team_auto.Car as car
import werkzeug.serving

__author__ = 'Thomas'
    

def proces_forever():
    while True:
        print "running"
        FD.processTime(100)


if __name__ == "__main__":
    FD = functionDivider.getFunctionDivider()
    process = threading.Thread(target=proces_forever, name='processing')
    process.setDaemon(True)
    process.start()
    # add other proces for adjusting to obstacles etc
    # hostfile.http.serve_forever()
    hostfile.socket.run(hostfile.app, host='0.0.0.0', port=4848)