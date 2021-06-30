import json

from config import DATA_FILEPATH, INVERTED_INDEX_FILEPATH, FEATURES

def fetch(IDs):
    with open(DATA_FILEPATH, "r") as infile:
        data = json.load(infile)

    result = []
    for ID in IDs:
        result.append(data[ID])

    return result

def fetch_with_score(sorted_products):
    with open(DATA_FILEPATH, "r") as infile:
        data = json.load(infile)

    sorted_product_IDs = []
    for product in sorted_products:
        sorted_product_IDs.append(product[0])

    sorted_product_scores = []
    for product in sorted_products:
        sorted_product_scores.append(product[1])

    result = []
    for idx, ID in enumerate(sorted_product_IDs):
        product_data = data[ID]
        product_data["score"] = sorted_product_scores[idx]
        result.append(product_data)

    return result

if __name__ == '__main__':
    print(fetch(set(["10"])))
