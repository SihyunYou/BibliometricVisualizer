# x2keywords.py
# Trend of keywords from x(= years or journals)

from abstract_reader import df_abstract
import hierarchizer
from regularizer import preprocess_text
from tqdm import tqdm

def get_list_top_keywords(_document, _threshold):
    list_tokenized_words = preprocess_text(_document)
    word_to_index, bow = {}, []

    for word in tqdm(list_tokenized_words, desc = "BoW 생성 중"):
        if word not in word_to_index.keys():
            word_to_index[word] = len(word_to_index)
            bow.insert(len(word_to_index) - 1, 1)
        else:
            index = word_to_index.get(word)
            bow[index] += 1

    dict_word_count = {}
    for key, value in word_to_index.items():
        if(bow[value] >= _threshold):
            dict_word_count[key] = bow[value]

    return dict_word_count

def get_dict_term_fair_frequency(_column_name, _query):
    df = df_abstract.loc[df_abstract[_column_name] == _query]
    list_raw_document = [str(df.iloc[i, 11]) for i in range(df.shape[0])]
    list_tokenized_document = [preprocess_text(d) for d in list_raw_document]
    dict_word_count = get_list_top_keywords(' '.join(list_raw_document), 5)
    list_refined_keyword = []

    for keyword, frequency in dict_word_count.items():
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

def get_trend_of_keywords(_column_name, _query):
    df = df_abstract.loc[df_abstract[_column_name] == _query]
    return get_list_top_keywords(' '.join([str(df.iloc[i, 11]) for i in range(df.shape[0])]), 10)