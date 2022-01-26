import pickle as pkl
with open("corpus_redirection.pickle","rb") as pf:
    s = pkl.load(pf)
    print(s)