#Convert query to model
#--------------------------------------
import re
import os

pn = "itz.scs" #Project Name
tableName = "MicrobiomeComposition"
folderName = '_'.join([x.lower() for x in re.findall('[A-Z][^A-Z]*', tableName)])
modelName = tableName
className = tableName
baseName = ''.join([tableName[0].lower() + tableName[1:]])
apiName = folderName.replace('_','-')

# Generate Pk,FK,unique to set,get data in db
pk = {"Id": "Integer"}
uk = {"Name": "String"}
fk = [{"ItemId": "String","ItemSku": "String"},{"ItemId": "String","VariantId": "String"}]
createdBy = "Abdul Baasit"
#--------------------------------------


parent_dir = "D:/DevTools/Automata/SpringBootAutomation/output"

print("Create a controller , service & repo ")

path = os.path.join(parent_dir, folderName)

if os.path.exists(path):
   print("Folder is not empty")
else:
    os.mkdir(path)

print(path)
# ----------------
print("Create controller class")
writeData = open(path + "/" + className + "Controller.java", 'w+')
#Create a Controller
writeData.write("package com."+pn+".use_cases."+folderName+";\n\n")
writeData.write("import org.springframework.data.domain.Page;\nimport org.springframework.web.bind.annotation.*;\nimport org.springframework.beans.factory.annotation.Autowired;\n")
writeData.write("import org.springframework.http.ResponseEntity;\nimport javax.servlet.http.HttpServletRequest;\nimport java.util.List;\n")
writeData.write("import org.springframework.http.HttpStatus;\nimport org.modelmapper.ModelMapper;\nimport org.modelmapper.TypeToken;\n")
writeData.write("import com."+pn+".helpers.common.results.*;\nimport com."+pn+".helpers.common.token.*;\n")
writeData.write("import com."+pn+".use_cases."+folderName+".dao.*;\n")
writeData.write("import com."+pn+".persistence.models." + modelName + ";\n\n")
writeData.write("@RestController\n@RequestMapping(\"${spring.base.path}\")\n")
writeData.write("public class " + className + "Controller {\n")
writeData.write("\n")
# Add a Annotation
writeData.write("\t@Autowired\n")
writeData.write("\t" + className + "Service ser;\n")
writeData.write("\t@Autowired\n")
writeData.write("\tClaimsSet claimsSet;\n")
writeData.write("\n")
# Create
writeData.write("\t@PostMapping(value =\"/"+apiName+"\")\n")
writeData.write("\tpublic ResponseEntity<?> masterSet(HttpServletRequest request,@RequestBody "+className+"Dao getVal) throws Exception {\n")
writeData.write("\t\tClaimsDao claimsDao = claimsSet.getClaimsDetailsAfterSet(request.getHeader(\"Authorization\"));\n")
writeData.write("\t\tif(ser.getPk2(getVal.get"+list(uk.keys())[0]+"())!=null)\n")
writeData.write("\t\t\tthrow new Exception(getVal.get"+list(uk.keys())[0]+"()+\" Value Already Set\");\n")
writeData.write("\t\tser.setData(new ModelMapper().map(getVal,"+modelName+".class));\n")
writeData.write("\t\treturn new ResponseEntity<>(new ReportDao(\"Added Successfully\",true), HttpStatus.OK);\n")
writeData.write("\t}\n\n")
# AddAll
writeData.write("\t@PostMapping(value =\"/"+apiName+"/add-all\")\n")
writeData.write("\tpublic ResponseEntity<?> masterSetAddAll(HttpServletRequest request, @RequestBody List<"+className+"Dao> getVal) throws Exception {\n")
writeData.write("\t\tClaimsDao claimsDao = claimsSet.getClaimsDetailsAfterSet(request.getHeader(\"Authorization\"));\n")
writeData.write("\t\tser.setAllData(new ModelMapper().map(getVal, new TypeToken<List<"+modelName+">>(){}.getType()));\n")
writeData.write("\t\treturn new ResponseEntity<>(new ReportDao(\"Imported Successfully\", true), HttpStatus.OK);\n")
writeData.write("\t}\n\n")
# DeleteAll
writeData.write("\t@PostMapping(value =\"/"+apiName+"/delete-all\")\n")
writeData.write("\tpublic ResponseEntity<?> masterSetDeleteAll(HttpServletRequest request, @RequestBody List<"+className+"IdDao> getVal) throws Exception {\n")
writeData.write("\t\tClaimsDao claimsDao = claimsSet.getClaimsDetailsAfterSet(request.getHeader(\"Authorization\"));\n")
writeData.write("\t\tser.delAllData(new ModelMapper().map(getVal, new TypeToken<List<"+modelName+">>(){}.getType()));\n")
writeData.write("\t\treturn new ResponseEntity<>(new ReportDao(\"Deleted Successfully\", true), HttpStatus.OK);\n")
writeData.write("\t}\n\n")
# update
writeData.write("\t@PutMapping(value =\"/"+apiName+"\")\n")
writeData.write("\tpublic ResponseEntity<?> masterUpdate(HttpServletRequest request,@RequestBody "+className+"IdDao getVal) throws Exception {\n")
writeData.write("\t\tClaimsDao claimsDao = claimsSet.getClaimsDetailsAfterSet(request.getHeader(\"Authorization\"));\n")
writeData.write("\t\t"+modelName+" setVal = ser.getPk1(getVal.get"+list(pk.keys())[0]+"());\n")
writeData.write("\t\tif(setVal!=null){\n")
writeData.write("\t\t\tif(!setVal.get"+list(uk.keys())[0]+"().equals(getVal.get"+list(uk.keys())[0]+"()) && ser.getPk2(getVal.get"+list(uk.keys())[0]+"())!=null)\n")
writeData.write("\t\t\t\tthrow new Exception(getVal.get"+list(uk.keys())[0]+"()+\" Value Already Set\");\n")
writeData.write("\t\t\tsetVal.setUpBy(claimsDao.getUsr());\n")
writeData.write("\t\t\tsetVal.setIsActive(getVal.getIsActive());\n")
writeData.write("\t\t\tsetVal.set"+list(uk.keys())[0]+"(getVal.get"+list(uk.keys())[0]+"());\n")
writeData.write("\t\t\tsetVal.setDescription(getVal.getDescription());\n")
writeData.write("\t\t\tser.setData(setVal);\n")
writeData.write("\t\t}else{\n")
writeData.write("\t\t\tthrow new Exception(getVal.get"+list(uk.keys())[0]+"()+\" Value Not Found To Update\");\n")
writeData.write("\t\t}\n")
writeData.write("\t\treturn new ResponseEntity<>(new ReportDao(\"Updated Successfully\",true), HttpStatus.OK);\n")
writeData.write("\t}\n\n")
# Delete
writeData.write("\t@DeleteMapping(value =\"/"+apiName+"/{id}\")\n")
writeData.write("\tpublic ResponseEntity<?> masterDelete(HttpServletRequest request\n")
writeData.write("\t\t\t,@PathVariable(name=\"id\") "+list(pk.values())[0]+" id) throws Exception {\n")
writeData.write("\t\tClaimsDao claimsDao = claimsSet.getClaimsDetailsAfterSet(request.getHeader(\"Authorization\"));\n")
writeData.write("\t\t"+modelName+" getVal = ser.getPk1(id);\n")
writeData.write("\t\tif(getVal == null){\n")
writeData.write("\t\t\tthrow new Exception(id+\" Not Found To Delete\");\n")
writeData.write("\t\t}else{\n")
writeData.write("\t\t\tser.delData(getVal);\n")
writeData.write("\t\t}\n")
writeData.write("\t\treturn new ResponseEntity<>(new ReportDao(\"Deleted Successfully\",true), HttpStatus.OK);\n")
writeData.write("\t}\n\n")
# Get by id
writeData.write("\t@GetMapping(value =\"/"+apiName+"/{id}\")\n")
writeData.write("\tpublic ResponseEntity<?> masterGet(HttpServletRequest request\n")
writeData.write("\t\t\t,@PathVariable(name=\"id\") "+list(pk.values())[0]+" id) throws Exception {\n")
writeData.write("\t\tClaimsDao claimsDao = claimsSet.getClaimsDetailsAfterSet(request.getHeader(\"Authorization\"));\n")
writeData.write("\t\t"+modelName+" getVal = ser.getPk1(id);\n")
writeData.write("\t\tif(getVal == null)\n")
writeData.write("\t\t\tthrow new Exception(id+\" Not Found To Get\");\n")
writeData.write("\t\treturn new ResponseEntity<>(new ResultDao( new ModelMapper().map(getVal, "+className+"Dao.class),\"Car Brand Fetched Successfully\",true), HttpStatus.OK);\n")
writeData.write("\t}\n\n")
# Get all
writeData.write("\t@GetMapping(value =\"/"+apiName+"\")\n")
writeData.write("\tpublic ResponseEntity<?> masterGetAll(HttpServletRequest request\n")
writeData.write("\t\t\t,@RequestParam(required=false,name=\"start\",defaultValue= \"1\")int pageNumber\n")
writeData.write("\t\t\t,@RequestParam(required=false,name=\"limit\",defaultValue= \"25\")int pageSize\n")
writeData.write("\t\t\t,@RequestParam(required=false,name=\"searchKey\",defaultValue= \"-1\")String searchKey\n")
writeData.write("\t\t\t,@RequestParam(required=false,name=\"orderBy\",defaultValue= \"-1\")String orderBy\n")
writeData.write("\t\t\t,@RequestParam(required=false,name=\"sortOrder\",defaultValue= \"-1\")int sortOrder\n")
writeData.write("\t\t\t,@RequestParam(required=false,name=\"isPagination\",defaultValue= \"true\")Boolean isPagination) throws Exception {\n")
writeData.write("\t\tClaimsDao claimsDao = claimsSet.getClaimsDetailsAfterSet(request.getHeader(\"Authorization\"));\n")
writeData.write("\t\tList<"+modelName+"> getVal;\n")
writeData.write("\t\tlong totalCount = 0;\n")
writeData.write("\t\tif(isPagination){\n")
writeData.write("\t\t\tPage<"+modelName+"> getAllWtPg = ser.getAllDataByPg(pageNumber-1,pageSize-(pageNumber-1),searchKey);\n")
writeData.write("\t\t\tgetVal = getAllWtPg.getContent();\n")
writeData.write("\t\t\ttotalCount = getAllWtPg.getTotalElements();\n")
writeData.write("\t\t}else{\n")
writeData.write("\t\t\tgetVal = ser.getAllData();\n")
writeData.write("\t\t\ttotalCount = getVal.size();\n")
writeData.write("\t\t\tpageNumber = 1;\n")
writeData.write("\t\t\tpageSize= Math.toIntExact(totalCount);\n")
writeData.write("\t\t}\n")
writeData.write("\t\treturn new ResponseEntity<>(new ResultsDao(new ModelMapper().map(getVal,\n")
writeData.write("\t\t\t\tnew TypeToken<List<"+className+"IdDao>>() {\n")
writeData.write("\t\t\t\t}.getType()),pageNumber,pageSize,totalCount), HttpStatus.OK);\n")
writeData.write("\t}\n")
writeData.write("}\n")

# service - > getPk1,getPk2,delData,setData,getAllData,getAllDataByPg