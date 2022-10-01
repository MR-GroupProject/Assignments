from openpyxl import load_workbook
import pymeshlab


wb = load_workbook('../filter.xlsx')
ws = wb['Sheet1']
ws.cell(1, 6).value = 'Bounding Box x'
ws.cell(1, 7).value = 'Bounding Box y'
ws.cell(1, 8).value = 'Bounding Box z'

ms = pymeshlab.MeshSet()

for row in range(2, ws.max_row+1):
    file = ws.cell(row, 1).value
    label = ws.cell(row, 2).value
    ms.load_new_mesh("../LabeledDB_new/" + label + "/" + file)
    ws.cell(row, 6).value = ms.current_mesh().bounding_box().dim_x()
    ws.cell(row, 7).value = ms.current_mesh().bounding_box().dim_y()
    ws.cell(row, 8).value = ms.current_mesh().bounding_box().dim_z()
    ms.clear()

wb.save('../filter.xlsx')

print('done')
