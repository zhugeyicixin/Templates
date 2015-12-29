import xlsxwriter

workbook = xlsxwriter.Workbook('chart.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write(0,1,'hi')

# for i in xrange(1000):
# 	worksheet.write(0, i, i)

workbook.close()