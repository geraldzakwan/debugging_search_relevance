from index import load_index
from preprocess import preprocess

# Will return product IDs using AND logic to aggregate results
# from various fields (feature is limited to string only)
def match(indexes, fields, search_terms):
    tokens = preprocess(search_terms)

    # Matching product IDs given a term (in respect to a certain field)
    matching_postings = []

    for token in tokens:
        for field in fields:
            if token in indexes[field]:
                matching_postings.append(set(indexes[field][token]))
            else:
                # Directly return an empty set when there is a term/token
                # that doesn't match any documents
                return set()

    result_sets = matching_postings[0]

    # Otherwise, get the intersection of all matching postings
    for posting in matching_postings:
        result_sets = result_sets.intersection(posting)

    return result_sets

if __name__ == '__main__':
    indexes = load_index()
    print(match(indexes, ["title", "desc"], "jual hp asus"))
