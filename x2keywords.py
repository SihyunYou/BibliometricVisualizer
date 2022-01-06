# x2keywords.py
# Trend of keywords from x(= years or journals)

import journal_reader
#import hierarchizer
import regularizer
from nltk.tokenize import word_tokenize

MAX_WORD_COUNT = 4

def make_bow(_document):
    list_tokenized_words = regularizer.apply_stopwords(word_tokenize(regularizer.regularize_abstract(_document)))
    word_to_index, bow = {}, []

    for j in range(1, MAX_WORD_COUNT + 1):
        for k in range(len(list_tokenized_words) - j):
            combined_words = ' '.join(list_tokenized_words[k:k+j])
            #hierarchizer.search_knowledge_hierarchy(combined_words)

            #if len(hierarchizer.list_searched) > 0:
            #    for searched_word in hierarchizer.list_searched:
            #        if searched_word not in word_to_index.keys():
            #            word_to_index[searched_word] = len(word_to_index)
            #            bow.insert(len(word_to_index) - 1, 1)
            #        else:
            #            index = word_to_index.get(searched_word)
            #            bow[index] += 1
            #elif j == 1:
            #    if combined_words not in word_to_index.keys():
            #        word_to_index[combined_words] = len(word_to_index)
            #        bow.insert(len(word_to_index) - 1, 1)
            #    else:
            #        index = word_to_index.get(combined_words)
            #        bow[index] += 1

            if combined_words not in word_to_index.keys():
                word_to_index[combined_words] = len(word_to_index)
                bow.insert(len(word_to_index) - 1, 1)
            else:
                index = word_to_index.get(combined_words)
                bow[index] += 1

            #hierarchizer.list_searched = []   
    return (word_to_index, bow)

def get_list_top_keywords(_document, _threshold):
    word_to_index, bow = make_bow(_document)
    dict_word_count = {}

    for key, value in word_to_index.items():
        if(bow[value] >= _threshold):
            dict_word_count[key] = bow[value]
    list_word_count_sorted = sorted(dict_word_count.items(), key = lambda item: item[1], reverse = True)

    return list_word_count_sorted

def get_trend_of_keywords_from_year(_remark_year):
    document_py = ""
    df_journal_py = journal_reader.df_journal.loc[journal_reader.df_journal["PY"] == str(_remark_year)]

    for i in range(df_journal_py.shape[0]):
        document_py += str(df_journal_py.iloc[i, 11]) + ' '
    return get_list_top_keywords(document_py, 10)

def get_trend_of_keywords_from_journal(_journal):
    # return하는 리스트 형식이 달라지므로 주의
    if _journal != "all":
        document_so = ""
        df_journal_so = journal_reader.df_journal.loc[journal_reader.df_journal["SO"] == _journal]
        for i in range(df_journal_so.shape[0]):
            document_so += str(df_journal_so.iloc[i, 11]) + ' '
    
        return get_list_top_keywords(document_so)
    else:
        list_so = []
        for journal in journal_reader.list_interesting_journal:
             document_so = ""
             df_journal_so = journal_reader.df_journal.loc[journal_reader.df_journal["SO"] == journal]
             for i in range(df_journal_so.shape[0]):
                 document_so += str(df_journal_so.iloc[i, 11]) + ' '
    
             list_top_keywords = get_list_top_keywords(document_so)
             list_so.append((journal, list_top_keywords))

        return list_so