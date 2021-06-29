from config import STOPWORDS_FILEPATH, WORD_MAP_FILEPATH, STOPWORDS, NORMALIZATION

def lowercase(sent):
    return sent.lower()

def tokenize(sent):
    return sent.split(" ")

def remove_stopwords(tokens):
    with open(STOPWORDS_FILEPATH, "r") as infile:
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
    with open(WORD_MAP_FILEPATH, "r") as infile:
        pairs = infile.readlines()

    word_map = {}
    for pair in pairs:
        word, normalized_word = pair.strip("\n").split(" ")

        word_map[word] = normalized_word

    cleaned_tokens = []
    for token in tokens:
        if token in word_map:
            cleaned_tokens.append(word_map[token])
        else:
            cleaned_tokens.append(token)

    return cleaned_tokens

def preprocess(sent):
    tokens = tokenize(lowercase(sent))

    if NORMALIZATION:
        tokens = normalize(tokens)

    if STOPWORDS:
        tokens = remove_stopwords(tokens)

    return tokens

if __name__ == '__main__':
    print(preprocess("jual hp asis"))
