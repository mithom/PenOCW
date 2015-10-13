from flask import Flask, render_template, request, jsonify, url_for
import functionCaller as FC

app = Flask(__name__)


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
        if func == "doUp":
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
            return jsonify(id="1")

        elif func == "stopUp":
            FC.getIOStream().removeFunctionFromQueue()
            return jsonify(id="1")

        elif func == "stopLeft":
            FC.getIOStream().removeFunctionFromQueue()
            return jsonify(id="1")

        elif func == "stopDown":
            FC.getIOStream().removeFunctionFromQueue()
            return jsonify(id="1")

        elif func == "stopRight":
            FC.getIOStream().removeFunctionFromQueue()
            return jsonify(id="1")

        return jsonify(error="unknown function")
"""
this file is intended to run as imported module, if it runs as main, debug options are on.
"""
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
