from regularizer import Regularizer
import spacy
import requests
import bs4
import pickle
import re
from tqdm import tqdm
import os 
import difflib
from spacy.lang.en.stop_words import STOP_WORDS

RELATIVE_PATH = ""

ws1 = STOP_WORDS
ws2 = [line.strip() for line in open(RELATIVE_PATH + "stopwords/stopwords_frequent.txt", 'r', encoding='UTF8')]
ws3 = ws2 + [line.strip() for line in open(RELATIVE_PATH + "stopwords/stopwords_expanded.txt", 'r', encoding='UTF8')]
list_stopwords = [ws1, ws2, ws3]
level_stopwords = 2

list_stopsigns = ['%', '±', '©', '°', '<', '>']
list_stoppos = ["PRON", "DET", "ADV", "SYM", "PART", "SPACE", "PUNCT", "NUM"]
list_revert_to_plural = ["datum"]
#os.system("python -m spacy download en_core_web_trf")
nlp = spacy.load('en_core_web_md')

URL_EN_WIKI = "https://en.wikipedia.org/wiki/"

class Unigramer(Regularizer):
    def __init__(self, _level_stopwords):
        self.level_stopwords = _level_stopwords

        try:
            with open("corpus_redirection.pickle","rb") as pf:
                self.dict_corpus_redirection = pickle.load(pf)
        except Exception as e:
            print(e)
            print("corpus_redirection does not exist.")
            self.dict_corpus_redirection = {}

    def __regularize_abstract(self, _abstract):
        p = re.compile(r'\([^)]*\)')
        return p.sub('', _abstract).replace('  ', ' ')

    def is_similar(self, _a, _b):
        _a = _a.lower()
        _b = _b.lower()
        for x in _a.split(' '):
            for y in _b.split(' '):
                if x == y: return True
        return False

    def is_unigram(self, _str):
        return _str.find(' ') == -1
    def put_unigram_to_list(self, _unigram):
        _unigram = _unigram.lower()
        if _unigram not in list_stopwords[self.level_stopwords - 1] and \
           _unigram not in self.list_modifier and \
           _unigram.split('-')[-1] not in self.list_modifier: # ngram은 명사구, 마지막 단어가 형용사로 끝나는 구는 제외
            self.list_unigram.append(_unigram)
    def put_ngram_to_list(self, _ngram):
        self.list_unigram.append(_ngram.lower())

    def get_redirected_term(self, _original_term):
        exception_code = ':( :('
        try:
            r = self.dict_corpus_redirection[_original_term]
            if r == exception_code:
                raise Exception()
            return r
        except:
            try:
                response = requests.get(URL_EN_WIKI + _original_term)
                if "Wikipedia does not have an article with this exact name." in response.text:
                    new_term = ''
                else:
                    new_term = bs4.BeautifulSoup(response.text, features="html.parser").title.text.split(' - ')[0]
        
                n = new_term.find('(')
                if n != -1:
                    new_term = new_term[:n - 1]

                if self.is_similar(_original_term, new_term) != True: # 최소한 원어휘와 리다이렉션 어휘 간 형태적으론 일치하는 부분이 있어야함
                    new_term = ''
                self.dict_corpus_redirection[_original_term] = new_term
                return new_term
            except:
                return exception_code

    def tokenize(self, _abstract):
        list_chunk = []
        self.list_modifier, self.list_unigram = [], []

        ab = self.__regularize_abstract(self._Preprocessor__correct_abstract_error(_abstract))
        #print(ab)
        document = nlp(ab)

        # Universal POS tags
        # https://universaldependencies.org/u/pos/
        for chunk in document.noun_chunks:
            list_token = []
            verb_delimiter = ''

            for i, token in enumerate(chunk):
                if token.pos_ not in list_stoppos and \
                   token.text not in list_stopsigns:
                    #print(token.text + " : " + token.pos_ + "(" + token.lemma_ + ")")
                    if token.pos_ == 'NOUN':
                        if token.lemma_ in list_revert_to_plural:
                            list_token.append(token.text)
                        else:
                            list_token.append(token.lemma_)
                    else:
                        list_token.append(token.text)
            
                    if token.pos_ == 'ADJ' or token.pos_ == 'VERB':
                        if token.text.lower() not in self.list_modifier:
                            self.list_modifier.append(token.text.lower())

                    if i > 0:
                        if (chunk[i - 1].pos_ == 'NOUN' or chunk[i - 1].pos_ == 'PROPN') and \
                            chunk[i].pos_ == 'VERB':
                            verb_delimiter = chunk[i].text
            if len(list_token) > 0:
                p = ' '.join(list_token)
                if verb_delimiter != '':
                    for q in p.split(' ' + verb_delimiter + ' '):
                        list_chunk.append(q)
                else:
                    list_chunk.append(p)
        #print(list_chunk)
        
        for chunk in tqdm(list_chunk):
            if self.is_unigram(chunk):
                self.put_unigram_to_list(chunk)
            else:
                list_token = chunk.split(' ')
                b = False
                for i in reversed(range(1, len(list_token))):
                    for j in reversed(range(len(list_token) - i)):
                        #print(list_token)
                        res = self.get_redirected_term(' '.join(list_token[j : i + j + 1]))
                        if res != '':
                            if self.is_unigram(res):
                                self.put_unigram_to_list(res)
                            else:
                                self.put_ngram_to_list(res)

                            del list_token[j : i + j + 1]
                            for token in list_token:
                                self.put_unigram_to_list(token)

                            b = True
                            break
                    if b: break
        
                if b != True:
                    for token in list_token:
                        self.put_unigram_to_list(token)

        with open("corpus_redirection.pickle","wb") as pf:
            pickle.dump(self.dict_corpus_redirection, pf)

        return self.list_unigram

#unigramer = Unigramer(3)
#s = unigramer.tokenize("advanced adsorption based osmotic heat engine")
#print(s)