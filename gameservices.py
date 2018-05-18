
from flask import Flask
from flask import jsonify
from flask import request
from gamedata import load_data
from gamedata import update_data

app = Flask(__name__)
@app.route('/')
def index():
    return '<div id="app"></div><script src="static/dist/build.js"></script>'
@app.route('/contact')
def contact():
    return '<table><tr><td>hello</td><td>games</td></tr></table>'
@app.route('/data', methods=['GET'])
def data():
    print request
    response = jsonify(load_data())#({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/update', methods=['GET'])
def update():
    response = jsonify(update_data(request))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
if __name__ == "__main__":
    app.run()
