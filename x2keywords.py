# x2keywords.py
# Trend of keywords from x(= years or journals)

import journal_reader
#import hierarchizer
import regularizer
import numpy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from nltk.tokenize import word_tokenize
from tqdm import tqdm

N_GRAM = 4

def make_bow(_document):
    list_tokenized_words = regularizer.apply_stopwords(word_tokenize(regularizer.regularize_abstract(_document)))
    word_to_index, bow = {}, []

    for j in range(1, N_GRAM + 1):
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


def make_dtm():
    whole_document = ""
    df_journal = journal_reader.df_journal.loc[journal_reader.df_journal["SO"] == "Renewable Energy"]
    for i in range(df_journal.shape[0]):
        whole_document += str(df_journal.iloc[i, 11]) + ' '

    list_keywords = get_list_top_keywords(whole_document, 10)
    list_document_refined = []

    for i in tqdm(range(df_journal.shape[0])):
        document = str(df_journal.iloc[i, 11])
        list_tokenized_words = regularizer.apply_stopwords(word_tokenize(regularizer.regularize_abstract(document)))
        list_document_refined.append("")
        for j in range(1, N_GRAM + 1):
            for k in range(len(list_tokenized_words) - j):
                combined_words = ' '.join(list_tokenized_words[k:k+j])
                if combined_words in [t[0] for t in list_keywords]:
                    list_document_refined[-1] += combined_words + ' '

    df_journal["_AB2"] = list_document_refined
    tfidf_vectorizer = TfidfVectorizer(min_df = 2, ngram_range=(1,5))
    tfidf_vectorizer.fit(list_document_refined)
    print(sorted(tfidf_vectorizer.vocabulary_.items()))
    vector = tfidf_vectorizer.transform(list_document_refined).toarray()
    vector = numpy.array(vector) 
    model = DBSCAN(eps=0.7, min_samples=4, metric = "cosine") # eps가 클수록 min_samples가 작을수록 노이즈 데이터 작아짐
    result = model.fit_predict(vector)
    df_journal["_CN"] = result 
    for cluster_num in set(result):
        if(cluster_num == -1 or cluster_num == 0): 
            continue
        else:
            print("cluster num : {}".format(cluster_num))
            temp_df = df_journal[df_journal['_CN'] == cluster_num] 
            for title in temp_df['TI']:
                print(title) 
            print()


make_dtm()
exit(1)
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