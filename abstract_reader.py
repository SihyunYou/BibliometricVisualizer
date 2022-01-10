import pickle
import pandas
import regularizer
from tqdm import tqdm

df_good_journal = pandas.read_excel("good_journal.xlsx", header = 7)
with open("df_ab.pkl", 'rb') as f:
    df_ab = pickle.load(f)

list_title = [regularizer.regularize_publication_name(x) for x in df_good_journal["TITLE"].values.tolist()]
df_abstract = pandas.DataFrame(columns = df_ab.columns)
for i in tqdm(range(df_ab.shape[0]), desc = "데이터프레임 정규화 중"):
    if regularizer.regularize_publication_name(df_ab["SO"][i]) in list_title:
        df_abstract.loc[len(df_abstract)] = df_ab.loc[i]

print(df_abstract["PY"].value_counts().head(10))
print(df_abstract["SO"].value_counts().head(10))
print("Number of articles to search: " + str(df_abstract.shape[0]))

