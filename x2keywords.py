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
import networkx as nx
import operator

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

    list_keyword = get_list_top_keywords(whole_document, 10)[:200] # Renewable Energy -> 1103
    print(list_keyword)
    list_document_refined = []

    for i in tqdm(range(df_journal.shape[0]), desc = "텍스트 전처리 과정 진행 중"):
        document = str(df_journal.iloc[i, 11])
        list_tokenized_words = regularizer.apply_stopwords(word_tokenize(regularizer.regularize_abstract(document)))
        list_document_refined.append("")
        for j in range(1, N_GRAM + 1):
            for k in range(len(list_tokenized_words) - j):
                combined_words = ' '.join(list_tokenized_words[k:k+j])
                if combined_words in [t[0] for t in list_keyword]:
                    list_document_refined[-1] += combined_words + ' '

    #df_journal["_AB2"] = list_document_refined
    dict_term_fair_frequency = { }

    THRESHOLD_FREQUENCY = 80

    for i in tqdm(range(len(list_keyword)), desc = "단어쌍 빈도(TPF) 딕셔너리 구성 중"):
        for j in range(i + 1, len(list_keyword)):
            for k in range(len(list_document_refined)):
                if(list_document_refined[k].count(list_keyword[i][0]) > 0 and list_document_refined[k].count(list_keyword[j][0]) > 0):
                    key = list_keyword[i][0] + "**" + list_keyword[j][0]
                    if key in dict_term_fair_frequency:
                        dict_term_fair_frequency[key] += 1
                    else:
                        dict_term_fair_frequency[key] = 1
    
    print(dict_term_fair_frequency)
    G_centrality = nx.Graph()
    for term_fair, frequency in dict_term_fair_frequency.items():
        if frequency >= THRESHOLD_FREQUENCY:
            list_term = term_fair.split('**')
            G_centrality.add_edge(list_term[0], list_term[1], weight = frequency)
    
    dgr = nx.degree_centrality(G_centrality)        # 연결 중심성
    pgr = nx.pagerank(G_centrality)                 # 페이지 랭크

    sorted_dgr = sorted(dgr.items(), key=operator.itemgetter(1), reverse=True)
    sorted_pgr = sorted(pgr.items(), key=operator.itemgetter(1), reverse=True)

    G = nx.Graph()

    # 페이지 랭크에 따라 두 노드 사이의 연관성을 결정한다. (단어쌍의 연관성)
    # 연결 중심성으로 계산한 척도에 따라 노드의 크기가 결정된다. (단어의 등장 빈도수)
    for i in range(len(sorted_pgr)):
        G.add_node(sorted_pgr[i][0], nodesize=sorted_dgr[i][1])

    for term_fair, frequency in dict_term_fair_frequency.items():
        if frequency >= THRESHOLD_FREQUENCY:
            list_term = term_fair.split('**')
            G.add_weighted_edges_from([(list_term[0], list_term[1], frequency * 2)])

    sizes = [G.nodes[node]['nodesize'] * 1200 for node in G]

    import matplotlib.pyplot as plt
    options = {
        'edge_color': '#0099FF',
        'width': 1,
        'with_labels': True,
        'font_weight': 'regular',
    }
    nx.draw(G, node_size=sizes, pos=nx.spring_layout(G, k=3.5, iterations=100), **options)  # font_family로 폰트 등록
    ax = plt.gca()
    ax.collections[0].set_edgecolor("#0099FF")
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