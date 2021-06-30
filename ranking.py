from config import FEATURES

def compute_tf(feature_name, product_ID, token, term_count_indexes):
    return 1

def compute_idf(feature_name, token, posting_indexes):
    if token in posting_indexes[feature_name]:
        return 1 / len(posting_indexes[feature_name][token])
    else:
        return 1

def rank(posting_indexes, term_count_indexes, tokens, product_IDs):
    product_scores = {}
    for product_ID in product_IDs:
        product_scores[product_ID] = 1

    for feature in FEATURES:
        feature_name = feature["name"]

        for token in tokens:
            idf_score = compute_idf(feature_name, token, posting_indexes)

            for product_ID in product_IDs:
                tf_score = compute_tf(feature_name, product_ID, token, term_count_indexes)

                product_scores[product_ID] = product_scores[product_ID] * tf_score * idf_score

    product_scores_list = []
    for product_ID in product_scores:
        product_scores_list.append((product_ID, product_scores[product_ID]))

    return sorted(product_scores_list, key=lambda x: x[1], reverse=True)
