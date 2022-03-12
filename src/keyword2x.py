# keyword2x.py
# x(= trend of years or journals) from a keyword

from abstract_reader import *
from hierarchizer import Hierarchizer
from tqdm.auto import tqdm
from datetime import datetime
import os 

def get_keyword_interest(_df_abstract, _interesting_keyword):
    hierarchizer = Hierarchizer()
    is_hierarchical = hierarchizer.is_this_keyword_hierarchical(_interesting_keyword)
    frequency_integrity, frequency_keyword = 0, 0

    for raw_abstract in tqdm([str(_df_abstract.iloc[i, 11]) for i in range(_df_abstract.shape[0])], desc = "BoW 생성 중(keyword2x)"):
        list_tokenized_unigram = hierarchizer.tokenize(raw_abstract)
        frequency_integrity += len(list_tokenized_unigram)

        if is_hierarchical:
            for j in range(1, hierarchizer.MAX_LEN_WORD_GRAPH + 1):
                for k in range(len(list_tokenized_unigram) - j - 1):
                    if hierarchizer.is_this_keyword_interesting(' '.join(list_tokenized_unigram[k:k+j])):
                        frequency_keyword += 1
        else:
            for j in range(1, _interesting_keyword.count(' ') + 2):
                for k in range(len(list_tokenized_unigram) - j - 1):
                    if ' '.join(list_tokenized_unigram[k:k+j]) == _interesting_keyword:
                        frequency_keyword += 1
    
    proportion = 0
    if frequency_integrity > 0:
        proportion = frequency_keyword / frequency_integrity
    return (proportion, frequency_keyword, frequency_integrity)

def get_trend_of_years_from_keyword(_info_abstract, _your_keyword):
    list_raw = [[n, get_keyword_interest(_info_abstract.df_abstract.loc[_info_abstract.df_abstract["PY"] == str(n)], _your_keyword)] \
                for n in range(_info_abstract.range_year[0], _info_abstract.range_year[1] + 1)]
    try:
        os.mkdir("report")
    except:
        pass
    with open("report/" + "analysis_k2x_year_" + datetime.today().strftime("%Y%m%d%H%M%S") + ".csv", 'w', encoding='utf8') as f:
        list_proportion = [list_raw[n][1] for n in range(len(list_raw))]
        list_rank = [len(list_proportion) - sorted(list_proportion).index(x) for x in list_proportion]
        for i, t in enumerate(list_raw):
            f.write(str(t[0]))
            f.write('|')
            f.write('|'.join([str(k) for k in t[1]]))
            f.write('|')
            f.write(str(_info_abstract.df_abstract.loc[_info_abstract.df_abstract["PY"] == str(t[0])].shape[0]))
            f.write('|')
            f.write(str(list_rank[i]))
            f.write('\n')

    return list_raw

def get_trend_of_journals_from_keyword(_info_abstract, _your_keyword, _n_journals, _threshold_against_distortion):
    list_raw = sorted([(journal, 
                        get_keyword_interest(_info_abstract.df_abstract.loc[_info_abstract.df_abstract["SO"] == journal], _your_keyword)) \
                        for journal in _info_abstract.df_abstract["SO"].unique()],
                        key = lambda x: x[1][0],
                        reverse = True)
    try:
        os.mkdir("report")
    except:
        pass
    with open("report/" + "analysis_k2x_journal_" + datetime.today().strftime("%Y%m%d%H%M%S") + ".csv", 'w', encoding='utf8') as f:
        list_proportion = [list_raw[n][1] for n in range(len(list_raw))]
        list_rank = [len(list_proportion) - sorted(list_proportion).index(x) for x in list_proportion]
        for i, t in enumerate(list_raw):
            f.write(str(t[0]))
            f.write('|')
            f.write('|'.join([str(k) for k in t[1]]))
            f.write('|')
            f.write(str(_info_abstract.df_abstract.loc[_info_abstract.df_abstract["SO"] == str(t[0])].shape[0]))
            f.write('|')
            f.write(str(list_rank[i]))
            f.write('\n')

    return sorted([(journal, 
                    get_keyword_interest(_info_abstract.df_abstract.loc[_info_abstract.df_abstract["SO"] == journal], _your_keyword)) \
                    for journal in _info_abstract.df_abstract["SO"].unique()
                    if _info_abstract.df_abstract.loc[_info_abstract.df_abstract["SO"] == journal].shape[0] >= _threshold_against_distortion],
            key = lambda x: x[1][0],
            reverse = True)[:_n_journals]