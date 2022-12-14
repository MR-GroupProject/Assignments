import os
from tools import dataset
from tools import convertor


head = ['Name', 'Class', 'Vertices', 'Faces', 'Type of faces']
workbook, worksheet = dataset.create_table('../data/filter.xlsx', labels=head)

root_dir = '../LabeledDB_new'
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

            fp = open(file_path)
            next(fp)  # skip first line
            for i, line in enumerate(fp):
                if i == 0:
                    v = int(line.split(' ')[0])
                    f = int(line.split(' ')[1])
                    worksheet.write(row, 2, v)
                    worksheet.write(row, 3, f)
                    continue

                if v > 0:
                    v -= v  # lines of vertices

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

            row += 1
            print(file)

# Finally, close the Excel file
workbook.close()
