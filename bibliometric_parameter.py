class BibliometricParameter:
    def __init__(self):
        self.query = ''
        self.range_year = (2010, 2020)
        self.limit_journal = True

class Keyword2xParameter(BibliometricParameter):
    def __init__(self, _bibliometricParameter):
        self.query = _bibliometricParameter.query
        self.range_year = _bibliometricParameter.range_year
        self.limit_journal = _bibliometricParameter.limit_journal

        self.target = ''
        self.user_keyword = ''

class X2KeywordParameter(BibliometricParameter):
    def __init__(self, _bibliometricParameter):
        self.query = _bibliometricParameter.query
        self.range_year = _bibliometricParameter.range_year
        self.limit_journal = _bibliometricParameter.limit_journal

        self.publication_name_ = ''