from index import load_posting_index

# Will return matched product IDs
# For a result to be retrieved, all search terms must be included
# in at least one of the fields (field is limited to string only)
def match(indexes, fields, tokens):
    # Matching product IDs given a term (in respect to a certain field)
    matching_postings = []

    for token in tokens:
        matching_postings_per_token = set()

        for field in fields:
            if token in indexes[field]:
                matching_postings_per_token = matching_postings_per_token.union(set(indexes[field][token]))

        # Directly return an empty set when there is a term/token
        # that doesn't match any field in any documents
        if len(matching_postings_per_token) == 0:
            return set()

        matching_postings.append(matching_postings_per_token)

    result_sets = matching_postings[0]

    # Otherwise, get the intersection of all matching postings
    for posting in matching_postings:
        result_sets = result_sets.intersection(posting)

    return result_sets

if __name__ == '__main__':
    indexes = load_posting_index()
    print(match(indexes, ["title", "desc"], "hp asus"))
