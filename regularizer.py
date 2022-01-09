import re
import nltk
from nltk.tokenize import word_tokenize
import hierarchizer
from nltk.corpus import wordnet as wn

nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

words2stop = [line.strip() for line in open("stopword.txt", 'r')]

re1 = re.compile('[^A-Za-z0-9]+')
re2 = re.compile('&')
def regularize_publication_name(_str):
    return re1.sub('', re2.sub('and', str(_str))).lower()
re3 = re.compile('[^a-z-/\s]+')
def regularize_abstract(_str):
    return re3.sub('', str(_str).lower())

def apply_stopwords(_list_tokenized_words):
    temps = []
    for word in _list_tokenized_words:
        if word not in words2stop and len(word) >= 3:
            temps.append(word)
    return temps

def preprocess_text(_text):
    list_tokenized_words = hierarchizer.replace_synonym(word_tokenize(regularize_abstract(_text)))
    tokens_pos = nltk.pos_tag(list_tokenized_words)
    NN_words, list_specific_unigram = [], []
    for word, pos in tokens_pos:
        if word in hierarchizer.dict_unigram.values():
            list_specific_unigram.append(word)
        elif 'NN' in pos:
            NN_words.append(word)

    wlem = nltk.WordNetLemmatizer()
    lemmatized_words = []
    for word in NN_words:
        new_word = wlem.lemmatize(word, 'n')
        lemmatized_words.append(new_word)

    return apply_stopwords(lemmatized_words + list_specific_unigram)