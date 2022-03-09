# -*- coding: utf-8 -*-
from bibliometric_visualizer import BibliometricVisualizer
from abstract_reader import AbstractReader
import socket
import traceback

#Query = 'TITLE-ABS-KEY ( "Photovoltaic" OR "BIPV" OR "PV" OR "Irradiation") AND TITLE-ABS-KEY ( "solar" OR "sun") AND TITLE-ABS-KEY ( "machine learning" OR "prediction" OR "modeling" ) AND ( EXCLUDE ( SUBJAREA , "MATE" ) OR EXCLUDE ( SUBJAREA , "CHEM" ) OR EXCLUDE ( SUBJAREA , "CENG" ) ) AND ( EXCLUDE ( SUBJAREA , "MEDI" ) OR EXCLUDE ( SUBJAREA , "SOCI" ) OR EXCLUDE ( SUBJAREA , "AGRI" ) OR EXCLUDE ( SUBJAREA , "BIOC" ) OR EXCLUDE ( SUBJAREA , "BUSI" ) OR EXCLUDE ( SUBJAREA , "ECON" ) OR EXCLUDE ( SUBJAREA , "IMMU" ) OR EXCLUDE ( SUBJAREA , "NEUR" ) OR EXCLUDE ( SUBJAREA , "PHAR" ) OR EXCLUDE ( SUBJAREA , "HEAL" ) OR EXCLUDE ( SUBJAREA , "PSYC" ) OR EXCLUDE ( SUBJAREA , "ARTS" ) OR EXCLUDE ( SUBJAREA , "VETE" ) OR EXCLUDE ( SUBJAREA , "NURS" ) OR EXCLUDE ( SUBJAREA , "DENT" ) OR EXCLUDE ( SUBJAREA , "Undefined" ) )'

try:
    HOST = '127.0.0.1'  
    PORT = 2937    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(client_socket)
    print("Connection succeeded.")

    OP_ENTER_QUERY = 1
    OP_DESIGNATE_LITTERATURE_RANGE = 2
    OP_ANALYSIS = 3

    InfoAbstract = None
    Visualizer = None

    while True:
        command = repr(client_socket.recv(1024).decode('utf-8', 'ignore')).replace("\\x00", '').strip('\'')
        print(command)
        code_operation = int(command.split('//')[0])
        parameter_chunk = command.split('//')[1]

        if OP_ENTER_QUERY == code_operation:
            list_parameter = parameter_chunk.split('**')
            InfoAbstract = AbstractReader(list_parameter[0],
                                                True if list_parameter[1] == "1" else False)
            client_socket.send("DONE".encode())
            pass
        elif OP_DESIGNATE_LITTERATURE_RANGE == code_operation:
            list_parameter = parameter_chunk.split('**')
            InfoAbstract.Read((int(list_parameter[0]), int(list_parameter[1])), list_parameter[2])
            Visualizer = BibliometricVisualizer(InfoAbstract)
            client_socket.send("DONE".encode())
            pass
        elif OP_ANALYSIS == code_operation:
            list_parameter = parameter_chunk.split('**')
            code_operation_detail = int(list_parameter[0])
            if code_operation_detail == 1:
                Visualizer.ShowTrendOfYearsFromKeyword(list_parameter[1])
            elif code_operation_detail == 2:
                Visualizer.ShowTrendOfJournalsFromKeyword(list_parameter[1], int(list_parameter[2]), int(list_parameter[3]))
            elif code_operation_detail == 3:
                Visualizer.ShowWordCloudOfKeywords(int(list_parameter[1]), int(list_parameter[2]))
            elif code_operation_detail == 4:
                Visualizer.ShowNetworkOfKeywords(int(list_parameter[1]), int(list_parameter[2]))
            elif code_operation_detail == 5:
                Visualizer.ShowBibliometrics()
            client_socket.send(Visualizer.filename.encode())
        else:
            print("Wrong operation code returned.")
except Exception as e:
    print(e)
    traceback.print_exc()
    import time
    time.sleep(300)

client_socket.close()
exit(1)

InfoAbstract = AbstractReader(Query, True)
InfoAbstract.Read((2011, 2021), "Renewable Energy")

Visualizer = BibliometricVisualizer(InfoAbstract)
Visualizer.ShowTrendOfYearsFromKeyword("machine learning")
Visualizer.ShowTrendOfJournalsFromKeyword("machine learning", 10, 30)
Visualizer.ShowWordCloudOfKeywords(50)
Visualizer.ShowNetworkOfKeywords(70)
Visualizer.ShowBibliometrics()