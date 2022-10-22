import features as ft
import xlsxwriter
import os


# create data sheet
def create_table(path, head=None, sheet=None):
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    if sheet is not None:
        worksheet.set_vba_name(sheet)
    if head is not None:
        for i in range(len(head)):
            worksheet.write(0, i, head[i])
    return workbook, worksheet


def write_data(data, worksheet, start_row=None, start_column=None):
    row, column = 0, 0
    if start_row is not None:
        row = start_row
    if start_column is not None:
        column = start_column
    for i in range(len(data)):  # row count
        for j in range(len(data[i])):  # column count
            worksheet.write(row + i, column + j, data[i][j])
