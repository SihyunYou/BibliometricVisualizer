# keyword2x.py
# x(= trend of years or journals) from a keyword

from abstract_reader import *
from hierarchizer import Hierarchizer
from tqdm.auto import tqdm

def get_keyword_interest(_df_abstract, _interesting_keyword):
    hierarchizer = Hierarchizer()
    is_hierarchical = hierarchizer.is_this_keyword_hierarchical(_interesting_keyword)
    frequency_integrity, frequency_keyword = 0, 0

    for raw_abstract in tqdm([str(_df_abstract.iloc[i, 11]) for i in range(_df_abstract.shape[0])], desc = "BoW 생성 중(keyword2x)"):
        list_tokenized_unigram = hierarchizer.tokenize(raw_abstract)
        frequency_integrity += len(list_tokenized_unigram)

        if is_hierarchical:
            for j in range(1, hierarchizer.MAX_LEN_WORD_GRAPH + 1):
                for k in range(len(list_tokenized_unigram) - j):
                    if hierarchizer.is_this_keyword_interesting(' '.join(list_tokenized_unigram[k:k+j])):
                        frequency_keyword += 1
        else:
             for k in range(len(list_tokenized_unigram) - _interesting_keyword.count(' ') + 1):
                 if ' '.join(list_tokenized_unigram[k:k+j]) == _interesting_keyword:
                     frequency_keyword += 1

    if frequency_integrity > 0:
        return frequency_keyword / frequency_integrity
    else: 
        return 0

def get_trend_of_years_from_keyword(_bibliometric_parameter, _your_keyword):
    df_abstract = _bibliometric_parameter.get_dataframe()
    return [(n, get_keyword_interest(df_abstract.loc[df_abstract["PY"] == str(n)], _your_keyword)) for n in range(_bibliometric_parameter.range_year[0], _bibliometric_parameter.range_year[1] + 1)]

def get_trend_of_journals_from_keyword(_bibliometric_parameter, _your_keyword):
    df_abstract = _bibliometric_parameter.get_dataframe()
    return sorted([(journal, get_keyword_interest(df_abstract.loc[df_abstract["SO"] == journal], _your_keyword)) for journal in df_abstract["SO"].unique()],
           key = lambda x: x[1],
           reverse = True)[:10]