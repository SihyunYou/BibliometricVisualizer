import pickle
import pandas
from tqdm import tqdm
from retriever import ScopusReader
import json
from collections import OrderedDict

FILENAME_DATAFRAME = "../df/"
pandas.set_option('display.max_rows', 64)

class AbstractReader:
    def __init__(self, _query, _limit_journal = True):
        self.query = _query
        self.limit_journal = _limit_journal
        self.df_limited_abstract = None

        scopus_reader = ScopusReader(_query)
        hashed_filename = scopus_reader.get_hashed_filename()
        print(FILENAME_DATAFRAME + hashed_filename)

        try:
            with open(FILENAME_DATAFRAME + hashed_filename, 'rb') as f:
                df_raw_abstract = pickle.load(f)
        except:
            scopus_reader.retrieve()
            df_raw_abstract = scopus_reader.get_df_abstract()
            scopus_reader.save_df_abstract()
   
        if _limit_journal:
            with open(FILENAME_DATAFRAME + "good_journal_issn.txt", 'r') as f:
                list_good_journal_issn = f.readlines()
            list_good_journal_issn = [x.replace('-', '').replace('\n', '') for x in list_good_journal_issn]

            self.df_abstract = pandas.DataFrame(columns = df_raw_abstract.columns)
            for i in tqdm(range(df_raw_abstract.shape[0]), desc = "데이터프레임 추출 중"):
                list_article_issn = str(df_raw_abstract["SN"][i]).split(' ')
                for article_issn in list_article_issn:
                    if article_issn in list_good_journal_issn:
                        self.df_abstract.loc[len(self.df_abstract)] = df_raw_abstract.loc[i]
        else:
            self.df_abstract = df_raw_abstract
        self.__print_dataframe(self.df_abstract)

        resume_df = OrderedDict()
        start_year = self.df_abstract["PY"].values.tolist()[-1]
        resume_df["start_year"] = start_year
        end_year = self.df_abstract["PY"].values.tolist()[0]
        resume_df["end_year"] = end_year
        resume_df["year_frequency"] = [self.df_abstract["PY"].loc[self.df_abstract["PY"] == str(n)].shape[0] for n in range(int(start_year), int(end_year) + 1)]
        resume_df["journal_name"] = self.df_abstract["SO"].values.tolist()
        resume_df["journal_frequency"] = [self.df_abstract["SO"].loc[self.df_abstract["SO"] == journal].shape[0] for journal in self.df_abstract["SO"].values.tolist()]

        print(json.dumps(resume_df, indent="\t"))
        with open('../df/resume_df.json', 'w') as f:
            json.dump(resume_df, f, indent="\t")

    def __print_dataframe(self, _df):
        print(_df["PY"].value_counts())
        print(_df["SO"].value_counts().head(10))
        print("Number of articles : " + str(_df.shape[0]))

    def Read(self, _range_year = (2010, 2020), _publication_name = "All"):
        self.range_year = _range_year
        self.publication_name = _publication_name
        self.df_abstract = self.df_abstract.loc[\
                (self.df_abstract["PY"].astype(int) >= _range_year[0]) &\
                (self.df_abstract["PY"].astype(int) <= _range_year[1])]
        if _publication_name != 'All':
            self.df_abstract = self.df_abstract.loc[self.df_abstract["SO"].isin(_publication_name.split(';'))]