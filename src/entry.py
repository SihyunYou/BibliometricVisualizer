#from bibliometric_visualizer import BibliometricVisualizer
#from abstract_reader import AbstractReader
import socket

Query = """\
TITLE-ABS-KEY ( "Photovoltaic" OR "BIPV" OR "PV" OR "Irradiation") AND
TITLE-ABS-KEY ( "solar" OR "sun") AND
TITLE-ABS-KEY ( "machine learning" OR "prediction" OR "modeling" ) AND
( EXCLUDE ( SUBJAREA , "MATE" ) OR EXCLUDE ( SUBJAREA , "CHEM" ) OR EXCLUDE ( SUBJAREA , "CENG" ) ) AND ( EXCLUDE ( SUBJAREA , "MEDI" ) OR EXCLUDE ( SUBJAREA , "SOCI" ) OR EXCLUDE ( SUBJAREA , "AGRI" ) OR EXCLUDE ( SUBJAREA , "BIOC" ) OR EXCLUDE ( SUBJAREA , "BUSI" ) OR EXCLUDE ( SUBJAREA , "ECON" ) OR EXCLUDE ( SUBJAREA , "IMMU" ) OR EXCLUDE ( SUBJAREA , "NEUR" ) OR EXCLUDE ( SUBJAREA , "PHAR" ) OR EXCLUDE ( SUBJAREA , "HEAL" ) OR EXCLUDE ( SUBJAREA , "PSYC" ) OR EXCLUDE ( SUBJAREA , "ARTS" ) OR EXCLUDE ( SUBJAREA , "VETE" ) OR EXCLUDE ( SUBJAREA , "NURS" ) OR EXCLUDE ( SUBJAREA , "DENT" ) OR EXCLUDE ( SUBJAREA , "Undefined" ) ) """

HOST = '127.0.0.1'  
PORT = 2937    
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

OP_ENTER_QUERY = 1
OP_DESIGNATE_LITTERATURE_RANGE = 2
OP_ANALYSIS = 3

while True:
    command = repr(client_socket.recv(1024).decode()).replace("\\x00", '')
    print(command)
    code_operation = command.split('//')[0]
       
    if OP_ENTER_QUERY == code_operation:
        Query = command.split('//')[1]
        InfoAbstract = AbstractReader(Query, True)

        client_socket.send("DONE".encode()) 
        pass
    elif OP_DESIGNATE_LITTERATURE_RANGE == code_operation:
        pass
    elif OP_ANALYSIS == code_operation:
        pass



client_socket.close()
exit(1)

InfoAbstract.Read((2011, 2021), "Renewable Energy")

Visualizer = BibliometricVisualizer(InfoAbstract)
Visualizer.ShowTrendOfYearsFromKeyword("machine learning")
Visualizer.ShowTrendOfJournalsFromKeyword("machine learning", 10, 30)
Visualizer.ShowWordCloudOfKeywords(50)
Visualizer.ShowNetworkOfKeywords(70)
Visualizer.ShowBibliometrics()