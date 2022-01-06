dict_knowledge_hierarchy = {
  "statistics": [
    "analysis of variance",
    "autoregressive integrated moving average",
    "autoregressive moving average",
    "markov",
    "kalman",
    "bayes",
    "gaussian process",
    "autoregression",
    "autoregressive",
    "probabilistic",
    "k-fold",
    "ensemble",
    "kruskal-wallis"
  ],
  "method": [
    "taguchi",
    "averaging point method",
    "describing function method",
    "finite difference time domain method",
    "finite element method",
    "group method of data handling",
    "incremental conductance method",
    "match evaluation method",
    "multiple-shifted-frequency method",
    "numerical method",
    "oblique asymptote method",
    "response surface methodology",
    "steepest descent method",
    "nelder-mead",
    "newton-raphson",
    "runge-kutta",
    "conditional interpolation",
    "expectation-maximization",
    "dynamic simulation",
    "empirical",
    "emulation",
    "gradient descent",
    "algorithm"
  ],
  "metric": [
    "mean square error",
    "mean absolute error",
    "mean absolute percentage error",
    "cross-entropy",
    "least-square",
    "mean bias error"
  ],
  "machine learning": [
    "clustering",
    "regression",
    "classification",
    "dimension reduction",
    "reinforcement learning",
    "ensemble",
    "natural language processing"
  ],
  "doc2vec": [
    "natural language processing"
  ],
  "reinforcement learning": [
    "sarsa",
    "markov"
  ],
  "ensemble": [
    "random forest",
    "adaboost",
    "bagging",
    "bootstrap",
    "lightgbm",
    "xgboost"
  ],
  "data": [
    "database",
    "data acquisition",
    "data-mining",
    "data-driven",
    "data-based"
  ],
  "database": [
    "mapreduce",
    "sql",
    "hadoop"
  ],
  "classification": [
    "k-nearest neighbor",
    "support vector machine",
    "neural network"
  ],
  "regression": [
    "k-nearest neighbor",
    "support vector machine",
    "neural network",
    "ridge",
    "lasso",
    "autoregressive",
    "support vector regression"
  ],
  "clustering": [
    "k means",
    "dbscan"
  ],
  "neural network": [
    "artificial neural network",
    "learning vector quantization",
    "recurrent neural network",
    "convolutional neural network",
    "autoencoder",
    "adaline",
    "artificial neural fuzzy inference system",
    "elman",
    "attention",
    "extreme learning machine",
    "multilayer perceptron"
  ],
  "recurrent neural network": [
    "long short-term memory",
    "boltzmann machine"
  ],
  "convolutional neural network": [
    "googlenet"
  ],
  "dimension reduction": [
    "principal component analysis",
    "factor analysis",
    "autoencoder"
  ],
  "algorithm": [
    "agent-based",
    "ant colony",
    "ant lion",
    "artificial bee colony",
    "artificial fish swarm",
    "backtracking search",
    "bacterial foraging",
    "bat",
    "bee pollinator",
    "binary search",
    "bio-inspired",
    "bucket elimination",
    "crow search",
    "elite retention",
    "evolutionary",
    "firefly",
    "fireworks explosion",
    "flower pollination",
    "fruitfly",
    "genetic algorithm",
    "golden section",
    "grasshopper",
    "gravity search",
    "grey wolf",
    "imperialist competition",
    "jaya",
    "leapfrog",
    "honey bee mating",
    "interior search",
    "invasive weed",
    "elephant herding",
    "particle swarm",
    "pattern search",
    "perturb and observe",
    "shuffled frog leaping",
    "versatile threshold",
    "monte carlo",
    "rule-based",
    "dynamic programming"
  ],
  "dynamic programming": [
    "reinforcement learning"
  ],
  "building-integrated": [
    "bapv",
    "bipv",
    "biss",
    "bispv",
    "bispvt",
    "bipv",
    "bipvt",
    "bipv/t",
    "bist",
    "bists"
  ],
  "thermal": [
    "bapvt",
    "bapv/t",
    "bispvt",
    "bipvt",
    "bipv/t",
    "bist",
    "bists"
  ],
  "photovoltaic": [
    "bapv",
    "bispv",
    "bispvt",
    "bipv",
    "biss",
    "bipv",
    "bipvt",
    "bipv/t",
    "bist",
    "bists",
    "agrivoltaic"
  ],
  "agriculture": [
    "agrivoltaic"
  ]
}

def is_this_keyword_hierarchical(_keyword):
    for key in dict_knowledge_hierarchy: 
        if(_keyword == key):
            return True
        for value in dict_knowledge_hierarchy[key]:
            if(_keyword == value):
                return True
    return False

list_searched = []

def search_knowledge_hierarchy(_value):
    if _value not in list_searched and is_this_keyword_hierarchical(_value):
        list_searched.append(_value)

    for key in dict_knowledge_hierarchy:
        if(key == _value):
            if(key not in list_searched):
                list_searched.append(key)
        for node in dict_knowledge_hierarchy[key]:
            if(_value == node):
                if(key not in list_searched):
                    list_searched.append(key)
                search_knowledge_hierarchy(key)

def get_maximum_len_of_words_in_graph():
    p = 0
    for key in dict_knowledge_hierarchy: 
        for value in dict_knowledge_hierarchy[key]:
            list_words = value.split(' ')
            if p < len(list_words):
                p  = len(list_words)
    return p

MAX_LEN_WORD_GRAPH = get_maximum_len_of_words_in_graph()            
    


