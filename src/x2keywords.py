# x2keywords.py
# Trend of keywords from x(= years or journals)

from abstract_reader import *
from unigramer import Unigramer
from tqdm.auto import tqdm

def top_n_dict(_dict, _threshold = 100):
    value = sorted(_dict.values(), reverse = True)[_threshold]
    list_key_delete = []
    for key in _dict:
        if _dict[key] < value:
            list_key_delete.append(key)
    for key in list_key_delete:
        del _dict[key]
    return _dict

def get_trend_of_keywords(_info_abstract, _n_keywords = 50):
    unigramer = Unigramer()
    dict_bow = {}

    for raw_abstract in tqdm([str(_info_abstract.df_abstract.iloc[i, 11]) for i in range(_info_abstract.df_abstract.shape[0])], desc = "BoW 생성 중(x2keywords)"):
        list_tokenized_unigram = unigramer.tokenize(raw_abstract)
        for unigram in list_tokenized_unigram:
            if unigram in dict_bow:
                dict_bow[unigram] += 1
            else:
                dict_bow[unigram] = 1

    return top_n_dict(dict_bow, _n_keywords)

def get_dict_term_fair_frequency(_info_abstract, _n_keywords = 50):
    unigramer = Unigramer()
    dict_term_fair_frequency = {}
    list_top_keywords = get_trend_of_keywords(_info_abstract, _n_keywords).keys()

    for raw_abstract in tqdm([str(_info_abstract.df_abstract.iloc[i, 11]) for i in range(_info_abstract.df_abstract.shape[0])], desc = "단어쌍 빈도(TPF) 딕셔너리 구성 중"):
        list_tokenized_unigram = unigramer.tokenize(raw_abstract)
        for i in range(len(list_tokenized_unigram)):
            for j in range(i + 1, len(list_tokenized_unigram)):
                if list_tokenized_unigram[i] == list_tokenized_unigram[j]:
                    continue
                if list_tokenized_unigram[i] not in list_top_keywords or \
                    list_tokenized_unigram[j] not in list_top_keywords:
                    continue

                key = list_tokenized_unigram[i] + "**" + list_tokenized_unigram[j]
                if key in dict_term_fair_frequency:
                    dict_term_fair_frequency[key] += 1
                else:
                    dict_term_fair_frequency[key] = 1

    print(dict_term_fair_frequency)
    return dict_term_fair_frequency