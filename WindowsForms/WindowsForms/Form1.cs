using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net;
using System.Net.Sockets;
using System.Diagnostics;

namespace WindowsForms
{
    public partial class Form1 : Form
    {
        Socket clientSock;
        Socket sock;
        byte[] buf = new byte[8192];

        public Form1()
        {
            InitializeComponent();

            string Query = "TITLE-ABS-KEY ( \"Photovoltaic\" OR \"BIPV\" OR \"PV\" OR \"Irradiation\") AND TITLE-ABS-KEY ( \"solar\" OR \"sun\") AND TITLE-ABS-KEY ( \"machine learning\" OR \"prediction\" OR \"modeling\" ) AND ( EXCLUDE ( SUBJAREA , \"MATE\" ) OR EXCLUDE ( SUBJAREA , \"CHEM\" ) OR EXCLUDE ( SUBJAREA , \"CENG\" ) ) AND ( EXCLUDE ( SUBJAREA , \"MEDI\" ) OR EXCLUDE ( SUBJAREA , \"SOCI\" ) OR EXCLUDE ( SUBJAREA , \"AGRI\" ) OR EXCLUDE ( SUBJAREA , \"BIOC\" ) OR EXCLUDE ( SUBJAREA , \"BUSI\" ) OR EXCLUDE ( SUBJAREA , \"ECON\" ) OR EXCLUDE ( SUBJAREA , \"IMMU\" ) OR EXCLUDE ( SUBJAREA , \"NEUR\" ) OR EXCLUDE ( SUBJAREA , \"PHAR\" ) OR EXCLUDE ( SUBJAREA , \"HEAL\" ) OR EXCLUDE ( SUBJAREA , \"PSYC\" ) OR EXCLUDE ( SUBJAREA , \"ARTS\" ) OR EXCLUDE ( SUBJAREA , \"VETE\" ) OR EXCLUDE ( SUBJAREA , \"NURS\" ) OR EXCLUDE ( SUBJAREA , \"DENT\" ) OR EXCLUDE ( SUBJAREA , \"Undefined\" ) )";
            richTextBox1.Text = Query;

            sock = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            IPEndPoint ep = new IPEndPoint(IPAddress.Any, 2937);
            sock.Bind(ep);
            sock.Listen(10);

            //Process.Start("cmd.exe", "/C ..\\..\\..\\..\\src\\entry.py");
            clientSock = sock.Accept();
        }
        ~Form1()
        {
            clientSock.Close();
            sock.Close();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string text = "1//" + richTextBox1.Text;
            clientSock.Send(Encoding.UTF8.GetBytes(text), 0, text.Length, SocketFlags.None);  // echo

            int n = clientSock.Receive(buf);
            string data = Encoding.UTF8.GetString(buf, 0, n);
            richTextBox2.Text = data;
        }
    }
}
