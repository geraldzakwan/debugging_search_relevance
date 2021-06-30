import pickle

from flask import Flask, request, jsonify
from config import DEBUG, PORT

from config import FEATURES
from index import load_posting_index, load_term_count_index
from view import fetch, fetch_with_score

from preprocess import preprocess
from matching import match
from ranking import rank

app = Flask(__name__)
app.features = []

app.posting_indexes = load_posting_index()
app.term_count_indexes = load_term_count_index

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

@app.route("/analyze", methods=["GET", "POST"])
def do_analyze():
    if request.method == "GET":
        keywords = request.args.get("keywords", None)
    elif request.method == "POST":
        json_req = request.get_json()
        keywords = json_req["keywords"]
    else:
        return reply_error(code=400, message="Supported method is 'GET' and 'POST'")

    if keywords:
        return reply_success(data={
            "tokens": preprocess(keywords),
        })

    return reply_error(code=400, message="Keywords/search terms are not specified")

@app.route("/match", methods=["GET", "POST"])
def do_match():
    if request.method == "GET":
        keywords = request.args.get("keywords", None)
    elif request.method == "POST":
        json_req = request.get_json()
        keywords = json_req["keywords"]
    else:
        return reply_error(code=400, message="Supported method is 'GET' and 'POST'")

    if keywords:
        tokens = preprocess(keywords)
        product_IDs = match(app.posting_indexes, app.features, tokens)

        return reply_success(data={
            "products": fetch(product_IDs),
        })

    return reply_error(code=400, message="Keywords/search terms are not specified")

@app.route("/rank", methods=["GET", "POST"])
def do_rank():
    if request.method == "GET":
        keywords = request.args.get("keywords", None)
    elif request.method == "POST":
        json_req = request.get_json()
        keywords = json_req["keywords"]
    else:
        return reply_error(code=400, message="Supported method is 'GET' and 'POST'")

    if keywords:
        tokens = preprocess(keywords)
        product_IDs = match(app.posting_indexes, app.features, tokens)
        sorted_products = rank(app.posting_indexes, app.term_count_indexes, tokens, product_IDs)

        return reply_success(data={
            "products": fetch_with_score(sorted_products),
        })

    return reply_error(code=400, message="Keywords/search terms are not specified")

if __name__ == "__main__":
    if DEBUG:
        app.run(threaded=True, port=PORT, debug=True)
    else:
        app.run(threaded=True, port=PORT, debug=False)
