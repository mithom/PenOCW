import gevent.monkey
##gevent.monkey.patch_all()
from flask import Flask, render_template, request, jsonify, url_for, Response
import functionCaller as FC
import cameraPi
from platform import system
from flask_jsglue import JSGlue
from gevent.pool import Pool
import gevent
from flask_socketio import SocketIO, emit

app = Flask(__name__)
jsglue = JSGlue(app)  # this allows us to use url_for in the javascript frontend
app.config['SECRET_KEY'] = 'secret!'
# http = WSGIServer(('127.0.0.1', 5000), app)
socket = SocketIO(app)


@app.route('/', methods=['GET'])  # post niet meer
def index():
    if request.method == 'GET':
        return render_template('index.html')
    # if request.method == 'POST':
    #   print request.json
    #    params = request.json
    #    func = params.get('function')
    #    return procesFunctionCall(func)

'''
def procesFunctionCall(func):
        """if func == "doUp":
            FC.getIOStream().addFunctionToQueue()
            return jsonify(id="1")

        elif func == "doLeft":
            FC.getIOStream().addFunctionToQueue()
            return jsonify(id="1")

        elif func == "doDown":
            FC.getIOStream().addFunctionToQueue()
            return jsonify(id="1")

        elif func == "doRight":
            FC.getIOStream().addFunctionToQueue()
            return jsonify(id="1")"""
        if "do" == func[:2]:
            #id = FC.getIOStream().addCommandToQueue(func[2:])
            id = FC.getIOStream().addCommandToQueue("goForward")
            return jsonify(id=id)

        elif func == "stopUp":
            FC.getIOStream().removeCommandFromQueue(1)
            return jsonify(id="1")

        elif func == "stopLeft":
            FC.getIOStream().removeCommandFromQueue(1)
            return jsonify(id="1")

        elif func == "stopDown":
            FC.getIOStream().removeCommandFromQueue(1)
            return jsonify(id="1")

        elif func == "stopRight":
            FC.getIOStream().removeCommandFromQueue(1)
            return jsonify(id="5")

        return jsonify(error="unknown function")
'''


@socket.on("connect", namespace="/manueel")
def connectManueel():
    emit("alert", "welcome to the socketIO for manual driving")


@socket.on("connect", namespace="/complex")
def connectComplex():
    emit("alert", "welcome to the socketIO for complex figures")


@socket.on("connect", namespace="/beschrijving")
def connectBeschrijving():
    emit("alert", "welcome to the socketIO for route description")


@socket.on("disconnectManueel", namespace="/manueel")
def disconnect():
    print "nice to have met you."


@socket.on("disconnect", namespace="/complex")
def disconnectComplex():
    print "nice to have met you."


@socket.on("disconnect", namespace="/beschrijving")
def disconnectBeschrijving():
    print "nice to have met you."


def updateRouteDesciption():
    emit('updateRouteDescription', FC.getIOStream().getAllCommandOutputsInQueue(), namespace="/beschrijving", broadcast=True)


@socket.on("line", namespace="/complex")
def line(params):
    id = FC.getIOStream().addCommandToQueue("line")
    params["id"] = id
    emit('alert', params)


@socket.on("square", namespace="/complex")
def square(params):
    id = FC.getIOStream().addCommandToQueue("square")
    params["id"] = id
    emit('alert', params)


@socket.on("circle", namespace="/complex")
def circle(params):
    id = FC.getIOStream().addCommandToQueue("circle")
    params["id"] = id
    emit('alert', params)


@socket.on("up", namespace="/manueel")
def up(params):
    if params.get("status") == "active":
        id = FC.getIOStream().addCommandToQueue("goForward")
        params["id"] = id
    else:
        for output in FC.getIOStream().getAllCommandOutputsInQueue():
            if output["commandName"] == "goForward":
                FC.getIOStream().removeCommandFromQueue(output['id'])
                break
        # FC.getIOStream().removeCommandFromQueue(1)
    emit('alert', params)


@socket.on("down", namespace="/manueel")
def down(params):
    if params.get("status") == "active":
        id = FC.getIOStream().addCommandToQueue("goDown")
        params["id"] = id
    else:
        for output in FC.getIOStream().getAllCommandOutputsInQueue():
            if output["commandName"] == "goDown":
                FC.getIOStream().removeCommandFromQueue(output['id'])
                break
        # FC.getIOStream().removeCommandFromQueue(1)
    emit('alert', params)


@socket.on("left", namespace="/manueel")
def left(params):
    if params.get("status") == "active":
        id = FC.getIOStream().addCommandToQueue("goLeft")
        params["id"] = id
    else:
        for output in FC.getIOStream().getAllCommandOutputsInQueue():
            if output["commandName"] == "goLeft":
                FC.getIOStream().removeCommandFromQueue(output['id'])
                break
        # FC.getIOStream().removeCommandFromQueue(1)
    emit('alert', params)


@socket.on("right", namespace="/manueel")
def right(params):
    if params.get("status") == "active":
        id = FC.getIOStream().addCommandToQueue("goRight")
        params["id"] = id
    else:
        for output in FC.getIOStream().getAllCommandOutputsInQueue():
            if output["commandName"] == "goRight":
                FC.getIOStream().removeCommandFromQueue(output['id'])
                break
        # FC.getIOStream().removeCommandFromQueue(1)
    emit('alert', params)
    updateRouteDesciption()


@socket.on("start", namespace="/beschrijving")
def start(params):
    id = FC.getIOStream().addCommandToQueue("start")
    params["id"] = id
    emit('alert', params)
    updateRouteDesciption()


@socket.on("stop", namespace="/beschrijving")
def stop(params):
    id = FC.getIOStream().addCommandToQueue("stop")
    params["id"] = id
    emit('alert', params)
    updateRouteDesciption()


@socket.on("right", namespace="/beschrijving")
def descriptionRight(params):
    id = FC.getIOStream().addCommandToQueue("right")
    params["id"] = id
    emit('alert', params)
    updateRouteDesciption()


@socket.on("left", namespace="/beschrijving")
def descriptionLeft(params):
    id = FC.getIOStream().addCommandToQueue("left")
    params["id"] = id
    emit('alert', params)
    updateRouteDesciption()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        gevent.sleep(0)

pool = Pool(2)


@app.route('/video_feed.mjpg')
def video_feed():
    thread = gevent.spawn(gen,camera)
    pool.add(thread)
    pool.join()
    return Response(thread.value,
                    mimetype='multipart/x-mixed-replace; boundary=frame')


"""
this file is intended to run as imported module, if it runs as main,
debug options are on.
If this file is not run on the raspbery pi, a stream emulated will be used.
Otherwise the real camera is used.
"""
if system() == 'Linux':
    camera = cameraPi.Camera()
    camera.initialize() #make shure you don't have to wait once stream starts, but also start consuming battery (250mA)
else:
    camera = cameraPi.ECamera()

if __name__ == '__main__':
    lol = FC.getIOStream()
    socket.run(app, host='127.0.0.1',port=5000)

"""
om je eigen ip adress te vinden gebruik je in command prompt ipconfig (ifconfig voor linux)
en je neetm iPv4.
"""