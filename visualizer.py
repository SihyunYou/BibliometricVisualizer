# keyword_trend_visualiser.py

import numpy
import matplotlib.pyplot as pyplot
import matplotlib.pylab as pylab
import keyword2x
import x2keywords
from tqdm import tqdm

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

def ShowTrendOfYearsFromKeyword(_your_keyword, _start_year, _end_year):
    list_raw = keyword2x.get_trend_of_years_from_keyword(_your_keyword, _start_year, _end_year)
    print(list_raw)
    
    n = 3
    list_sma = []
    for i in range(len(list_raw) - n + 1):
        s = 0
        for j in range(n):
            s += list_raw[i + j][1]
        list_sma.append(s / n)

    max_y = max([x[1] for x in list_raw]) * 1.35
    max_y = max_y - max_y % 10
    n_xticks = _end_year - _start_year + 1
    fig, ax = pyplot.subplots()
    ax.cla()
    ax.set_title('Trend of \'' + str(_your_keyword) + '\' keyword from ' + str(_start_year) + ' to ' + str(_end_year), y = y)
    #ax.plot(numpy.arange(n - 1, n_xticks), 
    #       list_sma,   
    #       'o-', 
    #       label = 'Simple moving average')
    ax.bar(numpy.arange(n_xticks), 
           [x[1] for x in list_raw], 
           width = 0.5, 
           color = get_palette_list([0x00, 0x66, 0x00], [0xCC, 0xFF, 0xCC], n_xticks), 
           label = "Number of keywords referred in n year")
    ax.legend(loc='upper right')   
    ax.set_ylim(0, max_y)
    ax.set_yticks(numpy.arange(0, max_y + 10, 10))
    ax.set_xticks(numpy.arange(n_xticks), [x[0] for x in list_raw])
    pyplot.show()

def ShowFluctuationOfKeywords(_list_your_keyword, _remark_year, _end_year):
    list_fluctuation = []
    n = 3
    sn = n * (n - 1) / 2

    for your_keyword in tqdm(_list_your_keyword):
        list_raw = keyword2x.get_trend_of_years_from_keyword(your_keyword, _remark_year - n + 1, _end_year)
        f, g = 0, 0
        for i in range(n):
            f += list_raw[i][1] * (i + 1)
            g += list_raw[-i][1] * (n - i)
        list_fluctuation.append(round((g - f) / sn, 0))

    print(list_fluctuation)

    list_sorted = [(_list_your_keyword[i], list_fluctuation[i]) for i in range(len(list_fluctuation))]
    list_sorted.sort(key = lambda x : x[1])

    max_y = max([x for x in list_fluctuation]) * 1.35
    max_y = max_y - max_y % 10
    n_xticks = len(list_fluctuation)
    fig, ax = pyplot.subplots()
    ax.cla()
    ax.set_title('Fluctuation of keywords from ' + str(_remark_year) + ' to ' + str(_end_year), y = y)
    ax.bar(numpy.arange(n_xticks), 
           [x[1] for x in list_sorted], 
           width = 0.5, 
           color = get_palette_list([0x00, 0x66, 0x00], [0xCC, 0xFF, 0xCC], n_xticks), 
           label = "WMA(" + str(_end_year) + ") - WMA(" + str(_remark_year) + ")\n* Weighted moving average")
    ax.legend(loc='upper right')   
    ax.set_ylim(0, max_y)
    ax.set_yticks(numpy.arange(0, max_y + 10, 10))
    ax.set_xticks(numpy.arange(len(_list_your_keyword)), [x[0].replace(' ', '\n') for x in list_sorted], fontsize = 14)
    pyplot.show()

def ShowTrendOfJournalsFromKeyword(_your_keyword, _n_journals):
    list_raw = keyword2x.get_trend_of_journals_from_keyword(_your_keyword, _n_journals)
    print(list_raw)
    list_raw.reverse()
    
    max_y = max([x[1] for x in list_raw]) * 1.35
    max_y = max_y - max_y % 10
   
    fig, ax = pyplot.subplots()
    ax.cla()
    ax.set_title('Trend of \'' + str(_your_keyword) + '\' keyword in top ' + str(_n_journals) + ' journals', y = y)
    ax.bar(numpy.arange(_n_journals), 
           [x[1] for x in list_raw],
           width = 0.5, 
           color = get_palette_list([0x00, 0x66, 0x00], [0xCC, 0xFF, 0xCC], _n_journals), 
           label = "Number of keywords referred in the journal")
    ax.legend(loc='upper right')   
    ax.set_ylim(0, max_y)
    ax.set_yticks(numpy.arange(0, max_y + 10, 10))
    ax.set_xticks(numpy.arange(_n_journals), [x[0].replace(' ', '\n') for x in list_raw], fontsize = 11)
    pyplot.show()

def ShowTrendOfKeywordsFromYear(_remark_year, _maximum_keywords):
    list_raw = x2keywords.get_trend_of_keywords_from_year(_remark_year)
    print(list_raw)
    list_raw = list_raw[:_maximum_keywords]
    list_raw.reverse()

    max_x = max([x[1] for x in list_raw]) * 1.05
    max_x = max_x - max_x % 10

    fig, ax = pyplot.subplots()
    ax.cla()
    ax.set_title('Trend of keywords in ' + str(_remark_year), y = y)
    ax.barh(numpy.arange(len(list_raw)), 
           [x[1] for x in list_raw],
           height = 0.8, 
           color = get_palette_list([0x00, 0x66, 0x00], [0xCC, 0xFF, 0xCC], len(list_raw)), 
           label = "Number of keywords referred in " + str(_remark_year))
    ax.legend(loc='lower right')   
    ax.set_xlim(0, max_x)
    ax.set_xticks(numpy.arange(0, max_x + 50, 50))
    ax.set_yticks(numpy.arange(len(list_raw)), [x[0] for x in list_raw], fontsize = 12)
    pyplot.show()

def ShowTrendOfKeywordsFromJournal(_journal_name, _maximum_keywords):
    list_raw = x2keywords.get_trend_of_keywords_from_journal("Renewable Energy")
    list_raw = list_raw[:_maximum_keywords]
    print(list_raw)
    list_raw.reverse()

    max_x = max([x[1] for x in list_raw]) * 1.05
    max_x = max_x - max_x % 10

    fig, ax = pyplot.subplots()
    ax.cla()
    ax.set_title('Trend of keywords in the journal \'' + str(_journal_name) + '\'', y = y)
    ax.barh(numpy.arange(len(list_raw)), 
           [x[1] for x in list_raw],
           height = 0.8, 
           color = get_palette_list([0x00, 0x66, 0x00], [0xCC, 0xFF, 0xCC], len(list_raw)), 
           label = "Number of keywords referred in " + str(_journal_name))
    ax.legend(loc='lower right')   
    ax.set_xlim(0, max_x)
    ax.set_xticks(numpy.arange(0, max_x + 100, 100))
    ax.set_yticks(numpy.arange(len(list_raw)), [x[0] for x in list_raw], fontsize = 12)
    pyplot.show()