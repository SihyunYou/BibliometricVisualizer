import xlsxwriter
import pandas
import pickle

s = 'df_ab'
with open(s + '.pkl', 'rb') as f:
    data = pickle.load(f)
writer = pandas.ExcelWriter(s + '.xlsx', engine='xlsxwriter')
data.to_excel(excel_writer=writer, sheet_name='Sheet1')
writer.save()
pandas.set_option('display.max_columns', None)
print(data)
