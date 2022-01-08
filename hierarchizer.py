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
    

dict_relative = {
 "estimator": ["estimation"],
 "pv": ["photovoltaic"],
 "optimisation": ["optimization"],
 "modelling": ["modeling"],
 "radiance": ["irradiation"],
 "radiation": ["irradiation"],
 "irradiance": ["irradiation"],
 "diode": ["diode"],
 "ESS": ["energy storage system"],
 "forecast": ["prediction"],
 "predictor": ["prediction"],
 "prognosis": ["prediction"],
 "prognose": ["prediction"],
 "mppt": ["maximum power point track"],
 "measuring": ["measurement"],
 "modul": ["module"],
 "diagnose": ["diagnosis"],
 "protection": ["protection"],
 "fa\u00e7ade": ["facade"],
 "analyz": ["analysis"],
 "extract": ["extraction"],
 "high concentrat": ["high-concentration"],
 "high frequency": ["high-frequency"],
 "hf": ["high frequency"],
 "high resolution": ["high-resolution"],
 "household": ["home"],
 "//t": ["thermal"],
 "power plant": ["power-plant"],
 "pvt": ["photovoltaic"],
 "hydro ": ["water"],
 "hydro-": ["water"],
 "image proc": ["image processing"],
 "large scale" : ["large-scale"],
 "least square": ["least-square"],
 "lithium ion": ["lithium-ion"],
 "long term": ["long-term"],
 "short term": ["short-term"],
 "low concentrat": ["low-concentration"],
 "low carbon": ["low-carbon"],
 "low voltage": ["low-voltage"],
 "low frequency": ["low-frequency"],
 "multi objective": ["multi-objective"],
 "nsrdb": ["national solar radiation database"],
 "nwp": ["numerical weather prediction"],
 "noisy": ["noise"],
 "non linear": ["non-linear"],
 "nonlinear": ["non-linear"],
 "non uniform": ["non-uniform"],
 "nonuniform": ["non-uniform"],
 "optimal": ["optimization"],
 "photo voltaic": ["photovoltaic"],
 "parametric": ["parameter"],
 "predictive": ["prediction"],
 "reliable": ["reliability"],
 "renewable energy source": ["renewable energy source"],
 "correct": ["correction"],
 "correlat": ["correlation"],
 "band gap": ["bandgap"],
 "band-gap": ["bandgap"],
 "distributed": ["distribution"],
 "energ": ["energy"],
 "fft": ["fast fourier transform"],
 "ifft": ["inverse fast fourier transform"],
 "bayes": ["bayesian"],
 "cluster": ["clustering"],
 "k nearest neighbor": ["k-nearest-neighbor"],
 "k-nearest neighbor": ["k-nearest-neighbor"],
 "knn": ["k-nearest-neighbor"],
 "gbdt": ["gradient-boosting-decision-tree"],
 "gradient boosting decision tree": ["gradient-boosting-decision-tree"],
 "gradient-boosting decision tree": ["radient-boosting-decision-tree"],
 "gradient boosting decision-tree": ["radient-boosting-decision-tree"],
 "gradient-boosting decision-tree": ["radient-boosting-decision-tree"],
 "gradient boosting": ["gradient-boosting"],
 "k mean": ["k-means"],
 "data base": ["database"],
 "meteorolog": ["meteorology"],
 "autoregressi": ["auto-regression"],
 "auto-regressi": ["auto-regression"],
 "auto regressi": ["auto-regression"],
 "on-line": ["online"],
 "principal component analysis": ["pca"],
 "convolutional neural network": ["cnn"],
 "long short term memory": ["lstm"],
 "long short-term memory": ["lstm"],
 "recurrent neural network": ["rnn"],
 "ant colony": ["ant-colony"],
 "ant lion": ["ant-lion"],
 "bpa" : ["bee-pollinator"],
 "bee pollinator": ["bee-pollinator"],
 "fpa": ["flower-pollination"],
 "flower pollination": ["flower-pollination"],
 "back search": ["backtracking search"],
 "cso": ["cat swarm optimization"],
 "p&o": ["perturb and observe"],
 "p & o": ["perturb and observe"],
 "p o": ["perturb and observe"],
 "p and o": ["perturb and observe"],
 "ga": ["genetic algorithm"],
 "gravitational": ["gravity"],
 "iwo": ["invasive weed"],
 "levengerg marquardt": ["levengerg-marquardt"],
 "mae": ["mean absolute error"],
 "mse": ["mean squared error"],
 "mbe": ["mean bias error"],
 "nrmse": ["normalized root mean squared error"],
 "rmse": ["root mean squared error"],
 "elephant swarm water search": ["elephant swarm water search"],
 "n-m": ["nelder-mead"],
 "newton raphson": ["newton-raphson"],
 "sparse aware": ["sparse-aware"],
 "bucket elimination": ["bucket-elimination"],
 "controller": ["control"],
 "bems": ["building energy management system"],
 "bapv": ["building attached photovoltaic"],
 "bipv": ["building integrated photovoltaic"],
 "building-integrated photovoltaic": ["building integrated photovoltaic"],
 "builing-integrated solar system": ["builing integrated solar system"],
 "bipvt": ["building integrated photovoltaic thermal"],
 "bipv/t": ["building integrated photovoltaic thermal"],
 "builing integrated solar thermal": ["builing-integrated solar thermal"],
 "bist": ["building integrated solar thermal"],
 "bists": ["building integrated solar thermal"],
 "bess": ["battery energy storage system"],
 "batteries": ["battery"],
 "bss": ["battery storage system"],
 "cfd": ["computational fluid dynamic"],
 "cpv": ["concentrated photovoltaic"],
 "cpvt": ["concentrated photovoltaic thermal"],
 "cpv/t": ["concentrated photovoltaic thermal"],
 "concentrated photovoltaic and thermal": ["concentrated photovoltaic thermal"],
 "concentrated photovoltaic-thermal": ["concentrated photovoltaic thermal"],
 "concentrated photovoltaic/thermal": ["concentrated photovoltaic thermal"]
}

N_GRAM = 4
def replace_synonym(_list_tokenized_word):
    for key, list_value in dict_relative.items():
        for i in range(N_GRAM):
            for j in range(len(_list_tokenized_word) - i):
                combined_word = ' '.join(_list_tokenized_word[j:j+i+1])
                if key == combined_word:
                    _list_tokenized_word[j] = ' '.join(list_value)
                    for k in range(j + 1, j + i + 1):
                        _list_tokenized_word[k] = ''
    temp = []
    for word in _list_tokenized_word:
        if word != '':
            list_a = word.split(' ')
            for a in list_a:
                temp.append(a)
    return temp