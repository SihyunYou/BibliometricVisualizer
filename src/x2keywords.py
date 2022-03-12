# x2keywords.py
# Trend of keywords from x(= years or journals)

from abstract_reader import *
from unigramer import Unigramer
from tqdm.auto import tqdm
from datetime import datetime
import os

def get_trend_of_keywords(_info_abstract, _level_stopwords, _n_keywords = 50):
    unigramer = Unigramer(_level_stopwords)
    dict_bow = {}

    for raw_abstract in tqdm([str(_info_abstract.df_abstract.iloc[i, 11]) for i in range(_info_abstract.df_abstract.shape[0])], desc = "BoW 생성 중(x2keywords)"):
        list_tokenized_unigram = unigramer.tokenize(raw_abstract)
        for unigram in list_tokenized_unigram:
            unigram = unigram.replace(',', '')
            if unigram in dict_bow:
                dict_bow[unigram] += 1
            else:
                dict_bow[unigram] = 1

    try:
        os.mkdir("report")
    except:
        pass
    with open("report/" + "analysis_x2k_freq_" + datetime.today().strftime("%Y%m%d%H%M%S") + ".csv", 'w', encoding='utf8') as f:
        list_bow = list(zip(dict_bow.keys(), dict_bow.values()))
        list_bow = sorted(list_bow, key = lambda x: x[1], reverse = True)
        for t in list_bow:
            f.write(str(t[0]) + '|' + str(t[1]))
            f.write('\n')
    
    return top_n_dict(dict_bow, _n_keywords)

def get_dict_term_fair_frequency(_info_abstract, _level_stopwords, _n_keywords = 50):
    unigramer = Unigramer(_level_stopwords)
    dict_term_fair_frequency = {}
    list_top_keywords = get_trend_of_keywords(_info_abstract, _level_stopwords, _n_keywords).keys()

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

    try:
        os.mkdir("report")
    except:
        pass
    with open("report/" + "analysis_x2k_cofreq_" + datetime.today().strftime("%Y%m%d%H%M%S") + ".csv", 'w', encoding='utf8') as f:
        list_bow = list(zip(dict_term_fair_frequency.keys(), dict_term_fair_frequency.values()))
        list_bow = sorted(list_bow, key = lambda x: x[1], reverse = True)
        for t in list_bow:
            f.write('|'.join(str(t[0]).split('**')))
            f.write('|')
            f.write(str(t[1]))
            f.write('\n')

    return dict_term_fair_frequency