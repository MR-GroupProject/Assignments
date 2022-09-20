# import xlsxwriter module
import xlsxwriter
import os
 
# Workbook() takes one, non-optional, argument
# which is the filename that we want to create.
workbook = xlsxwriter.Workbook('filter.xlsx')
 
# The workbook object is then used to add new
# worksheet via the add_worksheet() method.
worksheet = workbook.add_worksheet()



 
# Use the worksheet object to write
# data via the write() method.
worksheet.write('A1', 'Name')
worksheet.write('B1', 'Class')
worksheet.write('C1', 'Vertices, Faces, Edges')
worksheet.write('D1', 'Type')
worksheet.write('E1', 'Bounding box')

rootdir = './LabeledDB_new'
row = 1
for subfold in os.listdir(rootdir):
    d = os.path.join(rootdir, subfold)
    #print(subfold)
    for file in os.listdir(d):
        if file.endswith('.off'):
            obj_path = os.path.join(d, file)
            worksheet.write(row, 0, file)
            worksheet.write(row, 1, subfold)
            fp = open(obj_path)
            for i, line in enumerate(fp):

                if i == 1:
                    worksheet.write(row, 2, line)

            #print(file)
            row += 1
 
# Finally, close the Excel file
# via the close() method.
workbook.close()

 