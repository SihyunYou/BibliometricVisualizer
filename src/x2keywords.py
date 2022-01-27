# x2keywords.py
# Trend of keywords from x(= years or journals)

from abstract_reader import read_abstract
from unigramer import Unigramer
from tqdm import tqdm
    
def cut_dict(_dict, _threshold = 10):
    for key in _dict:
        if _dict[key] < _threshold:
            del _dict[key]
    return _dict

def substract_df_abstract(_query, _range_year, _publication_name, _limit_journal):
    df_abstract = read_abstract(_query, _limit_journal)
    df_abstract = df_abstract.loc[\
        (df_abstract["PY"].astype(int) >= _range_year[0]) &\
        (df_abstract["PY"].astype(int) >= _range_year[0]) &\
        (df_abstract["SO"] == _publication_name)]
    return df_abstract

def get_trend_of_keywords(_query, _range_year, _publication_name, _limit_journal):
    unigramer = Unigramer()
    dict_bow = {}
    df_abstract = substract_df_abstract(_query, _range_year, _publication_name, _limit_journal)

    for raw_abstract in tqdm([str(df_abstract.iloc[i, 11]) for i in range(df_abstract.shape[0])], desc = "BoW 생성 중(x2keywords)"):
        list_tokenized_unigram = unigramer.tokenize(raw_abstract)
        for unigram in list_tokenized_unigram:
            if unigram in dict_bow:
                dict_bow[unigram] += 1
            else:
                dict_bow[unigram] = 1

    return cut_dict(dict_bow)

def get_dict_term_fair_frequency(_query, _range_year, _publication_name, _limit_journal):
    unigramer = Unigramer()
    dict_term_fair_frequency = {}
    df_abstract = substract_df_abstract(_query, _range_year, _publication_name, _limit_journal)

    for raw_abstract in tqdm([str(df_abstract.iloc[i, 11]) for i in range(df_abstract.shape[0])], desc = "단어쌍 빈도(TPF) 딕셔너리 구성 중"):
        list_tokenized_unigram = unigramer.tokenize(raw_abstract)
        for i in range(len(list_tokenized_unigram)):
            for j in range(i + 1, len(list_tokenized_unigram)):
                key = list_tokenized_unigram[i] + "**" + list_tokenized_unigram[j]
                if key in dict_term_fair_frequency:
                    dict_term_fair_frequency[key] += 1
                else:
                    dict_term_fair_frequency[key] = 1

    return cut_dict(dict_term_fair_frequency)