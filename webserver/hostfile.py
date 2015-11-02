import gevent.monkey
gevent.monkey.patch_all()
from flask import Flask, render_template, request, send_file, Response
import functionCaller as FC
import cameraPi
from platform import system
from flask_jsglue import JSGlue
from gevent.pool import Pool
import gevent
#from flask_socketio import SocketIO, emit
# http = WSGIServer(('127.0.0.1', 5000), app)
#socket = SocketIO(app)
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin, RoomsMixin


app = Flask(__name__)
jsglue = JSGlue(app)  # this allows us to use url_for in the javascript frontend
app.config['SECRET_KEY'] = 'secret!'


class ManueelNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    def __init__(self, *args, **kwargs):
        super(ManueelNamespace, self).__init__(*args, **kwargs)

    def emit(self, event, args):
        self.socket.send_packet(dict(type="event", name=event,
            args=args, endpoint=self.ns_name))

    def recv_connect(self):
        print "manueel connect"
        self.emit('alert', "welkom  bij manuele aansturing")
        #self.broadcast_event('alert', 'nieuwe gebruiker!')

    def recv_message(self, message):
        print "PING!!!", message

    def on_up(self, params):
        if params.get("status") == "active":
            id = FC.getIOStream().addCommandToQueue("goForward")
            params["id"] = id
        else:
            for output in FC.getIOStream().getAllCommandOutputsInQueue():
                if output["commandName"] == "goForward":
                    FC.getIOStream().removeCommandFromQueue(output['id'])
                    break
            # FC.getIOStream().removeCommandFromQueue(1)
        self.emit('alert', params)

    def on_down(self, params):
        if params.get("status") == "active":
            id = FC.getIOStream().addCommandToQueue("goBackward")
            params["id"] = id
        else:
            for output in FC.getIOStream().getAllCommandOutputsInQueue():
                if output["commandName"] == "goDown":
                    FC.getIOStream().removeCommandFromQueue(output['id'])
                    break
            # FC.getIOStream().removeCommandFromQueue(1)
        self.emit('alert', params)

    def on_left(self, params):
        if params.get("status") == "active":
            id = FC.getIOStream().addCommandToQueue("goLeft")
            params["id"] = id
        else:
            for output in FC.getIOStream().getAllCommandOutputsInQueue():
                if output["commandName"] == "goLeft":
                    FC.getIOStream().removeCommandFromQueue(output['id'])
                    break
            # FC.getIOStream().removeCommandFromQueue(1)
        self.emit('alert', params)

    def on_right(self, params):
        if params.get("status") == "active":
            id = FC.getIOStream().addCommandToQueue("goRight")
            params["id"] = id
        else:
            for output in FC.getIOStream().getAllCommandOutputsInQueue():
                if output["commandName"] == "goRight":
                    FC.getIOStream().removeCommandFromQueue(output['id'])
                    break
            # FC.getIOStream().removeCommandFromQueue(1)
        self.emit('alert', params)


class ComplexNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    def __init__(self, *args, **kwargs):
        super(ComplexNamespace, self).__init__(*args, **kwargs)

    def emit(self, event, args):
        self.socket.send_packet(dict(type="event", name=event,
            args=args, endpoint=self.ns_name))

    def recv_connect(self):
        print "complex connect"
        self.emit('alert', "welkom  bij complexe aansturing")

    def recv_message(self, message):
        print "PING!!!", message

    def on_circle(self, data):
        id = FC.getIOStream().addCommandToQueue('makeCircle')
        data['id'] = id
        self.emit('alert', data)

    def on_square(self, data):
        id = FC.getIOStream().addCommandToQueue('makeSquare')
        data['id'] = id
        self.emit('alert', data)

    def on_line(self, data):
        id = FC.getIOStream().addCommandToQueue('makeLine')
        data['id'] = id
        self.emit('alert', data)

    def on_start(self, data):
        #TODO: implementeren
        pass



class BeschrijvingNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    def __init__(self, *args, **kwargs):
        super(BeschrijvingNamespace, self).__init__(*args, **kwargs)

    def emit(self, event, args):
        self.socket.send_packet(dict(type="event", name=event,
            args=args, endpoint=self.ns_name))

    def recv_connect(self):
        print "beschrijving connect"
        self.emit('alert', "welkom  bij wegbeschrijving")

    def recv_message(self, message):
        print "PING!!!", message


@app.route("/socket.io/<path:rest>")
def run_socketio(rest):
    socketio_manage(request.environ, {'/manueel': ManueelNamespace, '/complex': ComplexNamespace, '/beschrijving': BeschrijvingNamespace})
    return ''


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
@socket.on("disconnect", namespace="/manueel")
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
'''

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        gevent.sleep(0)

pool = Pool(5)


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
"""""""
if system() == 'Linux':
        camera = cameraPi.Camera()
        camera.initialize() #make shure you don't have to wait once stream starts, but also start consuming battery (250mA)
else:
    camera = cameraPi.ECamera()"""
camera = cameraPi.ECamera()

if __name__ == '__main__':
    lol = FC.getIOStream()
    #socket.run(app, host='127.0.0.1',port=5000)

"""
om je eigen ip adress te vinden gebruik je in command prompt ipconfig (ifconfig voor linux)
en je neetm iPv4.
"""
