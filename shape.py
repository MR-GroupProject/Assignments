
class Shape:
    def __init__(self, name=None, label=None, vertex=None, face=None, scalar=None, vector=None):
        self.name = name
        self.label = label
        self.vertex = vertex
        self.face = face
        self.scalar = scalar
        self.vector = vector

for subfold in os.listdir(rootdir):
    d = os.path.join(rootdir, subfold)
    # print(subfold)
    for file in os.listdir(d):
        if file.endswith('.off'):
            tri = 0
            quad = 0
            obj_path = os.path.join(d, file)
            worksheet.write(row, 0, file)
            worksheet.write(row, 1, subfold)
            fp = open(obj_path)
            for i, line in enumerate(fp):
                if i == 1:
                    v = int(line.split(' ')[0])
                    f = int(line.split(' ')[1])
                    worksheet.write(row, 2, v)
                    worksheet.write(row, 3, f)

                if line.startswith('3 ') or line.startswith('4 '):
                    if line.startswith('3 '):
                        tri = 1
                    if line.startswith('4 '):
                        quad = 1
                if tri == 1 and quad == 1:
                    worksheet.write(row, 4, 'Mix')
                    break
            if tri == 1 and quad == 0:
                worksheet.write(row, 4, 'Tri')
            elif tri == 0 and quad == 1:
                worksheet.write(row, 4, 'Quad')
            # print(file)
            row += 1