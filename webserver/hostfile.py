from flask import Flask, render_template, request, send_file, Response
import functionCaller as FC
import cameraPi
from platform import system
from flask_jsglue import JSGlue
# from gevent.pool import Pool
import gevent
from socketio.server import SocketIOServer
from werkzeug.wsgi import SharedDataMiddleware
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin, RoomsMixin
app = Flask(__name__)
jsglue = JSGlue(app)  # this allows us to use url_for in the javascript frontend
app.config['SECRET_KEY'] = 'secret!'

manueel = None
complex = None
beschrijving = None
beeldverwerking = None

# TODO:sockets omzetten naar get requests en 2 sockets overhouden, 1 voor laptop, 1 voor info zoals power en routeDescription


def sendPower(*args):
    global manueel
    if manueel is not None:
        #print "sending power"
        manueel.broadcast_event('power', *args)
    else:
        print "could not send power"


class ManueelNamespace(BaseNamespace, RoomsMixin,
                       BroadcastMixin):
    def __init__(self, *args, **kwargs):
        global manueel
        super(ManueelNamespace, self).__init__(*args, **kwargs)
        manueel = self

    def emit(self, event, args):
        self.socket.send_packet(dict(type="event", name=event,
                                     args=args, endpoint=self.ns_name))

    def recv_connect(self):
        print "manueel connect"
        self.emit('alert', "welkom  bij manuele aansturing")
        if complex is not None:
            complex.askDisconnect('manueel')
        if beschrijving is not None:
            beschrijving.askDisconnect('manueel')
        # self.broadcast_event('alert', 'nieuwe gebruiker!')
        # process = threading.Thread(target=sendPower,args=(self,), name='processing')
        # process.setDaemon(True)
        # process.start()
        # gevent.joinall([gevent.spawn(sendPower, self)])

    def askDisconnect(self, new):
        self.broadcast_event('askDisconnect', {"new": new})

    #def recv_disconnect(self):
        #print 'disconnected manueel'

    def on_up(self, params):
        if params.get("status") == "active":
            func_id = FC.getIOStream().addCommandToQueue("goForward")
            params["id"] = func_id
        else:
            for output in FC.getIOStream().getAllCommandOutputsInQueue():
                if output["commandName"] == "goForward":
                    FC.getIOStream().removeCommandFromQueue(output['id'])
                    # break
                    # FC.getIOStream().removeCommandFromQueue(1)
        self.emit('alert', params)

    def on_down(self, params):
        if params.get("status") == "active":
            func_id = FC.getIOStream().addCommandToQueue("goBackward")
            params["id"] = func_id
        else:
            for output in FC.getIOStream().getAllCommandOutputsInQueue():
                if output["commandName"] == "goBackward":
                    FC.getIOStream().removeCommandFromQueue(output['id'])
                    # break
                    # FC.getIOStream().removeCommandFromQueue(1)
        self.emit('alert', params)

    def on_left(self, params):
        if params.get("status") == "active":
            func_id = FC.getIOStream().addCommandToQueue("goLeft")
            params["id"] = func_id
        else:
            for output in FC.getIOStream().getAllCommandOutputsInQueue():
                if output["commandName"] == "goLeft":
                    FC.getIOStream().removeCommandFromQueue(output['id'])
                    # break
                    # FC.getIOStream().removeCommandFromQueue(1)
        self.emit('alert', params)

    def on_right(self, params):
        if params.get("status") == "active":
            func_id = FC.getIOStream().addCommandToQueue("goRight")
            params["id"] = func_id
        else:
            for output in FC.getIOStream().getAllCommandOutputsInQueue():
                if output["commandName"] == "goRight":
                    FC.getIOStream().removeCommandFromQueue(output['id'])
                    # break
                    # FC.getIOStream().removeCommandFromQueue(1)
        self.emit('alert', params)


class ComplexNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    def __init__(self, *args, **kwargs):
        global complex
        super(ComplexNamespace, self).__init__(*args, **kwargs)
        complex = self

    def askDisconnect(self, new):
        self.broadcast_event('askDisconnect', {"new": new})

    def emit(self, event, args):
        self.socket.send_packet(dict(type="event", name=event,
                                     args=args, endpoint=self.ns_name))

    def recv_connect(self):
        print "complex connect"
        self.emit('alert', "welkom  bij complexe aansturing")
        if manueel is not None:
            manueel.askDisconnect('complex')
        if beschrijving is not None:
            beschrijving.askDisconnect('complex')

    #def recv_disconnect(self):
        # print 'disconnected complex'

    def on_circle(self, data):
        func_id = FC.getIOStream().addCommandToQueue('makeCircle')
        data['id'] = func_id
        self.emit('alert', data)

    def on_square(self, data):
        func_id = FC.getIOStream().addCommandToQueue('makeSquare')
        data['id'] = func_id
        self.emit('alert', data)

    def on_line(self, data):
        func_id = FC.getIOStream().addCommandToQueue('makeLine')
        data['id'] = func_id
        self.emit('alert', data)


class BeschrijvingNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    def __init__(self, *args, **kwargs):
        global beschrijving
        super(BeschrijvingNamespace, self).__init__(*args, **kwargs)
        beschrijving = self

    def emit(self, event, args):
        self.socket.send_packet(dict(type="event", name=event,
                                     args=args, endpoint=self.ns_name))

    def askDisconnect(self, new):
        self.broadcast_event('askDisconnect', {"new": new})

    def recv_connect(self):
        print "beschrijving connect"
        self.emit('alert', "welkom  bij wegbeschrijving")
        if manueel is not None:
            manueel.askDisconnect("beschrijving")
        if complex is not None:
            complex.askDisconnect("beschrijving")

    #def recv_disconnect(self):
        #print 'disconnected beschrijving'

    def update_route_description(self):
        if beeldverwerking is not None:
            beeldverwerking.update_route_description()
        else:
            print "beeldverwerking was None"
        self.broadcast_event('updateRouteDescription', FC.getIOStream().getAllCommandOutputsInQueue())

    def on_start(self, params):
        func_id = FC.getIOStream().addCommandToQueue("start")
        params["id"] = func_id
        self.emit('alert', params)
        self.update_route_description()

    def on_stop(self, params):
        func_id = FC.getIOStream().addCommandToQueue("stop", **params)
        params["id"] = func_id
        self.emit('alert', params)
        self.update_route_description()

    def on_right(self, params):
        func_id = FC.getIOStream().addCommandToQueue("right", **params)
        params["id"] = func_id
        self.emit('alert', params)
        self.update_route_description()

    def on_left(self, params):
        func_id = FC.getIOStream().addCommandToQueue("left", **params)
        params["id"] = func_id
        self.emit('alert', params)
        self.update_route_description()


class BeeldverwerkingNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    def __init__(self, *args, **kwargs):
        global beeldverwerking
        super(BeeldverwerkingNamespace, self).__init__(*args, **kwargs)
        beeldverwerking = self

    def emit(self, event, args):
        self.socket.send_packet(dict(type="event", name=event,
                                     args=args, endpoint=self.ns_name))

    def update_route_description(self):
        self.broadcast_event('update_route_description', FC.getIOStream().getAllCommandOutputsInQueue())

    def on_command_finished(self, params):
        succes = False
        command_id = params.get('id', None)
        if command_id is not None:
            #succes = FC.getIOStream().removeCommandFromQueue(command_id)
            FC.functionDivider.getFunctionDivider().interuptCurrentFunction()
            succes = True
            beschrijving.update_route_description()
        if not succes:
            self.emit("event_confirmation", {'succes': False, 'id': command_id})
        else:
            self.emit("event_confirmation", {'succes': True, 'id': command_id})

    def on_set_power(self, params):
        func = FC.functionDivider.getFunctionDivider().currentCommand
        if func is not None and len(func) > 0:
            print params
            if func[0].getParams().has_key("left"):
                func[0].set_params(**params)
        else:
            print "could not set powers"


@app.route("/socket.io/<path:rest>")
def run_socketio(rest):
    socketio_manage(request.environ, {'/manueel': ManueelNamespace, '/complex': ComplexNamespace,
                                      '/beschrijving': BeschrijvingNamespace,
                                      '/beeldverwerking': BeeldverwerkingNamespace})
    return ''


@app.route('/', methods=['GET'])  # post niet meer
def index():
    if request.method == 'GET':
        return render_template('index.html')


def gen(cam):
    while True:
        gevent.sleep()
        frame = cam.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# pool = Pool(5)

@app.route('/video_feed.mjpg')
def video_feed():
    thread = gevent.spawn(gen, camera)
    # pool.add(thread)
    # pool.join()
    thread.join()
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
    #camera.initialize()
    # make shure you don't have to wait once stream starts, but also start consuming battery (250mA)
else:
    camera = cameraPi.ECamera()

if __name__ == '__main__':
    lol = FC.getIOStream()
    server = SocketIOServer(
        ('0.0.0.0', 4848),
        SharedDataMiddleware(app, {}),
        namespace="socket.io",
        policy_server=False)
    server.serve_forever()
    # socket.run(app, host='127.0.0.1',port=5000)

"""
om je eigen ip adress te vinden gebruik je in command prompt ipconfig (ifconfig voor linux)
en je neetm iPv4.
"""
