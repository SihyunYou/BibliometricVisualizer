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
    


dict_unigram = {
 "estimator": "estimation",
 "energy storage system": "ess",
 "pv": "photovoltaic",
 "optimisation": "optimization",
 "modelling": "modeling",
 "radiance": "irradiation",
 "radiation": "irradiation",
 "irradiance": "irradiation",
 "forecast": "prediction",
 "predictor": "prediction",
 "prognosis": "prediction",
 "prognose": "prediction",
 "machine learning": "machine_learning",
 "maximum power point track": "mppt",
 "measuring": "measurement",
 "modul": "module",
 "diagnose": "diagnosis",
 "analyz": "analysis",
 "extract": "extraction",
 "high concentrat": "high-concentration",
 "high frequency": "high-frequency",
 "hf": "high-frequency",
 "high resolution": "high-resolution",
 "household": "home",
 "//t": "thermal",
 "power plant": "power-plant",
 "hydro ": "water",
 "hydro-": "water",
 "image proc": "image_processing",
 "image processing": "image_processing",
 "large scale" : "large-scale",
 "least square": "least-square",
 "lithium ion": "lithium-ion",
 "long term": "long-term",
 "short term": "short-term",
 "low concentrat": "low-concentration",
 "low carbon": "low-carbon",
 "low voltage": "low-voltage",
 "low frequency": "low-frequency",
 "multi objective": "multi-objective",
 "nsrdb": "national_solar_radiation_database",
 "national solar radiation database": "national_solar_radiation_database",
 "nwp": "numerical_weather_prediction",
 "numerical weather prediction": "numerical_weather_prediction",
 "noisy": "noise",
 "non linear": "non-linear",
 "nonlinear": "non-linear",
 "non uniform": "non-uniform",
 "nonuniform": "non-uniform",
 "optimal": "optimization",
 "photo voltaic": "photovoltaic",
 "photovoltaics": "photovoltaic",
 "parametric": "parameter",
 "predictive": "prediction",
 "reliable": "reliability",
 "renewable energy source": "renewable_energy_source",
 "correct": "correction",
 "correlat": "correlation",
 "band gap": "bandgap",
 "band-gap": "bandgap",
 "distributed": "distribution",
 "energ": "energy",
 "fast fourier transform": "fft",
 "inverse fast fourier transform": "ifft",
 "bayes": "bayesian",
 "cluster": "clustering",
 "k nearest neighbor": "k-nearest_neighbor",
 "k-nearest neighbor": "k-nearest_neighbor",
 "knn": "k-nearest_neighbor",
 "gradient boosting decision tree": "gbdt",
 "gradient-boosting decision tree": "gbdt",
 "gradient boosting decision-tree": "gbdt",
 "gradient-boosting decision-tree": "gbdt",
 "gradient-boosting": "gradient_boosting",
 "gradient boosting": "gradient_boosting",
 "k mean": "k-means",
 "data base": "database",
 "meteorolog": "meteorology",
 "autoregressi": "auto-regression",
 "auto-regressi": "auto-regression",
 "auto regressi": "auto-regression",
 "on-line": "online",
 "principal component analysis": "pca",
 "convolutional neural network": "cnn",
 "long short term memory": "lstm",
 "long short-term memory": "lstm",
 "recurrent neural network": "rnn",
 "ant colony": "ant-colony",
 "ant lion": "ant-lion",
 "bpa" : "bee-pollinator",
 "bee pollinator": "bee-pollinator",
 "fpa": "flower-pollination",
 "flower pollination": "flower-pollination",
 "back search": "backtracking_search",
 "cat swarm optimization": "cso",
 "p&o": "perturb_and_observe",
 "p & o": "perturb_and_observe",
 "p o": "perturb_and_observe",
 "p and o": "perturb_and_observe",
 "ga": "genetic_algorithm",
 "genetic algorithm": "genetic_algorithm",
 "gravitational": "gravity",
 "iwo": "invasive_weed",
 "invasive weed": "invasive_weed",
 "levenberg marquardt": "levenberg-marquardt",
 "mean absolute error": "mae",
 "mean squared error": "mse",
 "mean bias error": "mbe",
 "normalized root mean squared error": "nrmse",
 "root mean squared error": "rmse",
 "elephant swarm water search": "elephant_swarm_water_search",
 "n-m": "nelder-mead",
 "newton raphson": "newton-raphson",
 "sparse aware": "sparse-aware",
 "bucket elimination": "bucket-elimination",
 "controller": "control",
 "building energy management system": "bems",
 "building attached photovoltaic": "bapv",
 "building integrated photovoltaic": "bipv",
 "building-integrated photovoltaic": "bipv",
 "builing integrated solar": "builing-integrated_solar",
 "builing-integrated solar": "builing-integrated_solar",
 "building integrated photovoltaic thermal": "bipvt",
 "building-integrated photovoltaic thermal": "bipvt",
 "pv-t": "pvt",
 "pv/t": "pvt",
 "photovoltaic-termal": "pvt",
 "bipv/t": "bipvt",
 "builing integrated solar thermal": "bist",
 "builing-integrated solar thermal": "bist",
 "bists": "bist",
 "battery energy storage system": "bess",
 "batteries": "battery",
 "battery storage system": "bss",
 "computational fluid dynamic": "cfd",
 "concentrated photovoltaic": "cpv",
 "concentrated photovoltaic thermal": "cpvt",
 "cpv/t": "cpvt",
 "concentrated photovoltaic and thermal": "cpvt",
 "concentrated photovoltaic-thermal": "cpvt",
 "concentrated photovoltaic/thermal": "cpvt",
 "methodology": "method"
}

N_GRAM = 4
def replace_synonym(_list_tokenized_word):
    for key, value in dict_unigram.items():
        for i in range(N_GRAM - 1, -1, -1):
            for j in range(len(_list_tokenized_word) - i):
                combined_word = ' '.join(_list_tokenized_word[j:j+i+1])
                if key == combined_word:
                    _list_tokenized_word[j] = value
                    for k in range(j + 1, j + i + 1):
                        _list_tokenized_word[k] = ''
    temp = []
    for word in _list_tokenized_word:
        if word != '':
            temp.append(word)
    return temp