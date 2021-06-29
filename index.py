import os
import json

from preprocess import preprocess
from config import DATA_FILEPATH, INVERTED_INDEX_FILEPATH, FEATURES

def reindex():
    # Load our product data, see data/products.json
    with open(DATA_FILEPATH, "r") as infile:
        data = json.load(infile)

    # Initiate index
    # Each feature will have its own (inverted) index
    indexes = {}
    for feature in FEATURES:
        indexes[feature["name"]] = {}

    # Populate the index with product data
    for product_ID, elem in enumerate(data):
        for feature in FEATURES:
            feature_name = feature["name"]

            # For string type feature, we need to tokenize it first
            # Then, each token will be a key!
            if feature["type"] == "string":
                for token in preprocess(elem[feature_name]):
                    if not token in indexes[feature_name]:
                        indexes[feature_name][token] = set()

                    # The (list of) value will be the product id
                    indexes[feature_name][token].add(product_ID)

            # For numerical features, we let it be (no tokenization whatsoever)
            else:
                if not elem[feature_name] in indexes[feature_name]:
                    indexes[feature_name][elem[feature_name]] = set()

                indexes[feature_name][elem[feature_name]].add(product_ID)

    # Dump index to text file, example format: "asus 0,1"
    # See data/inverted_index for details (there is one file for each feature)
    for feature in FEATURES:
        feature_name = feature["name"]

        with open(os.path.join(INVERTED_INDEX_FILEPATH, feature_name + ".json"), "w") as outfile:
            for elem in indexes[feature_name]:
                outfile.write(str(elem) + " ")

                for idx, product_ID in enumerate(indexes[feature_name][elem]):
                    outfile.write(str(product_ID))

                    if idx < len(indexes[feature_name][elem]) - 1:
                        outfile.write(",")

                outfile.write("\n")

def load_index():
    indexes = {}

    for feature in FEATURES:
        feature_name = feature["name"]
        indexes[feature_name] = {}

        with open(os.path.join(INVERTED_INDEX_FILEPATH, feature_name + ".json"), "r") as infile:
            for line in infile.readlines():
                term, postings = line.strip("\n").split(" ")
                posting_list = postings.split(",")

                indexes[feature_name][term] = posting_list

    return indexes

if __name__ == '__main__':
    reindex()
