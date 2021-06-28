from config import STOPWORDS_FILEPATH
from toggle import STOPWORDS, NORMALIZATION

def lowercase(sent):
    return sent.lower()

def tokenize(sent):
    return sent.split(" ")

def remove_stopwords(tokens):
    with open(STOPWORD_FILEPATH, "r") as infile:
        stopwords = infile.readlines()

    stopwords_set = set()
    for stopword in stopwords:
        stopwords_set.add(stopword.strip("\n"))

    cleaned_tokens = []
    for token in tokens:
        if not token in stopwords_set:
            cleaned_tokens.append(token)

    return cleaned_tokens

def normalize(tokens):
    pass

def preprocess(sent):
    tokens = tokenize(lowercase(sent))

    if STOPWORDS:
        tokens = remove_stopwords(tokens)

    if NORMALIZATION:
        pass

    return tokens

if __name__ == '__main__':
    preprocess("jual hp asus")
