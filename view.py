import json

from config import DATA_FILEPATH, INVERTED_INDEX_FILEPATH, FEATURES

def fetch(IDs):
    with open(DATA_FILEPATH, "r") as infile:
        data = json.load(infile)

    result = []
    for ID in IDs:
        result.append(data[ID])

    return result

if __name__ == '__main__':
    print(fetch(set(["10"])))
