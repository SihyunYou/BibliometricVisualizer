# x2keywords.py
# Trend of keywords from x(= years or journals)

import journal_reader
import hierarchizer
from hierarchizer import N_GRAM
from regularizer import preprocess_text
import numpy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from nltk.tokenize import word_tokenize
from tqdm import tqdm
import networkx as nx
import operator

def make_bow(_document):
    list_tokenized_words = preprocess_text(_document)
    word_to_index, bow = {}, []

    for word in list_tokenized_words:
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

def make_dtm():
    whole_document = ""
    df_journal = journal_reader.df_journal.loc[journal_reader.df_journal["SO"] == "Renewable Energy"]
    for i in range(df_journal.shape[0]):
        whole_document += str(df_journal.iloc[i, 11]) + ' '

    list_keyword = get_list_top_keywords(whole_document, 5)
    list_refined_keyword = []
    for keyword, frequency in list_keyword:
        if keyword in hierarchizer.dict_unigram.values():
            if frequency >= 5:
                list_refined_keyword.append(keyword)
        else:
            if frequency >= 50:
                list_refined_keyword.append(keyword)
    print(list_refined_keyword)

    list_tokenized_document = []
    for i in tqdm(range(df_journal.shape[0]), desc = "텍스트 전처리 과정 진행 중"):
        document = str(df_journal.iloc[i, 11])
        list_tokenized_words = []
        for word in preprocess_text(document):
            if word in list_refined_keyword:
                list_tokenized_words.append(word)
        list_tokenized_document.append(list_tokenized_words)
    #print(list_tokenized_document)

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

    G_centrality = nx.Graph()
    for term_fair, frequency in dict_term_fair_frequency.items():
        list_term = term_fair.split('**')
        G_centrality.add_edge(list_term[0], list_term[1], weight = frequency)
    
    dgr = nx.degree_centrality(G_centrality)        # 연결 중심성
    pgr = nx.pagerank(G_centrality)                 # 페이지 랭크

    sorted_dgr = sorted(dgr.items(), key=operator.itemgetter(1), reverse=True)
    sorted_pgr = sorted(pgr.items(), key=operator.itemgetter(1), reverse=True)
    
    G = nx.Graph()
    for i in range(len(sorted_pgr)):
        G.add_node(sorted_pgr[i][0], nodesize = sorted_dgr[i][1])

    for term_fair, frequency in dict_term_fair_frequency.items():
        list_term = term_fair.split('**')
        G.add_weighted_edges_from([(list_term[0], list_term[1], frequency)])

    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm

    nx.draw(G, with_labels=True, 
            node_size = [G.nodes[node]['nodesize'] * G.nodes[node]['nodesize'] * 3000 for node in G], 
            node_color= range(len(G)), width=0.5, edge_color="grey", alpha=0.8,
            font_size = 8, font_weight="regular")
    ax = plt.gca()
    plt.show()

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