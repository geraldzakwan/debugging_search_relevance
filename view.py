import json

from config import DATA_FILEPATH, INVERTED_INDEX_FILEPATH, FEATURES

def fetch_with_match(IDs, detail_matching):
    with open(DATA_FILEPATH, "r") as infile:
        data = json.load(infile)

    result = []
    for ID in IDs:
        product = data[ID]
        product["match"] = detail_matching

        result.append(product)

    return result

def fetch_with_score(sorted_products, detail_scores):
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
        tf_scores = {}
        for feature_name in detail_scores["tf"]:
            tf_scores[feature_name] = detail_scores["tf"][feature_name][ID]

        idf_scores = detail_scores["idf"]

        scores = {
            "final_score": sorted_product_scores[idx],
            "tf": tf_scores,
            "idf": idf_scores
        }

        product_data = data[ID]

        product_data["ID"] = ID
        product_data["scores"] = scores

        result.append(product_data)

    return result

if __name__ == '__main__':
    print(fetch(set(["10"])))
