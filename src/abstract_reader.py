import pickle
import pandas
from tqdm import tqdm
from retriever import ScopusReader

FILENAME_DATAFRAME = "../df/"
dict_abstract = {}

class AbstractReader:
    def __init__(self, _query, _range_year = (2010, 2020), _publication_name = "All", _limit_journal = True):
        self.query = _query
        self.range_year = _range_year
        self.publication_name = _publication_name
        self.limit_journal = _limit_journal
    
    def __print_dataframe(self, _df):
        print(_df["PY"].value_counts())
        print(_df["SO"].value_counts().head(10))
        print("Number of articles : " + str(_df.shape[0]))

    def __read_abstract(self, _query, _limit_journal):
        scopus_reader = ScopusReader(_query)
        hashed_filename = scopus_reader.get_hashed_filename()
        print(FILENAME_DATAFRAME + hashed_filename)
        try:
            return dict_abstract[hashed_filename]
        except:
            pass

        try:
            with open(FILENAME_DATAFRAME + hashed_filename, 'rb') as f:
                df_raw_abstract = pickle.load(f)
        except:
            scopus_reader.retrieve()
            df_raw_abstract = scopus_reader.get_df_abstract()
            scopus_reader.save_df_abstract()

        if not _limit_journal:
            dict_abstract[hashed_filename] = df_raw_abstract
            self.__print_dataframe(df_raw_abstract)
            return df_raw_abstract

        with open(FILENAME_DATAFRAME + "good_journal_issn.txt", 'r') as f:
            list_good_journal_issn = f.readlines()
        list_good_journal_issn = [x.replace('-', '').replace('\n', '') for x in list_good_journal_issn]

        df_abstract = pandas.DataFrame(columns = df_raw_abstract.columns)
        for i in tqdm(range(df_raw_abstract.shape[0]), desc = "데이터프레임 추출 중"):
            list_article_issn = str(df_raw_abstract["SN"][i]).split(' ')
            for article_issn in list_article_issn:
                if article_issn in list_good_journal_issn:
                    df_abstract.loc[len(df_abstract)] = df_raw_abstract.loc[i]

        dict_abstract[hashed_filename] = df_abstract
        self.__print_dataframe(df_abstract)
        return df_abstract

    def get_dataframe(self):
        df_abstract = self.__read_abstract(self.query, self.limit_journal)
        df_abstract = df_abstract.loc[\
                (df_abstract["PY"].astype(int) >= self.range_year[0]) &\
                (df_abstract["PY"].astype(int) <= self.range_year[1])]
        if self.publication_name != 'All':
            df_abstract = df_abstract.loc[df_abstract["SO"].isin(self.publication_name.split(';'))]
            
        return df_abstract