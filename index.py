import os
import json

from preprocess import preprocess
from config import DATA_FILEPATH, INVERTED_INDEX_FILEPATH, TERM_COUNT_FILEPATH, FEATURES

def reindex():
    # Load our product data, see data/products.json
    with open(DATA_FILEPATH, "r") as infile:
        data = json.load(infile)

    # Initiate index
    # Each feature will have its own (inverted and term count) index
    posting_indexes = {}
    for feature in FEATURES:
        posting_indexes[feature["name"]] = {}

    term_count_indexes = {}

    # Populate the index with product data
    for product_ID in data:
        product = data[product_ID]
        term_count_indexes[product_ID] = {}

        for feature in FEATURES:
            feature_name = feature["name"]
            term_count_indexes[product_ID][feature_name] = {}

            # For string type feature, we need to tokenize it first
            # Then, each token will be a key!
            if feature["type"] == "string":
                for token in preprocess(product[feature_name]):
                    if not token in posting_indexes[feature_name]:
                        posting_indexes[feature_name][token] = set()

                    # The (list of) value will be the product id
                    posting_indexes[feature_name][token].add(product_ID)

                    if not token in term_count_indexes[product_ID][feature_name]:
                        term_count_indexes[product_ID][feature_name][token] = 0

                    term_count_indexes[product_ID][feature_name][token] += 1

    # Dump inverted index to text file, example format: "asus 0,1"
    # See data/inverted_index for details (there is one file for each feature)
    for feature in FEATURES:
        feature_name = feature["name"]

        with open(os.path.join(INVERTED_INDEX_FILEPATH, feature_name + ".json"), "w") as outfile:
            for elem in posting_indexes[feature_name]:
                outfile.write(str(elem) + " ")

                for idx, product_ID in enumerate(posting_indexes[feature_name][elem]):
                    outfile.write(str(product_ID))

                    if idx < len(posting_indexes[feature_name][elem]) - 1:
                        outfile.write(",")

                outfile.write("\n")

    # Dump term count index to text file
    # See data/term_count_index for details (there is one file for each feature)
    for feature in FEATURES:
        feature_name = feature["name"]

        for product_ID in data:
            with open(os.path.join(TERM_COUNT_FILEPATH, feature_name, str(product_ID) + ".json"), "w") as outfile:
                for token in term_count_indexes[product_ID][feature_name]:
                    outfile.write(token + " " + str(term_count_indexes[product_ID][feature_name][token]) + "\n")

def load_posting_index():
    posting_indexes = {}

    # Load one index per feature
    for feature in FEATURES:
        feature_name = feature["name"]
        posting_indexes[feature_name] = {}

        with open(os.path.join(INVERTED_INDEX_FILEPATH, feature_name + ".json"), "r") as infile:
            for line in infile.readlines():
                # Two important things: term/token and its associated products (the postings)
                term, postings = line.strip("\n").split(" ")
                posting_list = postings.split(",")

                posting_indexes[feature_name][term] = posting_list

    return posting_indexes

def load_term_count_index():
    term_count_indexes = {}

    # Load our product data, see data/products.json
    with open(DATA_FILEPATH, "r") as infile:
        data = json.load(infile)

    term_count_indexes = {}
    for product_ID in data:
        term_count_indexes[product_ID] = {}

    for product_ID in data:
        for feature in FEATURES:
            feature_name = feature["name"]
            term_count_indexes[product_ID][feature_name] = {}

            with open(os.path.join(TERM_COUNT_FILEPATH, feature_name, str(product_ID) + ".json"), "r") as infile:
                for line in infile.readlines():
                    token, term_count = line.strip("\n").split(" ")

                    term_count_indexes[product_ID][feature_name][token] = int(term_count)

    return term_count_indexes

if __name__ == '__main__':
    reindex()
    print("-" * 100)
    print(load_posting_index())
    print("-" * 100)
    print(load_term_count_index())
    print("-" * 100)
