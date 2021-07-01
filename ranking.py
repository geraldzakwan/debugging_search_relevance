import math

from config import FEATURES, TF_VARIATIONS, TF_VERSION, IDF_VERSION, IDF_VARIATIONS

def compute_tf(feature_name, product_ID, token, term_count_indexes):
    if token in term_count_indexes[product_ID][feature_name]:
        if TF_VARIATIONS[TF_VERSION] == "RAW":
            return float(term_count_indexes[product_ID][feature_name][token])

        total_term_count = 0

        for indexed_token in term_count_indexes[product_ID][feature_name]:
            total_term_count += term_count_indexes[product_ID][feature_name][indexed_token]

        return float(term_count_indexes[product_ID][feature_name][token]/total_term_count)
    else:
        return float(1)

def compute_idf(feature_name, token, posting_indexes, term_count_indexes):
    if token in posting_indexes[feature_name]:
        idf = float(len(term_count_indexes) / len(posting_indexes[feature_name][token]))

        if IDF_VARIATIONS[IDF_VERSION] == "RAW":
            return idf

        return math.log(idf)
    else:
        return float(1)

def rank(posting_indexes, term_count_indexes, tokens, product_IDs):
    product_scores = {}
    for product_ID in product_IDs:
        product_scores[product_ID] = 1

    detail_scores = {}
    detail_scores["tf"] = {}
    detail_scores["idf"] = {}

    for feature in FEATURES:
        feature_name = feature["name"]

        detail_scores["idf"][feature_name]= {}
        detail_scores["tf"][feature_name] = {}

        for product_ID in product_IDs:
            detail_scores["tf"][feature_name][product_ID] = {}

    for feature in FEATURES:
        feature_name = feature["name"]

        for token in tokens:
            idf_score = compute_idf(feature_name, token, posting_indexes, term_count_indexes)
            detail_scores["idf"][feature_name][token] = idf_score

            for product_ID in product_IDs:
                tf_score = compute_tf(feature_name, product_ID, token, term_count_indexes)
                detail_scores["tf"][feature_name][product_ID][token] = tf_score

                product_scores[product_ID] = product_scores[product_ID] * tf_score * idf_score

    product_scores_list = []
    for product_ID in product_scores:
        product_scores_list.append((product_ID, product_scores[product_ID]))

    return sorted(product_scores_list, key=lambda x: x[1], reverse=True), detail_scores
