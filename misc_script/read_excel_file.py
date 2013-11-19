import xlrd

wb = xlrd.open_workbook('Team_Info.xls')
fso_dict = {}
sh = wb.sheet_by_index(0)
for rownum in range(1, sh.nrows):
    fso_dict[rownum] = sh.row_values(rownum)

f = open('user_dict.txt', 'w')
f.write(str(fso_dict))
f.close()
