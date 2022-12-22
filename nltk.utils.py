import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

def tokenize(sentences):
    """
    Split sentences into array of words / tokens
    a token can be word or punctuation character or number
    """
    return nltk.word_tokenize(sentences)

def stem(word):
    """
    stemming = find the root form of the word
    examples :
    words = ["organize","organizes","organizzing"]
    words = [stem(w) for w in words]
    -> ["organ","organ","organ"]
    """
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence,words):
    """
    return bag of words array:
    1 for each known word that exists in the sentence, 0 otherwise
    Example
    sentences = ["hello","how","are","you"]
    words = ["Hi","hello","I","you","bye","thank","cool"]
    bog = [0, 1, 0, 1, 0, 0, 0]
    """
    # stem each word
    sentence_words = [stem(word) for word in tokenized_sentence]
    # init bag with - for each word
    bag = np.zeros(len(words),dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words:
            bag[idx] = 1
    return bag
