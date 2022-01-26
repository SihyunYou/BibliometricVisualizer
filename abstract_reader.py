import pickle
import pandas
from tqdm import tqdm
from retriever import ScopusReader

dict_abstract = {}

def print_dataframe(_df):
    print(_df["PY"].value_counts().head(10))
    print(_df["SO"].value_counts().head(10))
    print("Number of articles : " + str(_df.shape[0]))

def read_abstract(_query, _limit_journal):
    scopus_reader = ScopusReader(_query)
    hashed_filename = scopus_reader.get_hashed_filename()
    print(hashed_filename)
    try:
        return dict_abstract[hashed_filename]
    except:
        pass

    try:
        with open(hashed_filename, 'rb') as f:
            df_raw_abstract = pickle.load(f)
    except:
        scopus_reader.retrieve()
        df_raw_abstract = scopus_reader.get_df_abstract()
        scopus_reader.save_df_abstract()

    if not _limit_journal:
        dict_abstract[hashed_filename] = df_raw_abstract
        print_dataframe(df_raw_abstract)
        return df_raw_abstract

    with open("good_journal_issn.txt", 'r') as f:
        list_good_journal_issn = f.readlines()
    list_good_journal_issn = [x.replace('-', '').replace('\n', '') for x in list_good_journal_issn]

    df_abstract = pandas.DataFrame(columns = df_raw_abstract.columns)
    for i in tqdm(range(df_raw_abstract.shape[0]), desc = "데이터프레임 추출 중"):
        list_article_issn = str(df_raw_abstract["SN"][i]).split(' ')
        for article_issn in list_article_issn:
            if article_issn in list_good_journal_issn:
                df_abstract.loc[len(df_abstract)] = df_raw_abstract.loc[i]

    dict_abstract[hashed_filename] = df_abstract
    print_dataframe(df_abstract)
    return df_abstract