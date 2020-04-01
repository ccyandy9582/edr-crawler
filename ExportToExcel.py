import pandas as pd
import os.path
import xlsxwriter

#check the file is exists or not
#if not it will be created
def isFileExist():
    if not os.path.exists('doctor.xlsx'):
        workbook = xlsxwriter.Workbook('doctor.xlsx')
        worksheet = workbook.add_worksheet()
        workbook.close()

# set up data
def insert(data):
    dataFrame = pd.DataFrame(data)
    return dataFrame

# write data into the sheet
def writeToExcel(dataFrame):
    excel = pd.ExcelWriter("doctor.xlsx", engine='xlsxwriter')
    dataFrame.to_excel(excel, sheet_name='Sheet1')
    excel.save()