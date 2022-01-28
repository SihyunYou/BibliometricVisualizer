from abstract_reader import *
import pandas

def substract_authors(_str_authors):
    list_authors = []
    p = _str_authors.count('\'')
    s, e = 0, 0
    for j in range(len(_str_authors)):
        if _str_authors[j] == '\'':
            if p % 2 == 0: s = j
            else: e = j
            p -= 1
        if s > 0 and e > 0:
            list_authors.append(_str_authors[s + 1:e - 1])
            s, e = 0, 0
        if p <= 0: break
    return list_authors

def get_trend_of_publication(_info_abstract):
    dict_n_author_publication = {}

    for n in range(_info_abstract.range_year[0], _info_abstract.range_year[1] + 1):
        df = _info_abstract.df_abstract.loc[_info_abstract.df_abstract["PY"] == str(n)]
        dict_authors = {}
        for i in range(df.shape[0]):
            for author in substract_authors(str(df.iloc[i, 3])):
                dict_authors[author] = 0
        dict_n_author_publication[n] = (len(dict_authors.keys()), df.shape[0])

    return [(n, dict_n_author_publication[n]) for n in range(_info_abstract.range_year[0], _info_abstract.range_year[1] + 1)]

