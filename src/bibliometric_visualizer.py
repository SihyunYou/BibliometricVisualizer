# bibliometric_visualizer.py

import numpy
import matplotlib.pyplot as pyplot
import matplotlib.pylab as pylab
from datetime import datetime
import os

from abstract_reader import AbstractReader
import keyword2x
import x2keywords
import bibliometrics

class BibliometricVisualizer:
    def __init__(self, _info_abstract, _showed = False):
        self.width_title = 1.04
        self.bar_size = 0.2
        self.info_abstract = _info_abstract
        self.showed = _showed
        self.filename = ''

        try:
            os.mkdir("pic")
        except:
            pass

        pyplot.style.use("default")
        pylab.rcParams.update({
            'figure.figsize' : (15, 8),
            'legend.fontsize' : 13,
            'axes.labelsize' : 11,
            'axes.titlesize' : 22,
            'xtick.labelsize' : 10,
            'ytick.labelsize' : 12,
            'font.family' : 'Arial'})

    def get_palette_list(self, _from, _to, _n, reversed = True):
        list_palette = []
        for i in range(_n):
            str_rgb_hex = '#'
            for j in range(3):
                s = hex(int(_from[j] + i * (_to[j] - _from[j]) / _n))[2:]
                if len(s) == 1:
                    s = '0' + s
                str_rgb_hex += s
            list_palette.append(str_rgb_hex)

        if reversed:
            list_palette.reverse()
        return list_palette

    def ShowTrendOfYearsFromKeyword(self, _your_keyword):
        list_raw = keyword2x.get_trend_of_years_from_keyword(self.info_abstract, _your_keyword)
        n_xticks = self.info_abstract.range_year[1] - self.info_abstract.range_year[0] + 1
        print(list_raw)
        
        fig, ax = pyplot.subplots()
        ax.cla()
        ax.set_title('Trend of \'' + str(_your_keyword) + '\' keyword from ' + str(self.info_abstract.range_year[0]) + ' to ' + str(self.info_abstract.range_year[1]), y = self.width_title)
        ax.bar(numpy.arange(n_xticks), 
              [y[1] * 100 for y in list_raw], 
              width = 0.5, 
              color = self.get_palette_list([0x00, 0x66, 0x00], [0xCC, 0xFF, 0xCC], n_xticks), 
              label = "Proportion that the keyword occupies in n year")
        ax.legend(loc='upper right')   
        ax.set_xticks(numpy.arange(n_xticks), [x[0] for x in list_raw])
        ax.set_ylim(min([y[1] for y in list_raw]) * (1 - self.bar_size) * 100, max([y[1] for y in list_raw]) * (1 + self.bar_size) * 100)
        ax.set_yticklabels(['{:,.2%}'.format(x / 100) for x in ax.get_yticks()])

        if self.showed:
            pyplot.show()
        else:
            self.filename = datetime.today().strftime("%Y%m%d%H%M%S") + ".png"
            pyplot.savefig("pic/" + self.filename, dpi = 300)
        pyplot.cla()

    def ShowTrendOfJournalsFromKeyword(self, _your_keyword, _n_journals, _threshold_against_distortion):
        list_raw = keyword2x.get_trend_of_journals_from_keyword(self.info_abstract, _your_keyword, _n_journals, _threshold_against_distortion)
        n_xticks = len(list_raw)
        print(list_raw)

        fig, ax = pyplot.subplots()
        ax.cla()
        ax.set_title('Trend of \'' + str(_your_keyword) + '\' keyword in top ' + str(_n_journals) + ' journals', y = self.width_title)
        ax.bar(numpy.arange(n_xticks), 
              [x[1] * 100 for x in list_raw],
              width = 0.5,
              color = self.get_palette_list([0xCC, 0xFF, 0xCC], [0x00, 0x66, 0x00], _n_journals), 
              label = "Proportion that the keyword occupies in the journal")
        ax.legend(loc='upper right')   
        ax.set_xticks(numpy.arange(n_xticks), [x[0].replace(' ', '\n') for x in list_raw])
        ax.set_ylim(min([y[1] for y in list_raw]) * (1 - self.bar_size) * 100, max([y[1] for y in list_raw]) * (1 + self.bar_size) * 100)
        ax.set_yticklabels(['{:,.2%}'.format(x / 100) for x in ax.get_yticks()])
        
        if self.showed:
            pyplot.show()
        else:
            self.filename = datetime.today().strftime("%Y%m%d%H%M%S") + ".png"
            pyplot.savefig("pic/" + self.filename, dpi = 300)
        pyplot.cla()

    def ShowWordCloudOfKeywords(self, _level_stopwords, _n_keywords):
        dict_word_count = x2keywords.get_trend_of_keywords(self.info_abstract, _level_stopwords, _n_keywords)
        print(dict_word_count)

        from wordcloud import WordCloud
        word_cloud = WordCloud(background_color = "white", max_words = 100, width = 1000, height = 800).generate_from_frequencies(dict_word_count)
        pyplot.figure(figsize = (15, 15))
        pyplot.imshow(word_cloud)
        pyplot.axis('off')
        
        if self.showed:
            pyplot.show()
        else:
            self.filename = datetime.today().strftime("%Y%m%d%H%M%S") + ".png"
            pyplot.savefig("pic/" + self.filename, dpi = 300)
        pyplot.cla()

    def ShowNetworkOfKeywords(self, _level_stopwords, _n_keywords):
        dict_term_fair_frequency = x2keywords.get_dict_term_fair_frequency(self.info_abstract, _level_stopwords, _n_keywords)

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
        
        if self.showed:
            pyplot.show()
        else:
            self.filename = datetime.today().strftime("%Y%m%d%H%M%S") + ".png"
            pyplot.savefig("pic/" + self.filename, dpi = 300)
        pyplot.cla()

    def ShowBibliometrics(self):
        list_raw = bibliometrics.get_trend_of_publication(self.info_abstract)
        print(list_raw)

        fig, ax = pyplot.subplots()
        ax.cla()
        ax.set_title('Number of publications/authors from ' + str(self.info_abstract.range_year[0]) + ' to ' + str(self.info_abstract.range_year[1]), y = self.width_title)

        list_palette = self.get_palette_list([0xCC, 0xFF, 0xCC], [0x00, 0x66, 0x00], len(list_raw) - 1, False)
        for i in range(len(list_raw) - 1):
            ax.plot((list_raw[i][1][0], list_raw[i + 1][1][0]), (list_raw[i][1][1], list_raw[i + 1][1][1]), 
                     'o-',
                     color = list_palette[i])
        
        if self.showed:
            pyplot.show()
        else:
            self.filename = datetime.today().strftime("%Y%m%d%H%M%S") + ".png"
            pyplot.savefig("pic/" + self.filename, dpi = 300)
        pyplot.cla()