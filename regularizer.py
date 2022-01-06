import re
from nltk.corpus import stopwords

words2stop = stopwords.words('english')
for x in ['elsevier', 'using', 'used']:
    words2stop.append(x)

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
        if word not in words2stop:
            temps.append(word)
    return temps