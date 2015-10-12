from flask import Flask,render_template,request,make_response,jsonify

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        print request.json
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=4848)

"""
om je eigen ip adress te vinden gebruik je in command prompt ipconfig (ifconfig voor linux)
en je neetm iPv4.
"""
