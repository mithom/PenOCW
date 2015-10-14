from flask import Flask, render_template, request, jsonify, url_for, Response
import functionCaller as FC
import cameraPi
from platform import system
from flask_jsglue import JSGlue

app = Flask(__name__)
jsglue = JSGlue(app) # this allows us to use url_for in the javascript frontend

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
            id = FC.getIOStream().addFunctionToQueue(func[2:])
            return jsonify(id=id)

        elif func == "stopUp":
            FC.getIOStream().removeFunctionFromQueue(1)
            return jsonify(id="1")

        elif func == "stopLeft":
            FC.getIOStream().removeFunctionFromQueue(1)
            return jsonify(id="1")

        elif func == "stopDown":
            FC.getIOStream().removeFunctionFromQueue(1)
            return jsonify(id="1")

        elif func == "stopRight":
            FC.getIOStream().removeFunctionFromQueue(1)
            return jsonify(id="5")

        return jsonify(error="unknown function")

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(camera),
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
    app.run(debug=True, host='127.0.0.1', port=5000)
else:
    FC.getIOStream().setWebsite(url_for('index'))
    app.run(debug=False, host='0.0.0.0', port=4848)

"""
om je eigen ip adress te vinden gebruik je in command prompt ipconfig (ifconfig voor linux)
en je neetm iPv4.
"""
