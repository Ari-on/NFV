# This file will read the swagger.yaml file and fetch the tags of the body
# and write it a text file for further use.
import os, sys, ntpath, pymongo, time
import yaml
import xlwt, xlrd,csv
from xlwt import Workbook
from xlrd import open_workbook
from pymongo import MongoClient

#class swaggerToExcel:

def readSwagger(yaml_file):
	global outFileName, inFileName, outputFileName, dictListKeys
	inFileName = yaml_file
	fileExists = os.path.exists(inFileName)
	outFileName = ntpath.basename(inFileName)
	#print("ntpath",outFileName)
	outputFileName = outFileName.strip(".yaml")
	outFileName = './outputFiles/' + outputFileName + ".csv"

	if not fileExists:
		flag = 0
		#print ("File not found! Check the file path")
	else:
		flag = 1
		# Opens the swagger.yaml file in read mode
		swaggerFile = open(inFileName,'r')

		# Loads the yaml file into a list
		yamlContent = yaml.load(swaggerFile)
		# print (yamlContent
		#print ("File read\n")

		# Calls the function to add the tags to the text file
	writeToExcel(yaml_file)
def writeToExcel(yaml_file):
	global dictListKeys
	dictListKeys = []
	with open(yaml_file) as file:
		data = yaml.load(file)
		pathsInfo = data["paths"]
		for path in pathsInfo:
			if "get" in data["paths"][path]:
				responses = data["paths"][path]["get"]["responses"]
				for resp in responses:
					if "200" in resp:
						items = data["paths"][path]["get"]["responses"][resp]
						if "schema" not in items:
							pass
						else:
							schitem = data["paths"][path]["get"]["responses"][resp]["schema"]
							if "$ref" in schitem:
								for k,v in schitem.items():
									refvalue = v.split("/")
									refvalue = refvalue[-1]
								for defTag in  data["definitions"]:
									if defTag == refvalue:
										for tagsInDef in data["definitions"][defTag]["properties"]:
											dictListKeys.append(tagsInDef)
							else:
								for item in schitem:
									if "items" not in item:
										properties = data["paths"][path]["get"]["responses"][resp]["schema"]#["properties"]
										for tag in properties:
											if "properties" in tag:
												properties1 = data["paths"][path]["get"]["responses"][resp]["schema"]["properties"]
												for x in properties1:	
													if tag == "id":
															pass
													else:
														dictListKeys.append(x)
											else:
												pass
									else:
										properties = data["paths"][path]["get"]["responses"][resp]["schema"][item]["properties"]
										for propertie in properties:
											GetTags = data["paths"][path]["get"]["responses"][resp]["schema"][item]["properties"][propertie]
											if "properties" in GetTags:
												GetTags1 = data["paths"][path]["get"]["responses"][resp]["schema"][item]["properties"][propertie]["properties"]
												for tags in GetTags1:
													if tags == "id":
														pass
													else:
														dictListKeys.append(tags)
											else:
												for tags in GetTags:
													if tags == "id":
														pass
													else:
														dictListKeys.append(tags)

												
	dictListKeys =  list(set(dictListKeys))
	with open(outFileName, 'wb') as csvfile:
		spamwriter = csv.writer(csvfile)
		spamwriter.writerow(dictListKeys)
	if dictListKeys == []:
		pass
	else:
		createDatabase(dictListKeys)
def createDatabase(dictListKeys):
	
	collName = outputFileName

	# Connection to mongodb
	client = pymongo.MongoClient("mongodb://localhost:27017/mecTest")
	db = client["NFVTest"]

	# This will read the excel file and insert it into the database
	if collName not in db.collection_names():
		# print (collName, "is created")
		with open(outFileName, 'rb') as csvfile:
			spamreader = csv.reader(csvfile)
			for row in spamreader:
		  # number_of_rows = sheet.nrows
			  number_of_columns = len(row)
			  # print (number_of_columns)
			  dictList = []
			  dictListValue = []
			  for column in range(number_of_columns):
				value = " "
				dictListValue.append(value)
				dictList = dict(zip(dictListKeys, dictListValue))
			  insertRecord = db[collName].insert_one(dictList)
			  # print ("Record inserted... Check the DB")
	else:
		# print (collName, "is exists")
		with open(outFileName, 'rb') as csvfile:
			spamreader = csv.reader(csvfile)
			for row in spamreader:
		  # number_of_rows = sheet.nrows
			  number_of_columns = len(row)
			  # print (number_of_columns)
			  dictList = []
			  dictListValue = []
			  for column in range(number_of_columns):
				value = ""
				dictListValue.append(value)
				dictList = dict(zip(dictListKeys, dictListValue))
			  insertRecord = db[collName].insert_one(dictList)
			  # print ("Record inserted... Check the DB")