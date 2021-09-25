import os
import xlrd
import csv

dir_path_xls = '../../static/data/sensors/xls/'
dir_path_csv = '../../static/data/sensors/csv/'
file_list = os.listdir(dir_path_xls)
for filename in file_list:

    wb = xlrd.open_workbook(dir_path_xls+filename)
    sh = wb.sheet_by_name(wb.sheet_names()[0])
    your_csv_file = open(dir_path_csv+filename[:-4]+'.csv', 'w', encoding='utf8')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()
