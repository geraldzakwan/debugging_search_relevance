PORT = 8080
DEBUG = True

DATA_FILEPATH = "data/products.json"
INVERTED_INDEX_FILEPATH = "data/inverted_index"
STOPWORDS_FILEPATH = "data/preprocessing/stopwords.txt"
WORD_MAP_FILEPATH = "data/preprocessing/word_map.txt"

FEATURES = [
    {
        "name": "title",
        "type": "string",
        "use": True
    },
    {
        "name": "desc",
        "type": "string",
        "use": True
    }
]

STOPWORDS = False
NORMALIZATION = False
