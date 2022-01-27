# keyword2x.py
# x(= trend of years or journals) from a keyword

from abstract_reader import read_abstract
from hierarchizer import Hierarchizer
from tqdm import tqdm
import math

def get_count_interesting_keyword(_df_abstract, _interesting_keyword):
    hierarchizer = Hierarchizer()
    is_hierarchical = hierarchizer.is_this_keyword_hierarchical(_interesting_keyword)
    interest_score = 0

    for raw_abstract in tqdm([str(_df_abstract.iloc[i, 11]) for i in range(_df_abstract.shape[0])], desc = "BoW 생성 중(keyword2x)"):
        list_tokenized_unigram = hierarchizer.tokenize(raw_abstract)
        interest = 0
        if is_hierarchical:
            for j in range(1, hierarchizer.MAX_LEN_WORD_GRAPH + 1):
                for k in range(len(list_tokenized_unigram) - j):
                    if hierarchizer.is_this_keyword_interesting(' '.join(list_tokenized_unigram[k:k+j])):
                        interest += 1
        else:
             for k in range(len(list_tokenized_unigram) - _interesting_keyword.count(' ') + 1):
                 if ' '.join(list_tokenized_unigram[k:k+j]) == _interesting_keyword:
                     interest += 1
        if interest > 0:
            interest_score += round(math.log10(interest + 1) * 3.33, 2)

    return interest_score

def get_trend_of_years_from_keyword(_query, _range_year, _limit_journal, _your_keyword):
    df_abstract = read_abstract(_query, _limit_journal)
    return [(n, get_count_interesting_keyword(df_abstract.loc[df_abstract["PY"] == str(n)], _your_keyword)) for n in range(_range_year[0], _range_year[1] + 1)]

def get_trend_of_journals_from_keyword(_query, _range_year, _n_journals, _limit_journal, _your_keyword):
    df_abstract = read_abstract(_query, _limit_journal)
    return sorted([(journal, get_count_interesting_keyword(df_abstract.loc[(df_abstract["SO"] == journal) & (df_abstract["PY"].astype(int) >= _range_year[0]) & (df_abstract["PY"].astype(int) >= _range_year[0])], _your_keyword)) for journal in df_abstract["SO"].unique()],
           key = lambda x: x[1],
           reverse = True)[:10]