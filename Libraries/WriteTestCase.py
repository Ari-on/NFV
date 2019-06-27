import sys , yaml ,json
import os
import csv
def readNFVYaml(inputFile):
	global space
	yamlFile = inputFile
	
	jsonFile = yamlFile.split(".")
	jsonInputFile = jsonFile[-2].split("\\")
	inputFile = jsonInputFile[-1] +'.json'
	
	space = "    "
	TagList = []
	with open(yamlFile) as file:
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
							for item in schitem:
								if "properties" in item:
									pro = data["paths"][path]["get"]["responses"][resp]["schema"]["properties"]
									for T in pro:
										if T == "id":
											pass
										else:
											TagList.append(T)
								elif "items" in item:
									properties = data["paths"][path]["get"]["responses"][resp]["schema"][item]["properties"]
									for propertie in properties:
										GetTags = data["paths"][path]["get"]["responses"][resp]["schema"][item]["properties"][propertie]#["properties"]
										for tags in GetTags:
											if "properties" in tags:
												properties1 = data["paths"][path]["get"]["responses"][resp]["schema"][item]["properties"][propertie]["properties"]
												for x in properties1:	
													if x == "id":
															pass
													else:
														TagList.append(x)
											else:
												pass
								# else:
								# 	properties2 = data["paths"][path]["get"]["responses"][resp]["schema"]["properties"]
								# 	for tag in properties2:
								# 		if tag == "id":
								# 			pass
								# 		else:
								# 			TagList.append(tag)
												
	TagList =  list(set(TagList))										
	JsonFile = open("./outputFiles/"+inputFile,'r+')
	jsonContent = json.load(JsonFile)
	for content in jsonContent['requests']:
		url = content['url']

		#We don't need 'Tests' for DELETE..
		if content['method'] == "DELETE":
			pass
		else :
			content['events'] = [] 
			content['events'].append({ #Default Content for 'Tests'
				"listen": "test",
				"script": {"type": "text/javascript",
				"exec":[]
				}
				})
			content['events'][0]['script']['exec'].append("var jsonData = pm.response.json();")
			content['events'][0]['script']['exec'].append("pm.test(\"Status code is -  \"+ jsonData['statuscode'] , function() {")
			content['events'][0]['script']['exec'].append(space + "pm.expect(jsonData['statuscode']).to.be.eql(" + "200" + ")")
			content['events'][0]['script']['exec'].append("});",)
			content['events'][0]['script']['exec'].append("")
			content['events'][0]['script']['exec'].append("pm.test(\"Body matches string\", function () {")
			for x in TagList: #Adding the TAG values
				content['events'][0]['script']['exec'].append(space+"pm.expect(pm.response.text()).to.include(\""+ x +"\""");")
		
			content['events'][0]['script']['exec'].append("});")
			content['events'][0]['script']['exec'].append("")
			content['events'][0]['script']['exec'].append("pm.test(\"isString\" ,function() {")
			content['events'][0]['script']['exec'].append(space + "if  (pm.response.json().res){")
			content['events'][0]['script']['exec'].append(2*space + "jsonData = pm.response.json().res; " +'\n' +space+"}")
			content['events'][0]['script']['exec'].append(space + "else{")
			content['events'][0]['script']['exec'].append(2*space + "var jsonData = [pm.response.json()];" +'\n'+space+ "}")
			content['events'][0]['script']['exec'].append(space+"for (i = 0; i < jsonData.length; i++) {")
			content['events'][0]['script']['exec'].append(space+"}")
			content['events'][0]['script']['exec'].append("})")


		
			with open("./outputFiles/"+inputFile, 'w') as outfile:
				json.dump(jsonContent, outfile,indent=4,ensure_ascii=False)
				
	preRequest(inputFile)
	
def preRequest(inputFile):

	jsnFile = inputFile.split(".")
	jsnFile = jsnFile[-2] +'.csv'
	
	JsonFile = open("./outputFiles/"+inputFile,'r+')
	jsonContent = json.load(JsonFile)
	rowNo = 0
	for content in jsonContent['requests']:
		url = content['url']
		if 'events' not in content:
			content['events'] = []
			eventCheck = 0
		else:
			eventCheck = 1
			pass
		rowNo = rowNo + 1

		url_List = []
		raw_List = []
		final_List = []
		csv_List = []

		file = open("./outputFiles/"+jsnFile,'r')#BWM_API_swagger/Location_API_swagger

		data = csv.reader(file)
		csv_List = []
		for row in data:
			csv_List.append(row)

		csv_List = csv_List[0]
		pathVariables = content['pathVariables']
		if len(pathVariables) == 0:
			pass
		else:
			for key,value in pathVariables.items():
				if key not in url_List:
					url_List.append(key)

		if '?' in url:
			url_copy = url.split('?')[1]
			url_copy = url_copy.split('&')
			for query in url_copy:
				query = query.split('=')[1]
				query = query.replace('{{','')
				query = query.replace('}}','')
				if query not in url_List:
					url_List.append(query)
		if type(content['rawModeData']) == unicode:
			rawModeData = json.loads(content['rawModeData'])
			if rawModeData == "string":
				pass
			else:
				for key,value in rawModeData.items():
					if type(value) == unicode:
						value = value.replace('{{','')
						value = value.replace('}}','')
						raw_List.append(value)
					else:
						pass
						# list1 = req_body(key,value,final_List,'')
						# for element in list1:
							# if element not in raw_List:
								# raw_List.append(element)
		else:
			pass

		query = url.split('{{port}}')[1]
		if content['method'] == 'POST':
			readUrl   = 'read_csv'
			rowNoCopy = 1 
		else:
			readUrl   = 'read_db'
			rowNoCopy = rowNo
		crcrQuery = query.replace('&','?')

		if content['method'] == 'POST':
			execContent = space*1+"url: 'localhost:8081/"+readUrl+'/'+str(rowNoCopy)+"?query="+crcrQuery+"',",
		else:
			execContent = space*1+"url: 'localhost:8081/"+readUrl+'/'+str(rowNoCopy)+"?query="+crcrQuery+"',",

		content['events'].append({   #Default content for 'Pre-Requests'
			"listen": "prerequest",
			"script": {"type": "text/javascript",
			"exec":[
			space*1+"var list = [];",
			space*1+"pm.sendRequest({",
			execContent,
			space*1+"method: 'GET',",
			space*1+"header: 'Content-Type:application/x-www-form-urlencoded',",
			space*1+"}, function (err, res) {",
			space*1+"var response_json = res.json();",
			space*1+"if(list.length === 0){",
			space*1+"var key;",
			space*1+"for (key in response_json) {",
			space*2+"if (response_json.hasOwnProperty(key))",
			space*2+"{",
			space*3+"list.push(response_json[key]);",
			space*2+"}",
			space*1+"}",
			"",
			space+"var currentData = list.shift();",
			"",
			]}
			})
		
		for urlElement in url_List:
			content['events'][eventCheck]['script']['exec'].append(space+"pm.environment.set("+'"'+urlElement+'"'+",currentData."+urlElement+");")
			
		content['events'][eventCheck]['script']['exec'].append(space+'}')
		content['events'][eventCheck]['script']['exec'].append('});')
		with open("./outputFiles/"+inputFile, 'w') as joutfile:
			json.dump(jsonContent, joutfile,indent=4,ensure_ascii=False)