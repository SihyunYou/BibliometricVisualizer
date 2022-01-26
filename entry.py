from bibliometric_visualizer import BibliometricVisualizer

Query = """\
TITLE-ABS-KEY ( "Photovoltaic" OR "BIPV" OR "PV" OR "Irradiation") AND
TITLE-ABS-KEY ( "solar" OR "sun") AND
TITLE-ABS-KEY ( "machine learning" OR "prediction" OR "modeling" ) AND
( EXCLUDE ( SUBJAREA , "MATE" ) OR EXCLUDE ( SUBJAREA , "CHEM" ) OR EXCLUDE ( SUBJAREA , "CENG" ) ) AND ( EXCLUDE ( SUBJAREA , "MEDI" ) OR EXCLUDE ( SUBJAREA , "SOCI" ) OR EXCLUDE ( SUBJAREA , "AGRI" ) OR EXCLUDE ( SUBJAREA , "BIOC" ) OR EXCLUDE ( SUBJAREA , "BUSI" ) OR EXCLUDE ( SUBJAREA , "ECON" ) OR EXCLUDE ( SUBJAREA , "IMMU" ) OR EXCLUDE ( SUBJAREA , "NEUR" ) OR EXCLUDE ( SUBJAREA , "PHAR" ) OR EXCLUDE ( SUBJAREA , "HEAL" ) OR EXCLUDE ( SUBJAREA , "PSYC" ) OR EXCLUDE ( SUBJAREA , "ARTS" ) OR EXCLUDE ( SUBJAREA , "VETE" ) OR EXCLUDE ( SUBJAREA , "NURS" ) OR EXCLUDE ( SUBJAREA , "DENT" ) OR EXCLUDE ( SUBJAREA , "Undefined" ) ) """
                 
visualizer = BibliometricVisualizer(Query, (2010, 2021), True)
#visualizer.ShowTrendOfYearsFromKeyword("machine learning")
visualizer.ShowTrendOfJournalsFromKeyword("machine learning", 10)
#visualizer.ShowWordCloudOfKeywords("Renewable Energy")
#visualizer.ShowNetworkOfKeywords("Renewable Energy")
