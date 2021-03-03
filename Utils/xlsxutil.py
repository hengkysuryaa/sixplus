import pandas as pd
import numpy as np 

# Usage : convert_normal_array_to_pandas({'columnName' : array})
def convert_normal_array_to_pandas(arrDict):
	df = pd.DataFrame(columns = [*arrDict])
	for key in arrDict:
		df[key] = arrDict[key]
	return df

def convert_pandas_to_normal_array(df):	
	columns = list(df) 

	arrDict = {}
	  
	for column in columns: 
	    arrDict[column] = df[column].to_list()

	return arrDict

def export_pandas_to_sheet(dataframe, file_name = "New Excel.xlsx", sheet_name = "New Sheet"):
	dataframe.to_excel(file_name, sheet_name = sheet_name, index = False)

def export_pandas_to_workbook(sheets_reference, file_name = "New Excel.xlsx"):
	xlsxWriter = pd.ExcelWriter(file_name, engine='xlsxwriter')
	
	for sheet_name in sheets_reference.keys():
		sheets_reference[sheet_name].to_excel(xlsxWriter, sheet_name = sheet_name, index = False)

	xlsxWriter.save()

def import_workbook_as_pandasDict(file_name):
	# sheet_name = None means to read every sheet
	return pd.read_excel(file_name, sheet_name=None)

def import_sheet_as_pandas(file_name, sheet_name, index_col = None):
	# sheet_name = None means to read every sheet
	# index_col is the col used as index (default to integers)
	return pd.read_excel(file_name, sheet_name=sheet_name, index_col = index_col)
