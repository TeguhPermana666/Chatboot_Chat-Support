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
    """