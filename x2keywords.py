# x2keywords.py
# Trend of keywords from x(= years or journals)

import abstract_reader
import hierarchizer
from regularizer import preprocess_text
import numpy
from nltk.tokenize import word_tokenize
from tqdm import tqdm

def make_bow(_document):
    list_tokenized_words = preprocess_text(_document)
    word_to_index, bow = {}, []

    for word in tqdm(list_tokenized_words, desc = "BoW 생성 중"):
        if word not in word_to_index.keys():
            word_to_index[word] = len(word_to_index)
            bow.insert(len(word_to_index) - 1, 1)
        else:
            index = word_to_index.get(word)
            bow[index] += 1
    return (word_to_index, bow)

def get_list_top_keywords(_document, _threshold):
    word_to_index, bow = make_bow(_document)
    dict_word_count = {}

    for key, value in word_to_index.items():
        if(bow[value] >= _threshold):
            dict_word_count[key] = bow[value]
    list_word_count_sorted = sorted(dict_word_count.items(), key = lambda item: item[1], reverse = True)

    return list_word_count_sorted

def get_dict_term_fair_frequency(_column_name, _query):
    df_extracted_abstract = abstract_reader.df_abstract.loc[abstract_reader.df_abstract[_column_name] == _query]
    list_raw_document = [str(df_extracted_abstract.iloc[i, 11]) for i in range(df_extracted_abstract.shape[0])]
    list_tokenized_document = [preprocess_text(d) for d in list_raw_document]
    list_keyword = get_list_top_keywords(' '.join(list_raw_document), 5)
    list_refined_keyword = []

    for keyword, frequency in list_keyword:
        if keyword in hierarchizer.dict_unigram.values():
            if frequency >= 5:
                list_refined_keyword.append(keyword)
        else:
            if frequency >= 50:
                list_refined_keyword.append(keyword)
    print(list_refined_keyword)

    dict_term_fair_frequency = { }
    for i in tqdm(range(len(list_refined_keyword)), desc = "단어쌍 빈도(TPF) 딕셔너리 구성 중"):
        for j in range(i + 1, len(list_refined_keyword)):
            for document in list_tokenized_document:
                if(list_refined_keyword[i] in document and list_refined_keyword[j] in document):
                    key = (list_refined_keyword[i] + "**" + list_refined_keyword[j]).replace('_', '\n')
                    if key in dict_term_fair_frequency:
                        dict_term_fair_frequency[key] += 1
                    else:
                        dict_term_fair_frequency[key] = 1
    print(dict_term_fair_frequency)

    return dict_term_fair_frequency

def get_trend_of_keywords_from_year(_remark_year):
    document_py = ""
    df_abstract_py = abstract_reader.df_abstract.loc[abstract_reader.df_abstract["PY"] == str(_remark_year)]

    for i in range(df_abstract_py.shape[0]):
        document_py += str(df_abstract_py.iloc[i, 11]) + ' '
    return get_list_top_keywords(document_py, 10)

def get_trend_of_keywords_from_journal(_journal):
    # return하는 리스트 형식이 달라지므로 주의
    if _journal != "all":
        document_so = ""
        df_abstract_so = abstract_reader.df_abstract.loc[abstract_reader.df_abstract["SO"] == _journal]
        for i in range(df_abstract_so.shape[0]):
            document_so += str(df_abstract_so.iloc[i, 11]) + ' '
    
        return get_list_top_keywords(document_so)
    else:
        list_so = []
        for journal in abstract_reader.list_interesting_journal:
             document_so = ""
             df_abstract_so = abstract_reader.df_abstract.loc[abstract_reader.df_abstract["SO"] == journal]
             for i in range(df_abstract_so.shape[0]):
                 document_so += str(df_abstract_so.iloc[i, 11]) + ' '
    
             list_top_keywords = get_list_top_keywords(document_so)
             list_so.append((journal, list_top_keywords))

        return list_so