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
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

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

            if (radioButton1.Checked)
            {
                textBox2.Enabled = false;
                textBox3.Enabled = false;
            }
            else if (radioButton2.Checked)
            {
                textBox2.Enabled = true;
                textBox3.Enabled = true;
            }

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
            clientSock.Send(Encoding.UTF8.GetBytes(text), 0, text.Length, SocketFlags.None);

            int n = clientSock.Receive(buf);
            string data = Encoding.UTF8.GetString(buf, 0, n);
            if(data != "Done")
            {
                ;
            }

            string json = null;
            using (System.IO.StreamReader sr = new System.IO.StreamReader("..\\..\\..\\..\\df\\resume_df.json"))
            {
                json = sr.ReadToEnd();
                sr.Close();
            }

            var jObject = JObject.Parse(json);
            this.richTextBox2.Text = jObject.ToString();
            int start_year = Convert.ToInt32(jObject["start_year"].ToString());
            int end_year = Convert.ToInt32(jObject["end_year"].ToString());
            
            var ArrayYear = Enumerable.Range(start_year, end_year - start_year + 1).Select(x => x.ToString()).ToArray();
            this.comboBox1.Items.AddRange(ArrayYear);
            this.comboBox2.Items.AddRange(ArrayYear);
            //JToken jToken = jObject["year_frequency"];

            this.comboBox3.Items.AddRange(jObject["journal_name"].ToObject<string[]>());
        }

        private void button2_Click(object sender, EventArgs e)
        {
            string t = this.comboBox3.Text;
            if (this.comboBox3.Text == "모든 저널")
            {
                t = "All";
            }
            string text = "2//" + this.comboBox1.Text + "**" + this.comboBox2.Text + "**" + t;
            clientSock.Send(Encoding.UTF8.GetBytes(text), 0, text.Length, SocketFlags.None);

            int n = clientSock.Receive(buf);
            string data = Encoding.UTF8.GetString(buf, 0, n);
            if (data != "Done")
            {
                ;
            }

        }

        private void button4_Click(object sender, EventArgs e)
        {

        }

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {
            if(radioButton1.Checked)
            {
                textBox2.Enabled = false;
                textBox3.Enabled = false;
            }
            else if(radioButton2.Checked)
            {
                textBox2.Enabled = true;
                textBox3.Enabled = true;
            }
        }

        private void radioButton2_CheckedChanged(object sender, EventArgs e)
        {
            if (radioButton1.Checked)
            {
                textBox2.Enabled = false;
                textBox3.Enabled = false;
            }
            else if (radioButton2.Checked)
            {
                textBox2.Enabled = true;
                textBox3.Enabled = true;
            }
        }
    }
}
