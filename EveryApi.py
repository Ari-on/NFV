import sys, yaml, json
import os
sys.path.insert(0, "./Libraries")
import splitTestCase
import WriteTestCase
import create_db_Excel
import spliting_testCase_basedOn_statusCode
import spliting_testCase_basedOn_EnumValues


def Yaml2Json(filepath):
		
	in_file = filepath
		
	inputFile = in_file.split(".")
	inputFile = inputFile[-2].split("\\")
	out_file = inputFile[-1] +'.json'
	
	with open(in_file) as file1:
		data = yaml.load(file1)
		
	with open("./outputFiles/" + out_file, 'w') as file2:
		json.dump(data, file2, indent=2)
	"""
		Function Name        : readSwagger
		Function Description : create DB and .csv file
		Inputs   : 
			FileName         : File name(.yaml file)
		Outputs  : 
			creates a (.csv file and one DB)
				
	"""
	
	create_db_Excel.readSwagger(in_file)
	
	"""
		Function Name        : .js file
		Function Description : create postman collection .json v1 file
		Inputs   : 
			FileName         : File name(.yaml file)
		Outputs  : 
			creates a (postman collection .json v1 file)
				
	"""
	swagger2postman(out_file)
	"""
		Function Name        : splitCollection
		Function Description : split the TCs of postman collection file
		Inputs   : 
			FileName         : File name(postman collection .json v1 file)
		Outputs  : 
			creates a (postman collection .json v1 file)
				
	"""
	splitTestCase.splitTestCase(out_file)
	spliting_testCase_basedOn_statusCode.split_testCases_using_status(in_file,out_file)
	spliting_testCase_basedOn_EnumValues.split_testCases_using_Enum(in_file,out_file)


	"""
		Function Name        : readNFVYaml
		Function Description : write the validation part in postman
		Inputs   : 
			FileName         : File name(postman collection .json v1 file)
		Outputs  : 
			creates a (postman collection .json v1 file)
				
	"""
	WriteTestCase.readNFVYaml(in_file)
	
	
def swagger2postman(out_file):
	os.system ("node ./Libraries/swagger2-postman.js "+ out_file)
	
	
if __name__ == '__main__':
	Yaml2Json(sys.argv[1])
