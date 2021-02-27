import pandas as pd

def export_pandas_to_sheet(dataframe, file_name = "New Excel.xlsx", sheet_name = "New Sheet"):
	dataframe.to_excel(file_name, sheet_name = sheet_name, index = false)

def export_pandas_to_workbook(sheets_reference, file_name = "New Excel.xlsx"):
	xlsxWriter = pd.ExcelWriter(file_name, engine='xlsxwriter')
	
	for sheet_name in sheets_reference.keys():
		sheets_reference[sheet_name].to_excel(writer, sheet_name = sheet_name, index = False)

	writer.save()

def import_workbook_as_pandas(file_name):
	# sheet_name = None means to read every sheet
	return pd.read_excel(file_name, sheet_name=None)

def import_sheet_as_pandas(file_name, sheet_name, index_col = None):
	# sheet_name = None means to read every sheet
	# index_col is the col used as index (default to integers)
	return pd.read_excel(file_name, sheet_name=sheet_name, index_col = index_col)
