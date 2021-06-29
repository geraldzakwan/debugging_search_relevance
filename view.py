import json

from config import DATA_FILEPATH, INVERTED_INDEX_FILEPATH, FEATURES

def fetch_products(product_IDs):
    with open(DATA_FILEPATH, "r") as infile:
        data = json.load(infile)

    result = []
    for ID in product_IDs:
        result.append(data[ID])

    return result

if __name__ == '__main__':
    print(fetch_products(set(["10"])))
