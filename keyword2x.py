# keyword2x.py
# x(= trend of years or journals) from a keyword

from abstract_reader import read_abstract
import hierarchizer
from regularizer import preprocess_text_no_unigram

list_column = [10, 11] # TI, AB
def get_count_interesting_keyword(_df_abstract, _interesting_keyword):
    count_interesting_keyword = 0
    is_hierarchical = hierarchizer.is_this_keyword_hierarchical(_interesting_keyword)
    breakable = False

    for i in range(_df_abstract.shape[0]):
        if breakable: 
            breakable = False
            continue

        for n in list_column:
            if breakable: break
            list_tokenized_words = preprocess_text_no_unigram(_df_abstract.iloc[i, n])

            if is_hierarchical:
                for j in range(1, hierarchizer.MAX_LEN_WORD_GRAPH + 1):
                    if breakable: break
                    for k in range(len(list_tokenized_words) - j):
                        combined_words = ' '.join(list_tokenized_words[k:k+j])
                        hierarchizer.search_knowledge_hierarchy(combined_words)

                        is_this_keyword_interested = _interesting_keyword in hierarchizer.list_searched
                        hierarchizer.list_searched = []

                        if is_this_keyword_interested:
                            count_interesting_keyword += 1
                            breakable = True
                            break
            else:
                 j = _interesting_keyword.count(' ') + 1
                 for k in range(len(list_tokenized_words) - j):
                     combined_words = ' '.join(list_tokenized_words[k:k+j])
                     if combined_words == _interesting_keyword:
                         count_interesting_keyword += 1
                         breakable = True
                         break

    return count_interesting_keyword

def get_trend_of_years_from_keyword(_query, _limit_journal, _your_keyword, _start_year, _end_year):
    df_abstract = read_abstract(_query, _limit_journal)
    return [(n, get_count_interesting_keyword(df_abstract.loc[df_abstract["PY"] == str(n)], _your_keyword)) for n in range(_start_year, _end_year + 1)]

def get_trend_of_journals_from_keyword(_query, _limit_journal, _your_keyword, _n_journals):
    df_abstract = read_abstract(_query, _limit_journal)
    return sorted([(journal, get_count_interesting_keyword(df_abstract.loc[df_abstract["SO"] == journal], _your_keyword)) for journal in df_abstract["SO"].unique()],
           key = lambda x: x[1],
           reverse = True)[:_n_journals]