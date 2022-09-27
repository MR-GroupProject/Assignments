# import xlsxwriter module
import xlsxwriter
import os
import convertor

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
worksheet.write('C1', 'Vertices')
worksheet.write('D1', 'Faces')
worksheet.write('E1', 'Type of Faces')
worksheet.write('F1', 'Bounding box')

root_dir = './LabeledDB_new'
row = 1
for sub_fold in os.listdir(root_dir):
    d = os.path.join(root_dir, sub_fold)

    for file in os.listdir(d):
        
        if file.endswith('.off') or file.endswith('.ply'):
            worksheet.write(row, 0, file)
            worksheet.write(row, 1, sub_fold)
            obj_path = os.path.join(d, file)
            file_path = obj_path
            if file.endswith('.ply'):
                file_path = convertor.convert_ply_into_off(obj_path)  # convert the .ply file into .off file
            v, f = 0, 0
            tri = 0
            quad = 0

            maxX = 0
            minX = 0
            maxY = 0 
            minY = 0
            maxZ = 0
            minZ = 0

            fp = open(file_path)
            next(fp)  # skip first line
            for i, line in enumerate(fp):
                if i == 0:
                    v = int(line.split(' ')[0])
                    f = int(line.split(' ')[1])
                    worksheet.write(row, 2, v)
                    worksheet.write(row, 3, f)

                elif v > 0:
                    v -= v  # read lines of vertices
                    curX = float(line.split(' ')[0])
                    curY = float(line.split(' ')[1])
                    curZ = float(line.split(' ')[2])

                    if curX < minX:
                        minX = curX
                    else:
                        maxX = curX
                    
                    if curY < minY:
                        minY = curY
                    else:
                        maxY = curY

                    if curZ < minZ:
                        minZ = curZ
                    else:
                        maxZ = curZ

                    continue

                else:  # read lines of faces
                    if tri == 1 and quad == 1:
                        worksheet.write(row, 4, 'Mix')
                        break
                    if line.startswith('3 '):
                        tri = 1
                    if line.startswith('4 '):
                        quad = 1
                    if quad == 0:
                        worksheet.write(row, 4, 'Tri')
                    elif tri == 0:
                        worksheet.write(row, 4, 'Quad')
                
                length = maxX - minX
                width = maxY - minY
                height = maxZ - minZ
                bBoxSize = str(length) + ' ' + str(width) + ' ' + str(height)
                worksheet.write(row, 5, bBoxSize)

            row += 1
            print(file)

# Finally, close the Excel file
# via the close() method.
workbook.close()
