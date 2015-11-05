import webserver.hostfile as hostfile
import webserver.functionDivider as functionDivider
import webserver.functionCaller
import sys, os, threading
import time
# import Team_auto.Car as car
import werkzeug.serving

from socketio.server import SocketIOServer
from werkzeug.wsgi import SharedDataMiddleware

__author__ = 'Thomas'
app = hostfile.app


def proces_forever():
    while True:
        print "running"
        FD.processTime(100)


def updateValues():
    while True:
        print "updating is so fun: ", webserver.functionDivider.car.isUpdated
        time.sleep(0.1)
        if webserver.functionDivider.car.isUpdated:
            hostfile.sendPower()
            webserver.functionDivider.car.isUpdated = False


def main():
    global FD
    FD = functionDivider.getFunctionDivider()
    process = threading.Thread(target=proces_forever, name='processing')
    process.setDaemon(True)
    process.start()

    process2 = threading.Thread(target=updateValues, name='processing')
    process2.setDaemon(True)
    process2.start()

    app.debug = True
    server = SocketIOServer(
        ('0.0.0.0', 4848),
        SharedDataMiddleware(app, {}),
        namespace="socket.io",
        policy_server=False)
    server.serve_forever()
    # add other proces for adjusting to obstacles etc
    # hostfile.http.serve_forever()


def gunicorn():
    global FD
    FD = functionDivider.getFunctionDivider()
    process = threading.Thread(target=proces_forever, name='processing')
    process.setDaemon(True)
    process.start()

#    hostfile.socket.run(hostfile.app, host='0.0.0.0', port=4848)

if __name__ == "__main__":
    print "run.py is main"
    main()
else:
    print "running thread function, server must be started with gunicorn"
    gunicorn()
##    main()
