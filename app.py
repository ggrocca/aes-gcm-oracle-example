from flask import Flask
from flask import request
from flask import jsonify
from aesgcm_wrapper import encode_dict

app = Flask(__name__)

@app.route('/')
def default_root():
    return "The API supports only a application/json POST to /oracleinvocation\n"

@app.route('/oracleinvocation', methods = ['POST'])
def oracleinvocation():
    return jsonify(encode_dict(request.json))

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
