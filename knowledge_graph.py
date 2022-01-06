#!/usr/bin/env python
# coding: utf-8

# In[4]:


# from graphviz import Digraph

# g = Digraph('G', filename='hello.gv')
# g.edge('Hello', 'World')
# g.view()


# In[18]:


from graphviz import Digraph

f = Digraph("knowledge_hierarchy", filename="knowledge_hierarchy", format="png")
f.attr(rankdir="LR")

f.attr("node", shape='doublecircle')
f.node("statistics")
f.node("method")
f.node("machine_learning")
f.node("metric")
f.node("ensemble")
f.node("data")
f.node("algorithm")

f.attr("node", shape="ellipse")
f.edge("statistics", "analysis_of_variance")
f.edge("statistics", "autoregressive_integrated_moving_average")
f.edge("statistics", "autoregressive_moving_average")
f.edge("statistics", "markov")
f.edge("statistics", "kalman_filter")
f.edge("statistics", "bayes")
f.edge("statistics", "gaussian_process")
f.edge("statistics", "autoregressi")
f.edge("statistics", "probabilistic")
f.edge("statistics", "kfold")
f.edge("statistics", "ensemble")
f.edge("statistics", "kruskal_wallis")

f.edge("method", "taguchi")
f.edge("method", "averaging_point_method")
f.edge("method", "describing_function_method")
f.edge("method", "finite_difference_time_domain_method")
f.edge("method", "finite_element_method")
f.edge("method", "group_method_of_data_handling")
f.edge("method", "incremental_conductance_method")
f.edge("method", "match_evaluation_method")
f.edge("method", "multiple_shifted_frequency_method")
f.edge("method", "numerical_method")
f.edge("method", "oblique_asymptote_method")
f.edge("method", "response_surface_methodology")
f.edge("method", "steepest_descent_method")
f.edge("method", "nelder_mead")
f.edge("method", "newton_raphson")
f.edge("method", "runge_kutta")
f.edge("method", "conditional_interpolation")
f.edge("method", "expectation_maximization")
f.edge("method", "Dynamic_simulation")
f.edge("method", "empirical")
f.edge("method", "emulation")
f.edge("method", "Gradient_descent")

f.edge("metric", "mean_square_error")
f.edge("metric", "mean_absolute_error")
f.edge("metric", "mean_absolute_percentage_error")
f.edge("metric", "cross_entropy")
f.edge("metric", "least_square")

f.edge("machine_learning", "clustering")
f.edge("machine_learning", "regression")
f.edge("machine_learning", "classification")
f.edge("machine_learning", "dimension_reduction")
f.edge("machine_learning", "reinforcement_learning")
f.edge("machine_learning", "ensemble")
f.edge("machine_learning", "natural_language_processing")

f.edge("natural_language_processing", "doc2vec")

f.edge("reinforcement_learning", "sarsa")
f.edge("reinforcement_learning", "markov")

f.edge("ensemble", "random_forest")
f.edge("ensemble", "adaboost")
f.edge("ensemble", "bagging")
f.edge("ensemble", "bootstrap")
f.edge("ensemble", "lightgbm")
f.edge("ensemble", "xgboost")

f.edge("data", "database")
f.edge("data", "data_acquisition")
f.edge("data", "data_mining")
f.edge("data", "data_driven")
f.edge("data", "data_based")

f.edge("database", "MapReduce")
f.edge("database", "sql")
f.edge("database", "hadoop")

f.edge("classification", "k_nearest_neighbor")
f.edge("classification", "support_vector_machine")
f.edge("classification", "neural_network")

f.edge("regression", "k_nearest_neighbor")
f.edge("regression", "support_vector_machine")
f.edge("regression", "neural_network")
f.edge("regression", "ridge")
f.edge("regression", "lasso")
f.edge("regression", "autoregressive")
f.edge("regression", "support_vector_regression")

f.edge("clustering", "k_means")
f.edge("clustering", "DBSCAN")

f.edge("neural_network", "artificial_neural_network")
f.edge("neural_network", "learning_vector_quantization")
f.edge("neural_network", "recurrent_neural_network")
f.edge("neural_network", "convolutional_neural_network")
f.edge("neural_network", "autoencoder")
f.edge("neural_network", "adaline")
f.edge("neural_network", "artificial_neural_fuzzy_inference_system")
f.edge("neural_network", "elman")
f.edge("neural_network", "attention")
f.edge("neural_network", "Extreme_Learning_Machine")
f.edge("neural_network", "multilayer_perceptron")

f.edge("recurrent_neural_network", "long_short_term_memory")
f.edge("recurrent_neural_network", "boltzmann_machine")

f.edge("convolutional_neural_network", "GoogLeNet")

f.edge("dimension_reduction", "principal_component_analysis")
f.edge("dimension_reduction", "factor_analysis")
f.edge("dimension_reduction", "autoencoder")

f.edge("algorithm", "ant_colony")
f.edge("algorithm", "ant_lion")
f.edge("algorithm", "artificial_bee_colony")
f.edge("algorithm", "artificial_fish_swarm")
f.edge("algorithm", "backtracking_search")
f.edge("algorithm", "bacterial_foraging")
f.edge("algorithm", "bat")
f.edge("algorithm", "bee_pollinator")
f.edge("algorithm", "binary_search")
f.edge("algorithm", "bio_inspired")
f.edge("algorithm", "bucket_elimination")
f.edge("algorithm", "crow_search")
f.edge("algorithm", "elite_retention")
f.edge("algorithm", "evolutionary")
f.edge("algorithm", "firefly")
f.edge("algorithm", "fireworks_explosion")
f.edge("algorithm", "flower_pollination")
f.edge("algorithm", "fruitfly")
f.edge("algorithm", "genetic_algorithm")
f.edge("algorithm", "golden_section")
f.edge("algorithm", "grasshopper")
f.edge("algorithm", "gravity_search")
f.edge("algorithm", "grey_wolf")
f.edge("algorithm", "imperialist_competition")
f.edge("algorithm", "jaya")
f.edge("algorithm", "leapfrog")
f.edge("algorithm", "honey_bee_mating")
f.edge("algorithm", "interior_search")
f.edge("algorithm", "invasive_weed")
f.edge("algorithm", "elephant_herding")
f.edge("algorithm", "particle_swarm")
f.edge("algorithm", "pattern_search")
f.edge("algorithm", "perturb_and_observe")
f.edge("algorithm", "shuffled_frog_leaping")
f.edge("algorithm", "versatile_threshold")
f.edge("algorithm", "monte_carlo")
f.edge("algorithm", "rule_based")
f.edge("algorithm", "Dynamic_Programming")

f.edge("Dynamic_Programming", "reinforcement_learning")

f.render()
# f.view()


# In[ ]:




