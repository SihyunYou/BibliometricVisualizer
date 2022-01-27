class BibliometricParameter:
    def __init__(self, _query, _range_year = (2010, 2020), _publication_name = "All", _limit_journal = True):
        self.query = _query
        self.range_year = _range_year
        self.publication_name = _publication_name
        self.limit_journal = _limit_journal
    
    def get_conditioned_dataframe(self, _df_abstract):
        df_abstract = df_abstract.loc[\
                (df_abstract["PY"].astype(int) >= _range_year[0]) &\
                (df_abstract["PY"].astype(int) <= _range_year[1])]

        if self.publication_name != 'All':
            df_abstract = df_abstract.loc[df_abstract["SO"].isin(self.publication_name.split(';'))]
            
        return df_abstract