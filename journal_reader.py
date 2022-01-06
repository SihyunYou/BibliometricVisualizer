import pickle
import pandas
import regularizer
from tqdm import tqdm

df_good_journal = pandas.read_excel("good_journal.xlsx", header = 7)
with open("df_ab.pkl", 'rb') as f:
    df_ab = pickle.load(f)

list_so = [regularizer.regularize_publication_name(x) for x in df_ab["SO"].values.tolist()]
list_title = [regularizer.regularize_publication_name(x) for x in df_good_journal["TITLE"].values.tolist()]
list_interesting_journal = list(set(list_so) & set(list_title))

# 정규화된 저널 리스트를 복호화
for journal_so in tqdm(df_ab["SO"].values.tolist()):
    for i in range(len(list_interesting_journal)):
        if regularizer.regularize_publication_name(list_interesting_journal[i]) == regularizer.regularize_publication_name(journal_so):
            list_interesting_journal[i] = journal_so

df_journal = df_ab.loc[df_ab["SO"].isin(list_interesting_journal)]
print("Number of journals to search : " + str(len(list_interesting_journal)))
print("Number of articles to search : " + str(df_journal.shape[0]))

