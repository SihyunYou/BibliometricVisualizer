# bibliometric_visualizer.py

import numpy
import matplotlib.pyplot as pyplot
import matplotlib.pylab as pylab
from tqdm import tqdm

from abstract_reader import AbstractReader
import keyword2x
import x2keywords
import bibliometrics


pyplot.style.use("default")
y = 1.04

def get_palette_list(_from, _to, _n):
    list_palette = []
    for i in range(_n):
        str_rgb_hex = '#'
        for j in range(3):
            s = hex(int(_from[j] + i * (_to[j] - _from[j]) / _n))[2:]
            if len(s) == 1:
                s = '0' + s
            str_rgb_hex += s
        list_palette.append(str_rgb_hex)

    list_palette.reverse()
    return list_palette

pylab.rcParams.update({
            'figure.figsize' : (15, 8),
            'legend.fontsize' : 13,
            'axes.labelsize' : 12,
            'axes.titlesize' : 27,
            'xtick.labelsize' : 14,
            'ytick.labelsize' : 15,
            'font.family' : 'S-Core Dream'})

class BibliometricVisualizer:
    def __init__(self, _query, _range_year, _publication_name, _limit_journal = True):
        self.bar_size = 0.2
        self.bibliometric_parameter = AbstractReader(_query, _range_year, _publication_name, _limit_journal)

    def ShowTrendOfYearsFromKeyword(self, _your_keyword):
        n_xticks = self.bibliometric_parameter.range_year[1] - self.bibliometric_parameter.range_year[0] + 1
        list_raw = keyword2x.get_trend_of_years_from_keyword(self.bibliometric_parameter, _your_keyword)
        print(list_raw)
        
        fig, ax = pyplot.subplots()
        ax.cla()
        ax.set_title('Trend of \'' + str(_your_keyword) + '\' keyword from ' + str(self.bibliometric_parameter.range_year[0]) + ' to ' + str(self.bibliometric_parameter.range_year[1]), y = y)
        ax.bar(numpy.arange(n_xticks), 
              [y[1] * 100 for y in list_raw], 
              width = 0.5, 
              color = get_palette_list([0x00, 0x66, 0x00], [0xCC, 0xFF, 0xCC], n_xticks), 
              label = "Proportion that the keyword occupies in n year")
        ax.legend(loc='upper right')   
        ax.set_xticks(numpy.arange(n_xticks), [x[0] for x in list_raw])
        ax.set_ylim(min([y[1] for y in list_raw]) * (1 - self.bar_size) * 100, max([y[1] for y in list_raw]) * (1 + self.bar_size) * 100)
        ax.set_yticklabels(['{:,.2%}'.format(x / 100) for x in ax.get_yticks()])
        pyplot.show()

    def ShowTrendOfJournalsFromKeyword(self, _your_keyword, _n_journals):
        list_raw = keyword2x.get_trend_of_journals_from_keyword(self.bibliometric_parameter, _your_keyword, _n_journals)
        print(list_raw)
    
        max_y = max([x[1] for x in list_raw]) * 1.35
        max_y = max_y - max_y % 10
        yticks = max_y / 8 - (max_y / 8 % 10)

        fig, ax = pyplot.subplots()
        ax.cla()
        ax.set_title('Trend of \'' + str(_your_keyword) + '\' keyword in top ' + str(_n_journals) + ' journals', y = y)
        ax.bar(numpy.arange(_n_journals), 
              [x[1] for x in list_raw],
              width = 0.5,
              color = get_palette_list([0xCC, 0xFF, 0xCC], [0x00, 0x66, 0x00], _n_journals), 
              label = "Weighted score of keywords referred in the journal")
        ax.legend(loc='upper right')   
        ax.set_ylim(0, max_y)
        ax.set_xticks(numpy.arange(_n_journals), [x[0].replace(' ', '\n') for x in list_raw], fontsize = 11)
        pyplot.show()

    def ShowWordCloudOfKeywords(self, _n_keywords):
        dict_word_count = x2keywords.get_trend_of_keywords(self.bibliometric_parameter, _n_keywords)
        print(dict_word_count)

        from wordcloud import WordCloud
        word_cloud = WordCloud(background_color = "white", max_words = 100, width = 1000, height = 800).generate_from_frequencies(dict_word_count)
        pyplot.figure(figsize = (15, 15))
        pyplot.imshow(word_cloud)
        pyplot.axis('off')
        pyplot.show()

    def ShowNetworkOfKeywords(self, _n_keywords):
        dict_term_fair_frequency = x2keywords.get_dict_term_fair_frequency(self.bibliometric_parameter, _n_keywords)

        import networkx as nx
        import operator
        G_centrality = nx.Graph()
        for term_fair, frequency in dict_term_fair_frequency.items():
            list_term = term_fair.split('**')
            G_centrality.add_edge(list_term[0], list_term[1], weight = frequency)
    
        dgr = nx.degree_centrality(G_centrality) 
        pgr = nx.pagerank(G_centrality)     

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

        nx.draw(G, 
                with_labels = True, 
                node_size = [G.nodes[node]['nodesize'] * G.nodes[node]['nodesize'] * 3000 for node in G], 
                node_color = range(len(G)),
                width = 0.5, 
                edge_color = "grey", 
                alpha = 1,
                font_size = 9, 
                font_weight = "regular")
        ax = plt.gca()
        plt.show()

    def ShowBibliometrics(self):
        list_raw = bibliometrics.get_trend_of_publication(self.bibliometric_parameter)
        print(list_raw)

        fig, ax = pyplot.subplots()
        ax.cla()
        ax.set_title('Number of publications/authors from ' + str(self.range_year[0]) + ' to ' + str(self.range_year[1]), y = y)

        for i in range(len(list_raw) - 1):
            ax.plot((list_raw[i][1][0], list_raw[i + 1][1][0]), 
                     (list_raw[i][1][1], list_raw[i + 1][1][1]), 
                     'bo-')

        pyplot.show()