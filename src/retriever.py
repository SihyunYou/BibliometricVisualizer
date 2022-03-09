from pybliometrics.scopus import ScopusSearch
from pybliometrics.scopus import AbstractRetrieval
from tqdm import tqdm
import pandas as pd
import numpy as np
import calendar
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

class ScopusReader:
    def __init__(self, _query):
        self.query = _query

    def retrieve(self):
        df_abstract_retrieved = pd.DataFrame(ScopusSearch(self.query, download=True, verbose=True).results)
        columns=["eid", "PT", "AU", "AF", "TI", 
                    "SO", "SO_abb", "LA", "DT", "DE", 
                    "ID", "AB", "C1", "RP", "EM", 
                    "CR", "NR", "TC", "Z9", "SN", 
                    "J9", "JI", "PD", "PY", "VL", 
                    "AR", "DI", "SC"]
        self.df_ab = pd.DataFrame(columns=columns)

        starting_index = 0
        data_index = list(range(starting_index, df_abstract_retrieved.shape[0]))

        for art in tqdm(data_index, desc="논문 초록을 받아오는 중"):
            eid = df_abstract_retrieved.loc[art, "eid"]
            ab = AbstractRetrieval(eid, view="FULL")

            # 1. PT: publication type
            docu_type_ = ab.srctype

            # 2. AU: index name
            index_name_ = [a.indexed_name for a in ab.authors] if ab.authors else [None]

            # 3. AF: author name
            author_name_ = [f"{a.surname}, {a.given_name}" for a in ab.authors] if ab.authors else [None]

            # 4. TI: document title
            docu_title_ = df_abstract_retrieved.loc[art, "title"]

            # 5. SO: publication name
            src_title_ = ab.publicationName

            # 5-1. publication abbr.
            src_abb_ = ab.sourcetitle_abbreviation

            # 6. LA : Language
            try:
                language_ = dic_language[ab.language]
            except:
                language_ = "unknown"

            # 7. DT : Document Type
            docu_type_ = ab.subtype

            # 8. DE : Author Keywords
            auth_kw_ = ab.authkeywords

            if not auth_kw_:
                auth_kw_ = 'None'
            else:
                auth_kw_ = '; '.join(auth_kw_)

            # 9. ID : Keyword Plus
            kw_plus_ = 'None'

            # 10. AB : Abstract
            abstract_ = ab.abstract

            # 11. C1 : Author Address
        #     if ab.authorgroup:
        #         tmp = pd.DataFrame(ab.authorgroup)
        #         grouped = tmp.groupby('organization').agg(lambda x: list(x))

        #         aff_names = [str(aff) for aff in grouped["affiliation_id"].index.tolist()]
        #         aff_ids = grouped["affiliation_id"].tolist()
        #         citys = grouped["city"].tolist()
        #         countrys = grouped["country"].tolist()
        #         auids = grouped["auid"].tolist()
        #         indexed_names = grouped["indexed_name"].tolist()

        #         address = []
        #         for aff_name, aff_id, city, country in zip(aff_names, aff_ids, citys, countrys):
        #             if isinstance(aff_id, list):
        #                 aff_id, city, country = aff_id[0], city[0], country[0]
        #             address.append(f"{aff_id}, {aff_name}, {city}, {country}")

        #         addresss_ = list(zip(auids, indexed_names, address))
            if ab.affiliation and ab.authors:
                df_aff = pd.DataFrame(ab.affiliation)
                df_aff["id"] = df_aff["id"].astype(str)
                df_auth = pd.DataFrame(ab.authors)
                df_authgroup = df_auth.groupby("affiliation").agg(list).reset_index()

                df_aff = pd.merge(df_aff, df_authgroup, left_on="id", right_on="affiliation").drop(["affiliation"], axis=1)
                df_aff["address"] = df_aff[['id', 'name', 'city', 'country']].apply(lambda x: ', '.join(x.astype(str)), axis=1)
                addresss_ = df_aff[["auid", "indexed_name", "address"]].values.tolist()
            else:
                addresss_ = []

            # df_aff = pd.DataFrame(ab.authorgroup)
            # grouped = df_aff.groupby("affiliation_id")
            # grouped[["organization", "affiliation_id", "city", "country"]]

            # 12. RP : Reprint Address
            rep_addr_ = "None"

            # 13. EM : E-mail Address
            em_addr_ = "None"

            # 14. CR : Cited References
            refs_ = []
            if ab.references != None:
                tmp = pd.DataFrame(ab.references)
                refcount = int(ab.refcount)

                for i in range(refcount):
                    tmp_ = tmp.iloc[i]
                    tmp_authors = tmp_['authors']
                    if tmp_authors == None:
                        tmp_authors = "[Anonymous]"
                    tmp_year = tmp_['publicationyear']
                    tmp_src = tmp_['sourcetitle']
                    tmp_vol = tmp_['volume']
                    tmp_page = tmp_['first']
                    tmp_doi = tmp_['doi']

                    ref = tmp_authors
                    for item in [tmp_year, tmp_src, tmp_vol, tmp_page]:
                        if item != None:
                            ref = ', '.join([ref, item])
                    if tmp_doi != None:
                        ref = ref + f", DOI {tmp_doi}"

                    if i == 0:
                        refs_.append(f"CR {ref}")
                    else:
                        refs_.append(f"   {ref}")

            # 15. NR : Cited Reference Count
            nr_ = ab.refcount

            # 16. TC : Web of Science Core Collection Times Cited Count
            tc_ = ab.citedby_count

            # 17. Z9 : Total Times Cited Count
            cc_ = tc_

            # 18. U1 : Usage Count (Last 180 Days)
            # 19. U2 : Usage Count (Since 2013)
            # 20. PU : Publisher = ELSEVIER SCI LTD
            # 21. PI : Publisher City = OXFORD
            # 22. PA : Publisher Address = THE BOULEVARD, LANGFORD LANE, KIDLINGTON, OXFORD OX5 1GB, OXON, ENGLAND
            # 23. SN : International Standard Serial Number (ISSN) = 0959-6526
            sn_ = "None" if ab.issn == None else ab.issn

            # 24. EI : Electronic International Standard Serial Number (eISSN) = 1879-1786
            # 25. J9 : 29-Character Source Abbreviation = J CLEAN PROD
            j9_ = ab.sourcetitle_abbreviation if ab.sourcetitle_abbreviation != None else "None"
            j9_ = j9_.upper()

            # 26. JI : ISO Source Abbreviation = J. Clean Prod.
            ji_ = ab.sourcetitle_abbreviation if ab.sourcetitle_abbreviation != None else "None"

            # 27. PD : Publication Date = JUL 1
            month = ab.coverDate.split('-')[1]
            date = ab.coverDate.split('-')[2]
            pd_ = f"{calendar.month_name[int(month)][:3].upper()} {int(date)}"

            # 28. PY : Publication Year = 2020
            py_ = ab.coverDate.split('-')[0]

            # 29. VL : Volumn = 260
            vl_ = ab.volume

            # 30. AR : Article Number = 121059
            ar_ = df_abstract_retrieved.loc[art, "article_number"] if df_abstract_retrieved.loc[art, "article_number"] != None else "None"

            # 31. DI : Digital Object Identifier = 10.1016/j.jclepro.2020.121059
            doi_ = ab.doi

            # 32. PG : Page Count = 14
            # 33. WC : Web of Science Categories = Green & Sustainable Science & Technology; Engineering, Environmental; Environmental Sciences
            # 34. SC : Research Areas = Science & Technology - Other Topics; Engineering; Environmental Sciences & Ecology
            if ab.subject_areas:        
                tmp = pd.DataFrame(ab.subject_areas)
                tmp_ = tmp["area"].tolist()
                sc_ = "; ".join(tmp_)
            else: 
                sc_ = [None]

            # 35. GA : Document Delivery Number = LL4XH
            # 36. UT : Accession Number = WOS:000531559900003
            # 37. DA : Date this report was generated. = 2020-06-14
    
            # summation
            data=[eid, docu_type_, index_name_, author_name_, docu_title_, 
                                        src_title_, src_abb_, language_, docu_type_, auth_kw_, 
                                        kw_plus_, abstract_, addresss_, rep_addr_, em_addr_, 
                                        refs_, nr_, tc_, cc_, sn_, 
                                        j9_, ji_, pd_, py_, vl_, 
                                        ar_, doi_, sc_]
    
            df_ab_tmp = pd.DataFrame(dict(zip(columns, [[d] for d in data])))
            self.df_ab = pd.concat([self.df_ab, df_ab_tmp], axis=0)

    def get_hashed_filename(self):
        import hashlib
        return hashlib.md5(self.query.encode()).hexdigest() + ".pkl"

    def get_df_abstract(self):
        return self.df_ab

    def save_df_abstract(self):
        self.df_ab.to_pickle("df/" + self.get_hashed_filename())
