# keyword2x.py
# x(= trend of years or journals) from a keyword

import journal_reader
import hierarchizer
import regularizer
from nltk.tokenize import word_tokenize

list_column = [10, 11] # TI, AB
def get_count_interesting_keyword(_df_journal, _interesting_keyword):
    count_interesting_keyword = 0
    is_hierarchical = hierarchizer.is_this_keyword_hierarchical(_interesting_keyword)
    breakable = False

    for i in range(_df_journal.shape[0]):
        if breakable: 
            breakable = False
            continue

        for n in list_column:
            if breakable: break
            list_tokenized_words = regularizer.apply_stopwords(word_tokenize(regularizer.regularize_abstract(_df_journal.iloc[i, n])))

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

def get_trend_of_years_from_keyword(_your_keyword, _start_year, _end_year):
    list_py = []
    for n in range(_start_year, _end_year + 1):
        c = get_count_interesting_keyword(journal_reader.df_journal.loc[journal_reader.df_journal["PY"] == str(n)], _your_keyword)
        list_py.append((n, c))
    return list_py

def get_trend_of_journals_from_keyword(_your_keyword, _n_journals):
    dict_so = {}
    for journal in journal_reader.list_interesting_journal:
        dict_so[journal] = get_count_interesting_keyword(journal_reader.df_journal.loc[journal_reader.df_journal["SO"] == journal], _your_keyword)
    return sorted(dict_so.items(), key = lambda item: item[1], reverse = True)[:_n_journals]