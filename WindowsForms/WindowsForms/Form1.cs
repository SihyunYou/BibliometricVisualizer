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
using System.Collections;

namespace WindowsForms
{
    public partial class Form1 : Form
    {
        Socket clientSock;
        Socket sock;
        byte[] buf = new byte[8192];
        ArrayList ArrayQuery = new ArrayList();

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

            //string Query = "TITLE-ABS-KEY ( \"Photovoltaic\" OR \"BIPV\" OR \"PV\" OR \"Irradiation\") AND TITLE-ABS-KEY ( \"solar\" OR \"sun\") AND TITLE-ABS-KEY ( \"machine learning\" OR \"prediction\" OR \"modeling\" ) AND ( EXCLUDE ( SUBJAREA , \"MATE\" ) OR EXCLUDE ( SUBJAREA , \"CHEM\" ) OR EXCLUDE ( SUBJAREA , \"CENG\" ) ) AND ( EXCLUDE ( SUBJAREA , \"MEDI\" ) OR EXCLUDE ( SUBJAREA , \"SOCI\" ) OR EXCLUDE ( SUBJAREA , \"AGRI\" ) OR EXCLUDE ( SUBJAREA , \"BIOC\" ) OR EXCLUDE ( SUBJAREA , \"BUSI\" ) OR EXCLUDE ( SUBJAREA , \"ECON\" ) OR EXCLUDE ( SUBJAREA , \"IMMU\" ) OR EXCLUDE ( SUBJAREA , \"NEUR\" ) OR EXCLUDE ( SUBJAREA , \"PHAR\" ) OR EXCLUDE ( SUBJAREA , \"HEAL\" ) OR EXCLUDE ( SUBJAREA , \"PSYC\" ) OR EXCLUDE ( SUBJAREA , \"ARTS\" ) OR EXCLUDE ( SUBJAREA , \"VETE\" ) OR EXCLUDE ( SUBJAREA , \"NURS\" ) OR EXCLUDE ( SUBJAREA , \"DENT\" ) OR EXCLUDE ( SUBJAREA , \"Undefined\" ) )";
            //richTextBox1.Text = Query;

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
            this.groupBox2.Enabled = false;
            this.groupBox3.Enabled = false;
            this.dataGridView1.Rows.Clear();
            this.dataGridView2.Rows.Clear();

            string text = "1//" + richTextBox1.Text + "**" + (checkBox1.Checked ? "1" : "0");
            clientSock.Send(Encoding.UTF8.GetBytes(text), 0, text.Length, SocketFlags.None);

            int n = clientSock.Receive(buf);
            string data = Encoding.UTF8.GetString(buf, 0, n);
            if(data != "DONE")
            {
                
            }

            if (!ArrayQuery.Contains(this.richTextBox1.Text))
            {
                ArrayQuery.Add(this.richTextBox1.Text);
            }

            string json = null;
            using (System.IO.StreamReader sr = new System.IO.StreamReader("..\\..\\..\\..\\df\\resume_df.json"))
            {
                json = sr.ReadToEnd();
                sr.Close();
            }

            var jObject = JObject.Parse(json);
            int start_year = Convert.ToInt32(jObject["start_year"].ToString());
            int end_year = Convert.ToInt32(jObject["end_year"].ToString());
            JToken jToken = jObject["year_frequency"];
            
            var ArrayYear = Enumerable.Range(start_year, end_year - start_year + 1).Select(x => x.ToString()).ToArray();
            
            this.comboBox3.Items.AddRange(jObject["journal_name"].ToObject<string[]>());
            this.groupBox2.Enabled = true;

            this.comboBox1.Items.AddRange(ArrayYear);
            this.comboBox2.Items.AddRange(ArrayYear);

            for (n = start_year; n <= end_year; n++)
            {
                string[] rows = { (end_year + start_year - n).ToString(), jToken[end_year - n].ToString() };
                dataGridView1.Rows.Add(rows);
            }

            for (n = 0; n < jObject["journal_name"].Count(); n++)
            {
                string[] rows = { jObject["journal_name"][n].ToString(), jObject["journal_frequency"][n].ToString() };
                dataGridView2.Rows.Add(rows);
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            this.groupBox3.Enabled = false;
            string text = "2//" + this.comboBox1.Text + "**" + this.comboBox2.Text + "**" + this.comboBox3.Text;
            clientSock.Send(Encoding.UTF8.GetBytes(text), 0, text.Length, SocketFlags.None);

            int n = clientSock.Receive(buf);
            string data = Encoding.UTF8.GetString(buf, 0, n);
            if (data != "DONE")
            {
                ;
            }
            this.groupBox3.Enabled = true;
        }

        private void button4_Click(object sender, EventArgs e)
        {
            string text = "3//";
            text += radioButton1.Checked ? "1**" : "2**";
            text += this.textBox1.Text;

            if(radioButton2.Checked)
            {
                text += "**" + this.textBox2.Text + "**" + this.textBox3.Text;
            }
            clientSock.Send(Encoding.UTF8.GetBytes(text), 0, text.Length, SocketFlags.None);

            int n = clientSock.Receive(buf);
            string data = Encoding.UTF8.GetString(buf, 0, n);
            if (data != "DONE")
            {
                ;
            }
            else
            {
                pictureBox1.Image = Bitmap.FromFile("..\\..\\..\\..\\pic\\" + (radioButton1.Checked ? "1.png" : "2.png"));
            }
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

        private void radioButton4_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void button3_Click(object sender, EventArgs e)
        {
            string text = "3//";
            text += radioButton3.Checked ? "3**" : "4**";
            text += this.textBox4.Text;
            clientSock.Send(Encoding.UTF8.GetBytes(text), 0, text.Length, SocketFlags.None);

            int n = clientSock.Receive(buf);
            string data = Encoding.UTF8.GetString(buf, 0, n);
            if (data != "DONE")
            {
                ;
            }
            else
            {
                pictureBox1.Image = Bitmap.FromFile("..\\..\\..\\..\\pic\\" + (radioButton3.Checked ? "3.png" : "4.png"));
            }
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            this.groupBox2.Enabled = false;
            this.groupBox3.Enabled = false;

            string query = null;
            try
            {
                using (System.IO.StreamReader sr = new System.IO.StreamReader("..\\..\\..\\..\\log\\query_scopus.txt"))
                {
                    while ((query = sr.ReadLine()) != null)
                    {
                        if(!ArrayQuery.Contains(query))
                        {
                            dataGridView3.Rows.Add(query);
                            ArrayQuery.Add(query);
                        }
                    }
                    sr.Close();
                }
            }
            catch
            {
                using (System.IO.StreamWriter sr = new System.IO.StreamWriter("..\\..\\..\\..\\log\\query_scopus.txt"))
                {
                    sr.Close();
                }
            }
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            using (System.IO.StreamWriter sr = new System.IO.StreamWriter("..\\..\\..\\..\\log\\query_scopus.txt", append: false))
            {
                foreach(var Query in ArrayQuery)
                {
                    sr.WriteLine(Query);
                }
            }
        }

        private void dataGridView3_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            if(e.ColumnIndex == 1)
            {
                ArrayQuery.Remove(dataGridView3.Rows[e.RowIndex].Cells[0].Value.ToString());
                dataGridView3.Rows.Remove(dataGridView3.Rows[e.RowIndex]);
            }
            else if(e.ColumnIndex == 2)
            {
                richTextBox1.Text = dataGridView3.Rows[e.RowIndex].Cells[0].Value.ToString();
            }
        }
    }
}
