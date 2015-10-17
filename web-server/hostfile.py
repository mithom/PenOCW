import gevent.monkey
gevent.monkey.patch_all()
from flask import Flask, render_template, request, jsonify, url_for, Response
import functionCaller as FC
import cameraPi
from platform import system
from flask_jsglue import JSGlue
from gevent.pywsgi import WSGIServer
from gevent.pool import Pool
import gevent
from flask.ext.socketio import SocketIO,send,emit

app = Flask(__name__)
jsglue = JSGlue(app)  # this allows us to use url_for in the javascript frontend
app.config['SECRET_KEY'] = 'secret!'
http = WSGIServer(('127.0.0.1', 5000), app)
socketio = SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        print request.json
        params = request.json
        func = params.get('function')
        return procesFunctionCall(func)


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


@socketio.on("connect", namespace="/manualDriving")
def connectManualDriving():
    return "welcome to the socketIO for manual driving"

@socketio.on("disconnect", namespace="/manualDriving")
def disconnectManualDriving():
    return "nice to have met you."



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
    #app.run(debug=True, host='127.0.0.1', port=5000)
    socketio.run(debug=True, host='127.0.0.1',port=5000)
else:
    pass
    #appThread = threading.Thread(target=app.run,name="websiteHost",kwargs={"debug": False, "host": '0.0.0.0', "port": 4848})
    #appThread.start()
    #appThread = threading.Thread(target=http.serve_forever,name="websiteHost")
    #appThread.setDaemon(True)
    #appThread.start()
    #http.serve_forever()


"""
om je eigen ip adress te vinden gebruik je in command prompt ipconfig (ifconfig voor linux)
en je neetm iPv4.
"""
