import pandas as pd
import numpy as np

# Usage : convert_normal_array_to_pandas({'columnName' : array})
def convert_normal_array_to_pandas(arrDict):
	df = pd.DataFrame(columns = [*arrDict])
	for key in arrDict:
		if(arrDict[key] == []):
			df[key] = df[key].fillna('')
		else:
			df[key] = arrDict[key]
	return df

# Usage : convert_normal_array_to_pandas({'columnName' : array})
def convert_pandas_to_normal_array(df):	
	columns = list(df) 

	arrDict = {}
	  
	for column in columns: 
	    arrDict[column] = df[column].to_list()

	return arrDict


def export_pandas_to_sheet(dataframe, file_name = "New Excel.xlsx", sheet_name = "New Sheet", use_title = False, title = ""):
	#dataframe.to_excel(file_name, sheet_name = sheet_name, index = False)
	writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
	dataframe.to_excel(writer, sheet_name = sheet_name, startrow = 1, index=False)


	workbook  = writer.book
	worksheet = writer.sheets[sheet_name]

	header_format = workbook.add_format({'bold': True, 'valign': 'top', 'fg_color': '#D7E4BC','border': 1})
	for col_num, value in enumerate(dataframe.columns.values):
		worksheet.write(1, col_num, value, header_format)

	if(use_title):
		bold = workbook.add_format({'bold': True})
		worksheet.write(0, 0, title, bold)
		writer.save()

def export_pandas_to_workbook(sheets_reference, file_name = "New Excel.xlsx"):
	xlsxWriter = pd.ExcelWriter(file_name, engine='xlsxwriter')
	
	for sheet_name in sheets_reference.keys():
		sheets_reference[sheet_name].to_excel(xlsxWriter, sheet_name = sheet_name, index = False, na_filter = False)

	xlsxWriter.save()


def column_check(x):
	if 'unnamed' in x.lower():
		return False
	return True


def import_workbook_as_pandasDict(file_name):
	# sheet_name = None means to read every sheet
	return pd.read_excel(file_name, sheet_name=None)

def import_sheet_as_pandas(file_name, sheet_name, index_col = None, skiprows = 0):
	# sheet_name = None means to read every sheet
	# index_col is the col used as index (default to integers)
	cols_to_exclude = ['unnamed']
	return pd.read_excel(file_name, sheet_name=sheet_name, index_col = index_col, na_filter = False, usecols = column_check, skiprows = skiprows)

# dc = import_sheet_as_pandas("Lembar Penilaian MS1100 K1 Semester 1 2020-2021.xlsx", "MS1100 K1 Semester 1 2020-2021", skiprows = 1)
# print(dc)
# print(len(dc.columns))