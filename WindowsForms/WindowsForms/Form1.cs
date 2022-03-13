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
using System.IO;
using System.Text.RegularExpressions;

namespace WindowsForms
{
    public partial class Form1 : Form
    {
        string CurrentDatagridviewPic;
        string CurrentDatagridviewCsv;
        Socket clientSock;
        Socket sock;
        byte[] buf = new byte[8192];
        ArrayList ArrayQuery = new ArrayList();
        int start_year, end_year;
        int len;
        JObject jObject;

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

            Process.Start("cmd.exe", "/C src\\__entry.py false");

            sock = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            IPEndPoint ep = new IPEndPoint(IPAddress.Any, 2937);
            sock.Bind(ep);
            sock.Listen(10);
            clientSock = sock.Accept();
        }
        ~Form1()
        {
            clientSock.Close();
            sock.Close();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if(richTextBox1.Text.Length <= 0)
            {
                MessageBox.Show("Invalid query input.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

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
            using (System.IO.StreamReader sr = new System.IO.StreamReader("df\\resume_df.json"))
            {
                json = sr.ReadToEnd();
                sr.Close();
            }

            jObject = JObject.Parse(json);
            start_year = Convert.ToInt32(jObject["start_year"].ToString());
            end_year = Convert.ToInt32(jObject["end_year"].ToString());
            len = Convert.ToInt32(jObject["len"].ToString());
            label1.Text = len.ToString() + " literatures retrieved.";

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

        public static FileInfo GetNewestFile(DirectoryInfo directory)
        {
            return directory.GetFiles()
                .Union(directory.GetDirectories().Select(d => GetNewestFile(d)))
                .OrderByDescending(f => (f == null ? DateTime.MinValue : f.LastWriteTime))
                .FirstOrDefault();
        }

        private void button4_Click(object sender, EventArgs e)
        {
            int n;
            if (radioButton1.Checked)
            {
                JToken jToken = jObject["year_frequency"];
                for (n = Convert.ToInt32(this.comboBox1.Text) - start_year; n < Convert.ToInt32(this.comboBox2.Text) - start_year; n++)
                {
                    if (Convert.ToInt32(jToken[n]) < 100)
                    {
                        var result = MessageBox.Show("A distortion can occur if the number of documents in n year is less than 100. Do you still want to proceed?", "Warning", MessageBoxButtons.OKCancel, MessageBoxIcon.Warning);
                        if (result == DialogResult.OK)
                        {
                            break;
                        }
                        else if (result == DialogResult.Cancel)
                        {
                            return;
                        }
                    }
                }
            }
            else
            {
                if (comboBox3.Text != "All")
                {
                    MessageBox.Show("For trend analysis by journal, the literature scope setting must be \"All\".", "Warning", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    return;
                }
            }


            string text = "3//";
            text += radioButton1.Checked ? "1**" : "2**";
            text += this.textBox1.Text;

            if (radioButton2.Checked)
            {
                text += "**" + this.textBox2.Text + "**" + this.textBox3.Text;
            }
            clientSock.Send(Encoding.UTF8.GetBytes(text), 0, text.Length, SocketFlags.None);

            n = clientSock.Receive(buf);
            string data = Encoding.UTF8.GetString(buf, 0, n);

            label10.Visible = false;
            CurrentDatagridviewPic = "pic\\" + GetNewestFile(new DirectoryInfo("pic")).Name;
            CurrentDatagridviewCsv = "report\\" + GetNewestFile(new DirectoryInfo("report")).Name;
            pictureBox1.Image = Bitmap.FromFile(CurrentDatagridviewPic);
            string[] Lines = File.ReadAllLines(CurrentDatagridviewCsv);

            dataGridView4.Rows.Clear();

            if(radioButton1.Checked)
            {
                string[] Names = { "Year", "Proportion", "Keyword frequency", "Total frequency", "Number of publications", "Rank" };
                for (int i = 0; i < Names.Length; i++)
                {
                    dataGridView4.Columns[i].Visible = true;
                    dataGridView4.Columns[i].HeaderText = Names[i];
                }
                foreach (var Line in Lines)
                {
                    string[] Token = Regex.Split(Line, "\",");
                    for(int j = 0; j < Token.Length; j++)
                    {
                        Token[j] = Token[j].Replace("\"", "");
                    }
                    dataGridView4.Rows.Add(Token);
                }
            }
            else if(radioButton2.Checked)
            {
                string[] Names = { "Journal", "Proportion", "Keyword frequency", "Total frequency", "Number of publications", "Rank" };
                for (int i = 0; i < Names.Length; i++)
                {
                    dataGridView4.Columns[i].Visible = true;
                    dataGridView4.Columns[i].HeaderText = Names[i];
                }
                foreach (var Line in Lines)
                {
                    string[] Token = Regex.Split(Line, "\",");
                    for (int j = 0; j < Token.Length; j++)
                    {
                        Token[j] = Token[j].Replace("\"", "");
                    }
                    dataGridView4.Rows.Add(Token);
                }
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
            text += comboBox4.Text[0] + "**";
            text += this.textBox4.Text;
            clientSock.Send(Encoding.UTF8.GetBytes(text), 0, text.Length, SocketFlags.None);

            int n = clientSock.Receive(buf);
            string data = Encoding.UTF8.GetString(buf, 0, n);
            label10.Visible = false;
            CurrentDatagridviewPic = "pic\\" + GetNewestFile(new DirectoryInfo("pic")).Name;
            CurrentDatagridviewCsv = "report\\" + GetNewestFile(new DirectoryInfo("report")).Name;
            pictureBox1.Image = Bitmap.FromFile(CurrentDatagridviewPic);
            string[] Lines = File.ReadAllLines(CurrentDatagridviewCsv);

            dataGridView4.Rows.Clear();

            if (radioButton3.Checked)
            {
                string[] Names = { "Word", "Frequency" };
                for (int i = 0; i < Names.Length; i++)
                {
                    dataGridView4.Columns[i].Visible = true;
                    dataGridView4.Columns[i].HeaderText = Names[i];
                }
                for(int i = Names.Length; i < dataGridView4.Columns.Count; i++)
                {
                    dataGridView4.Columns[i].Visible = false;
                }
                foreach (var Line in Lines)
                {
                    string[] Token = Regex.Split(Line, "\",");
                    for (int j = 0; j < Token.Length; j++)
                    {
                        Token[j] = Token[j].Replace("\"", "");
                    }
                    dataGridView4.Rows.Add(Token);
                }
            }
            else if (radioButton4.Checked)
            {
                string[] Names = { "First word", "Second word", "Co-occurrence frequency" };
                for (int i = 0; i < Names.Length; i++)
                {
                    dataGridView4.Columns[i].Visible = true;
                    dataGridView4.Columns[i].HeaderText = Names[i];
                }
                for (int i = Names.Length; i < dataGridView4.Columns.Count; i++)
                {
                    dataGridView4.Columns[i].Visible = false;
                }
                foreach (var Line in Lines)
                {
                    string[] Token = Regex.Split(Line, "\",");
                    for (int j = 0; j < Token.Length; j++)
                    {
                        Token[j] = Token[j].Replace("\"", "");
                    }
                    dataGridView4.Rows.Add(Token);
                }
            }
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            this.groupBox2.Enabled = false;
            this.groupBox3.Enabled = false;

            string query = null;
            try
            {
                using (System.IO.StreamReader sr = new System.IO.StreamReader("conf\\query_scopus.txt"))
                {
                    while ((query = sr.ReadLine()) != null)
                    {
                        if(!ArrayQuery.Contains(query))
                        {
                            if(query != "")
                            {
                                ArrayQuery.Add(query);
                                dataGridView3.Rows.Add(query);
                            }
                        }
                    }
                    sr.Close();
                }
            }
            catch
            {
                using (System.IO.StreamWriter sr = new System.IO.StreamWriter("conf\\query_scopus.txt"))
                {
                    sr.Close();
                }
            }
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            using (System.IO.StreamWriter sr = new System.IO.StreamWriter("conf\\query_scopus.txt", append: false))
            {
                foreach(var Query in ArrayQuery)
                {
                    if(Query != "")
                    {
                        sr.WriteLine(Query);
                    }
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

        private void button6_Click(object sender, EventArgs e)
        {
            
        }

        private void button7_Click(object sender, EventArgs e)
        {
            
        }

        private void dataGridView4_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }

        private void button7_Click_1(object sender, EventArgs e)
        {
            SaveFileDialog Dialog = new SaveFileDialog();
            Dialog.Title = "Save PNG File";
            Dialog.DefaultExt = "png";
            Dialog.FileName = "Figure.png";
            if (Dialog.ShowDialog() == DialogResult.OK)
            {
                File.Copy(CurrentDatagridviewPic, Dialog.FileName, true);
            }
        }

        private void button6_Click_1(object sender, EventArgs e)
        {
            
        }

        private void button7_Click_2(object sender, EventArgs e)
        {
            SaveFileDialog Dialog = new SaveFileDialog();
            Dialog.Title = "Save file";
            switch(tabControl2.SelectedIndex)
            {
                case 0:
                    Dialog.DefaultExt = "png";
                    Dialog.FileName = "Figure.png";
                    if (Dialog.ShowDialog() == DialogResult.OK)
                    {
                        File.Copy(CurrentDatagridviewPic, Dialog.FileName, true);
                    }
                    break;
                case 1:
                    Dialog.DefaultExt = "csv";
                    Dialog.FileName = "Analysis.csv";
                    if (Dialog.ShowDialog() == DialogResult.OK)
                    {
                        File.Copy(CurrentDatagridviewCsv, Dialog.FileName, true);
                    }
                    break;
            }
        }

        private void button5_Click(object sender, EventArgs e)
        {
            string text = "3//";
            if(radioButton5.Checked)
            {
                text += "5";
            }

            clientSock.Send(Encoding.UTF8.GetBytes(text), 0, text.Length, SocketFlags.None);

            int n = clientSock.Receive(buf);
            string data = Encoding.UTF8.GetString(buf, 0, n);

            label10.Visible = false;
            CurrentDatagridviewPic = "pic\\" + GetNewestFile(new DirectoryInfo("pic")).Name;
            CurrentDatagridviewCsv = "report\\" + GetNewestFile(new DirectoryInfo("report")).Name;
            pictureBox1.Image = Bitmap.FromFile(CurrentDatagridviewPic);
            string[] Lines = File.ReadAllLines(CurrentDatagridviewCsv);
        }
    }
}
