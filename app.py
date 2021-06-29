import pickle

from flask import Flask, request, jsonify
from config import DEBUG, PORT

from config import FEATURES
from index import load_index
from matching import match
from view import fetch

app = Flask(__name__)
app.indexes = load_index()
app.features = []

for feature in FEATURES:
    if feature["use"]:
        app.features.append(feature["name"])

def reply_success(data):
    response = jsonify({
        "data": data
    })

    response.headers['Access-Control-Allow-Origin'] = '*'

    return response

def reply_error(code, message):
    response = jsonify({
        "error": {
            "code": code,
            "message": message
        }
    })

    response.headers['Access-Control-Allow-Origin'] = '*'

    return response

@app.route("/")
def index():
    return "<h1>Presenting you the dumb Search Engine</h1>"

@app.route("/query", methods=["GET", "POST"])
def query():
    if request.method == "GET":
        keywords = request.args.get("keywords", None)
    elif request.method == "POST":
        json_req = request.get_json()
        keywords = json_req["keywords"]
    else:
        return reply_error(code=400, message="Supported method is 'GET' and 'POST'")

    if keywords:
        product_IDs = match(app.indexes, app.features, keywords)

        return reply_success(data={
            "products": fetch(product_IDs),
        })

    return reply_error(code=400, message="Keywords/search terms are not specified")

if __name__ == "__main__":
    if DEBUG:
        app.run(threaded=True, port=PORT, debug=True)
    else:
        app.run(threaded=True, port=PORT, debug=False)
