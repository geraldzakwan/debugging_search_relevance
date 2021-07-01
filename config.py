PORT = 8080
DEBUG = True

DATA_FILEPATH = "data/products.json"
INVERTED_INDEX_FILEPATH = "data/inverted_index"
TERM_COUNT_FILEPATH = "data/term_count_index"

STOPWORDS_FILEPATH = "data/preprocessing/stopwords.txt"
WORD_MAP_FILEPATH = "data/preprocessing/word_map.txt"

FEATURES = [
    {
        "name": "title",
        "type": "string"
    },
    {
        "name": "desc",
        "type": "string"
    }
]

TF_VARIATIONS = ["RAW", "FREQ"]
TF_VERSION = 0

IDF_VARIATIONS = ["RAW", "LOG"]
IDF_VERSION = 0

STOPWORDS = False
NORMALIZATION = False
