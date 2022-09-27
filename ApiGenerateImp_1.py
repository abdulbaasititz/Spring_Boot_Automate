import re
#Convert query to model
#--------------------------------------
pn = "itz.base" #Project Name
tableName = "" #No Need
moduleName = "test_module"
cstQry = 0
addAllOpt = 1
delAllOpt = 1
createdBy = "Abdul Baasit"
# -------------------------------------

# Find Table name and other attributes
pk={};pkType="";uk={};ukType=""
# -------------------
file = open("GetData", "r")
name = []
flag = 0
check = ""
get = ""

columnName=[]
columnType=[]
i =0
toggle=-1
for line in file:
    fields = line.rstrip('\n').split(" ")
    for word in fields :
        check = word.rstrip(',()')

        if check != "NOT" and check != "NULL" and check != "CREATE" and check != "KEY"  and check != "AUTO_INCREMENT":
            #print(check)
            get = 1
            if check == "TABLE":
                tableName = fields[i + 1]
                get=0
            if check == "UNIQUE":
                ukTemp = fields[i - 3].rstrip(',();')
                ukTemp = ukTemp.replace('(','')
                uk[ukTemp] = 'String'
                ukType = fields[i - 2].rstrip(',();')
                continue
            if check == "PRIMARY":
                pkTemp = fields[len(fields)-1].rstrip(',();')
                pkTemp = pkTemp.replace('(','')
                pk[pkTemp]='Integer'
                break;
        if get ==1:
            if tableName == word:
                toggle = 0
                continue
            if toggle == 0:
                columnName.append(check)
                toggle = 1
            else:
                columnType.append(check)
                toggle = 0
            get =0
        i=i+1


print("tablename :"+tableName)
print("primaryKey :"+str(pk))
print("uniqueKey :"+str(uk))
print("uniqueKeyType :"+ukType)
print("Column Name and Column Type below :")
print(columnName)
print(columnType)
file.close()
# ----------------------

# Should be underscore snake_case
folderName = '_'.join([x.lower() for x in re.findall('[A-Z][^A-Z]*', tableName)])
# it should be same name which create in model folder #- PascalCase
modelName = tableName
# common name for all cntrl,service - PascalCase
className = tableName
# object name for class camelCase
baseName = ''.join([tableName[0].lower() + tableName[1:]])
# SHould be hipen snake_case
apiName = folderName.replace('_','-')
# Generate Pk,FK,unique to set,get data in db
# pk = {"Id": "Integer"}
# uk = {"Name": "String"}
#fk = [{"ItemId": "String","ItemSku": "String"},{"ItemId": "String","VariantId": "String"}]

#--------------------------------------
# Create Path and Folder
import os

parent_dir = "D:/DevTools/Automata/SpringBootAutomation/output"

path = os.path.join(parent_dir, folderName)
if not os.path.exists(path):
    os.mkdir(path)

daoPath=os.path.join(path, "dao")
if not os.path.exists(daoPath):
    os.mkdir(daoPath)

print("Created folder path is "+path)

# --------------------------
print("Create model class")
i=0
get = 0
idSet = 0
splitBy = " "
writeData = open("output/"+className+".java", 'w+')
writeData.write("package com." + pn + ".persistence.models;\n")
writeData.write("import com." + pn + ".helpers.utils.JwtUtil;\n")
writeData.write("import com." + pn + ".persistence.models.common.Auditable;\n")
writeData.write("import lombok.Getter;\nimport lombok.Setter;\nimport javax.persistence.*;\n\n")
writeData.write("@Entity @Table(name=\"" + tableName + "\") \n")
writeData.write("@Getter @Setter\n")
if "UpAt" in columnName:
    writeData.write("public class " + className + " extends Auditable<String> {\n")
else:
    writeData.write("public class "+className+"  {\n")
for name in columnName:
    if idSet == 0 and name == "ID" or name == "(Id" :
        idSet = 1
        writeData.write("\t@Id\n")
        writeData.write("\t@GeneratedValue(strategy=GenerationType.IDENTITY)\n")
        if name == "(Id" :
            name = name.split('(')[1]
    columnTypeCk = columnType[i].split("(")[0]
    #print(columnTypeCk)
    if len(columnType[i].split("(")) > 1:
       writeData.write("\t@Size(max=")
       writeData.write(columnType[i].split("(")[1] + ")\n")
    if columnTypeCk == "int" or columnTypeCk == "smallint" or columnTypeCk == "bigint":
        if idSet == 1:
            writeData.write("\tprivate Integer " + ''.join([name[0].lower() + name[1:]]) + " = 0;\n")
            idSet = 2
        else :
            if (get == 0 and name == "CrBy"):
                writeData.write("\tprivate Integer crBy = JwtUtil.usr;\n")
                get = 1;
                i = i + 1;
                continue;
            writeData.write("\tprivate Integer " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "tinyint" or columnTypeCk == "bit":
        writeData.write("\tprivate Boolean " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "float" or columnTypeCk == "amount":
        writeData.write("\tprivate Float " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "double":
        writeData.write("\tprivate Double " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "date" :
        if (name != "CrAt" and name != "UpAt"):
            writeData.write("\tprivate Date " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "timestamp" :
        if (name != "CrAt" and name != "UpAt"):
            writeData.write("\tprivate Timestamp " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    else:
        if (get == 0 and name == "CrBy"):
            writeData.write("\tprivate String crBy = JwtUtil.usr;\n")
            get = 1;i=i+1;
            continue;
        writeData.write("\tprivate String "+''.join([name[0].lower()+name[1:]])+";\n")
    i=i+1

writeData.write("}")
writeData.close()
# ---------

print("Create dao class")
get=0
i=0
idSet = 0
splitBy = " "
writeData = open(path + "/dao/" + className + "Dao.java", 'w+')
writeData.write("package com."+pn+".use_cases."+moduleName+"."+folderName+".dao;\n\n")
writeData.write("import lombok.Getter;\nimport lombok.Setter;\nimport javax.validation.constraints.Size;\n\n")
writeData.write("@Getter @Setter\n")
writeData.write("public class "+className+"Dao {\n")
for name in columnName:
    if idSet == 0 and name == "ID" or name == "(Id" :
        idSet = 1
        if name == "(Id" :
            name = name.split('(')[1]
    columnTypeCk = columnType[i].split("(")[0]
    if (name == "CrAt" or name == "CrBy" or name == "UpAt" or name == "UpBy"):
        i=i+1;continue;
    if len(columnType[i].split("(")) > 1:
       writeData.write("\t@Size(max=")
       writeData.write(columnType[i].split("(")[1] + ")\n")
    #print(columnTypeCk)
    if columnTypeCk == "int" or columnTypeCk == "smallint" or columnTypeCk == "bigint":
        writeData.write("\tprivate Integer " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "tinyint" or columnTypeCk == "bit":
        writeData.write("\tprivate Boolean " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "float" or columnTypeCk == "amount":
        writeData.write("\tprivate Float " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "double":
        writeData.write("\tprivate Double " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "date":
        writeData.write("\tprivate Date " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    else:
        writeData.write("\tprivate String "+''.join([name[0].lower()+name[1:]])+";\n")
    i=i+1;

writeData.write("}")
writeData.close()

if cstQry == 1 :
    # ---------------------------
    print("Create custom pojo & dao class")
    splitBy = " "
    writeDataCstPojo = open(path+"/dao/"+className+"CstPojo.java", 'w+')
    writeDataCstDao = open(path+"/dao/"+className+"CstDao.java", 'w+')
    # writeData = open(path + "/dao/" + className + "Dao.java", 'w+')
    idSet = 0
    writeDataCstPojo.write("package com." + pn + ".persistence.dao;\n\n")
    writeDataCstDao.write("package com."+pn+".use_cases."+folderName+".dao;\n\n")
    writeDataCstDao.write("import lombok.Getter;\nimport lombok.Setter;\n\n")
    writeDataCstDao.write("@Getter @Setter\n")
    writeDataCstPojo.write("public interface "+className+"CstPojo {\n")
    writeDataCstDao.write("public class "+className+"CstDao {\n")
    # ----------------------
    rx = re.compile(r'(?<=[a-z])(?=[A-Z])')
    columnNameSpt = [rx.sub(' ', word) for word in columnName]
    print(columnNameSpt)
    selectQry=""
    tables=[tableName]
    jn = 1
    i = 0
    # print("Select ",end="")
    selectQry = "Select "
    for name in columnName:
        if (name == "CrAt" and name == "CrBy" and name == "UpAt" and name == "UpBy"):
            i=i+1;continue;
        check = rx.sub(' ', name).split(' ')
        columnTypeCk = columnType[i].split("(")[0]
        # print(columnTypeCk)
        if name == "Id" or name == "(Id":
            # print("t1."+word+",",end="")
            selectQry = selectQry+"t1.Id,"
            writeDataCstPojo.write("\tInteger getId();\n")
            writeDataCstDao.write("\tprivate Integer id;\n")
        elif len(check) == 1 :
            # print("t1."+word+",",end="")
            selectQry = selectQry + "t1." + name + ","
            if columnTypeCk == "tinyint" or columnTypeCk == "bit":
                writeDataCstPojo.write("\tBoolean get" + name + "();\n")
                writeDataCstDao.write("\tprivate Boolean " + ''.join([name[0].lower() + name[1:]]) + ";\n")
            elif columnTypeCk == "float" or columnTypeCk == "amount":
                writeDataCstPojo.write("\tFloat get" + name + "();\n")
                writeDataCstDao.write("\tprivate Float " + ''.join([name[0].lower() + name[1:]]) + ";\n")
            elif columnTypeCk == "double":
                writeDataCstPojo.write("\tDouble get" + name + "();\n")
                writeDataCstDao.write("\tprivate Double " + ''.join([name[0].lower() + name[1:]]) + ";\n")
            else:
                writeDataCstPojo.write("\tString get" + name + "();\n")
                writeDataCstDao.write("\tprivate String " + ''.join([name[0].lower() + name[1:]]) + ";\n")
        elif len(check) > 1:
            if check[1] == "Id":
                jn = str(int(jn) + 1)
                # print("t"+jn+"."+word+",", end="")
                selectQry = selectQry + "t" + jn + ".Id as " + check[0] + "Id,"
                writeDataCstPojo.write("\tInteger get"+check[0]+"Id();\n")
                writeDataCstDao.write("\tprivate Integer "+ ''.join([check[0][0].lower() + check[0][1:]]) +"Id;\n")
                selectQry = selectQry + "t" + jn + ".name as " + check[0] + "Name,"
                writeDataCstPojo.write("\tString get"+check[0]+"Name();\n")
                writeDataCstDao.write("\tprivate String "+''.join([check[0][0].lower() + check[0][1:]])+"Name;\n")
                tables.append(check[0])
            elif len(check) > 2 and check[len(check)-1] == "Id":
                jn = str(int(jn) + 1)
                # print("t"+jn+"."+word+",", end="")
                # selectQry = selectQry + "t" + jn + ".Id as " + check[0]+check[1] + "Id,"
                selectQry = selectQry + "t" + jn + ".Id as " + ''.join(check) + ","
                # print(selectQry)
                # print(''.join([check[0][0].lower() + check[0][1:]]))
                # writeDataCstPojo.write("\tInteger get" + check[0]+check[1] + "Id();\n")
                writeDataCstPojo.write("\tInteger get" + ''.join(check) + "();\n")
                # writeDataCstDao.write("\tprivate Integer " + ''.join([check[0][0].lower() + check[0][1:]])+check[1] + "Id;\n")
                writeDataCstDao.write(
                    "\tprivate Integer " + ''.join([check[0][0].lower() + check[0][1:]]) + ''.join(map(str.capitalize, check[1:])) + ";\n")
                selectQry = selectQry + "t" + jn + ".name as " + ''.join(check[:-1]) + "Name,"
                writeDataCstPojo.write("\tString get" + ''.join(check[:-1]) + "Name();\n")
                writeDataCstDao.write("\tprivate String "+''.join([check[0][0].lower() + check[0][1:]])+''.join(check[1:-1])+"Name;\n")
                tables.append(''.join(check[:-1]))
        i=i+1

    selectQry = selectQry.rstrip(',')+' from '
    jn=1
    print(tables)
    for name in tables:
        if name == tableName:
            selectQry = selectQry + " " + name + " t1 "
            # print(word)
        else:
            jn = str(int(jn) + 1)
            selectQry = selectQry + " join " + name + " t" + jn
            # print(word)

    if int(jn)>1:
        jn = 1
        selectQry = selectQry + " where"
        for name in tables:
            if name == tableName:
                continue
            else:
                selectQry = selectQry + " t1." + name + "Id ="
                jn = str(int(jn) + 1)
                selectQry = selectQry + " t" + jn + ".Id "
                if int(jn) < len(tables):
                    selectQry = selectQry + " And"

    print("Custom query is "+selectQry)

    writeDataCstPojo.write("}")
    writeDataCstPojo.close()
    writeDataCstDao.write("}")
    writeDataCstDao.close()
# --------------------



print("Create controller class")
writeData = open(path + "/" + className + "Controller.java", 'w+')
#Create a Controller
writeData.write("package com."+pn+".use_cases."+moduleName+"."+folderName+";\n\n")
writeData.write("import org.springframework.data.domain.Page;\nimport org.springframework.web.bind.annotation.*;\nimport org.springframework.beans.factory.annotation.Autowired;\n")
writeData.write("import org.springframework.http.ResponseEntity;\nimport javax.servlet.http.HttpServletRequest;\nimport java.util.List;\n")
writeData.write("import org.springframework.http.HttpStatus;\nimport org.modelmapper.ModelMapper;\nimport org.modelmapper.TypeToken;\n")
writeData.write("import com."+pn+".helpers.common.results.*;\nimport com."+pn+".helpers.common.token.*;\n")
writeData.write("import com."+pn+".use_cases."+moduleName+"."+folderName+".dao.*;\n")
writeData.write("import com."+pn+".persistence.models."+moduleName+"."+modelName+";\n\n")
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
if cstQry == 1 :
    writeData.write("\tpublic ResponseEntity<?> masterSet(HttpServletRequest request,@RequestBody "+className+"CstDao getVal) throws Exception {\n")
else:
    writeData.write("\tpublic ResponseEntity<?> masterSet(HttpServletRequest request,@RequestBody " + className + "Dao getVal) throws Exception {\n")
writeData.write("\t\tClaimsDao claimsDao = claimsSet.getClaimsDetailsAfterSet(request.getHeader(\"Authorization\"));\n")
if len(uk) > 0:
    writeData.write("\t\tif(ser.getPk2(getVal.get"+list(uk.keys())[0]+"())!=null)\n")
    writeData.write("\t\t\tthrow new Exception(getVal.get"+list(uk.keys())[0]+"()+\" Value Already Set\");\n")
writeData.write("\t\tser.setData(new ModelMapper().map(getVal,"+modelName+".class));\n")
writeData.write("\t\treturn new ResponseEntity<>(new ReportDao(\"Added Successfully\",true), HttpStatus.OK);\n")
writeData.write("\t}\n\n")
if addAllOpt == 1 :
    # AddAll
    writeData.write("\t@PostMapping(value =\"/"+apiName+"/add-all\")\n")
    writeData.write("\tpublic ResponseEntity<?> masterSetAddAll(HttpServletRequest request, @RequestBody List<"+className+"Dao> getVal) throws Exception {\n")
    writeData.write("\t\tClaimsDao claimsDao = claimsSet.getClaimsDetailsAfterSet(request.getHeader(\"Authorization\"));\n")
    writeData.write("\t\tser.setAllData(new ModelMapper().map(getVal, new TypeToken<List<"+modelName+">>(){}.getType()));\n")
    writeData.write("\t\treturn new ResponseEntity<>(new ReportDao(\"Imported Successfully\", true), HttpStatus.OK);\n")
    writeData.write("\t}\n\n")
if delAllOpt == 1:
    # DeleteAll
    writeData.write("\t@PostMapping(value =\"/"+apiName+"/delete-all\")\n")
    writeData.write("\tpublic ResponseEntity<?> masterSetDeleteAll(HttpServletRequest request, @RequestBody List<"+className+"Dao> getVal) throws Exception {\n")
    writeData.write("\t\tClaimsDao claimsDao = claimsSet.getClaimsDetailsAfterSet(request.getHeader(\"Authorization\"));\n")
    writeData.write("\t\tser.delAllData(new ModelMapper().map(getVal, new TypeToken<List<"+modelName+">>(){}.getType()));\n")
    writeData.write("\t\treturn new ResponseEntity<>(new ReportDao(\"Deleted Successfully\", true), HttpStatus.OK);\n")
    writeData.write("\t}\n\n")
# update
writeData.write("\t@PutMapping(value =\"/"+apiName+"\")\n")
if cstQry == 1 :
    writeData.write("\tpublic ResponseEntity<?> masterUpdate(HttpServletRequest request,@RequestBody "+className+"CstDao getVal) throws Exception {\n")
else:
    writeData.write("\tpublic ResponseEntity<?> masterUpdate(HttpServletRequest request,@RequestBody "+className+"Dao getVal) throws Exception {\n")

writeData.write("\t\tClaimsDao claimsDao = claimsSet.getClaimsDetailsAfterSet(request.getHeader(\"Authorization\"));\n")
writeData.write("\t\t"+modelName+" setVal = ser.getPk1(getVal.get"+list(pk.keys())[0]+"());\n")
writeData.write("\t\tif(setVal!=null){\n")
if len(uk) > 0:
    writeData.write("\t\t\tif(!setVal.get" + list(uk.keys())[0] + "().equals(getVal.get" + list(uk.keys())[
        0] + "()) && ser.getPk2(getVal.get" + list(uk.keys())[0] + "())!=null)\n")
    writeData.write("\t\t\t\tthrow new Exception(getVal.get"+list(uk.keys())[0]+"()+\" Value Already Set\");\n")
    writeData.write("\t\t\tsetVal.set"+list(uk.keys())[0]+"(getVal.get"+list(uk.keys())[0]+"());\n")
# writeData.write("\t\t\tsetVal.setDescription(getVal.getDescription());\n")
writeData.write("\t\t\tser.setData(setVal);\n")
writeData.write("\t\t}else{\n")
writeData.write("\t\t\tthrow new Exception(\"Value Not Found To Update\");\n")
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
writeData.write("\t\treturn new ResponseEntity<>(new ResultDao( new ModelMapper().map(getVal, "+className+"Dao.class),\"Fetched Successfully\",true), HttpStatus.OK);\n")
writeData.write("\t}\n\n")
# Get all
if len(uk) > 0:
    writeData.write("\t@GetMapping(value =\"/"+apiName+"\")\n")
    writeData.write("\tpublic ResponseEntity<?> masterGetAll(HttpServletRequest request\n")
    writeData.write("\t\t\t,@RequestParam(required=false,name=\"start\",defaultValue= \"1\")int pageNumber\n")
    writeData.write("\t\t\t,@RequestParam(required=false,name=\"limit\",defaultValue= \"25\")int pageSize\n")
    writeData.write("\t\t\t,@RequestParam(required=false,name=\"searchKey\",defaultValue= \"\")String searchKey\n")
    writeData.write("\t\t\t,@RequestParam(required=false,name=\"orderBy\",defaultValue= \"-1\")String orderBy\n")
    writeData.write("\t\t\t,@RequestParam(required=false,name=\"sortOrder\",defaultValue= \"-1\")int sortOrder\n")
    writeData.write("\t\t\t,@RequestParam(required=false,name=\"isPagination\",defaultValue= \"true\")Boolean isPagination) throws Exception {\n")
    writeData.write("\t\tClaimsDao claimsDao = claimsSet.getClaimsDetailsAfterSet(request.getHeader(\"Authorization\"));\n")
    writeData.write("\t\tList<"+modelName+"> getVal;\n")
    writeData.write("\t\tlong totalCount;\n")
    writeData.write("\t\tif(isPagination){\n")

    if cstQry == 1 :
        writeData.write("\t\t\tPage<"+modelName+"CstPojo> getAllWtPg = ser.getAllDataByPg(pageNumber-1,pageSize-(pageNumber-1),searchKey);\n")
        writeData.write("\t\t\ttotalCount = getAllWtPg.getTotalElements();\n")
        writeData.write("\t\t\treturn new ResponseEntity<>(new ResultsDao(getAllWtPg.getContent(),pageNumber,pageSize,totalCount), HttpStatus.OK);\n")
        writeData.write("\t\t}else{\n")
    else:
        writeData.write("\t\t\tPage<"+modelName+"> getAllWtPg = ser.getAllDataByPg(pageNumber-1,pageSize-(pageNumber-1),searchKey);\n")
        writeData.write("\t\t\tgetVal = getAllWtPg.getContent();\n")
        writeData.write("\t\t\ttotalCount = getAllWtPg.getTotalElements();\n")
        writeData.write("\t\t\treturn new ResponseEntity<>(new ResultsDao(new ModelMapper().map(getVal,\n")
        writeData.write("\t\t\t\t\tnew TypeToken<List<"+className+"Dao>>() {\n")
        writeData.write("\t\t\t\t\t}.getType()),pageNumber,pageSize,totalCount), HttpStatus.OK);\n")
        writeData.write("\t\t}else{\n")

    writeData.write("\t\t\tgetVal = ser.getAllData();\n")
    writeData.write("\t\t\ttotalCount = getVal.size();\n")
    writeData.write("\t\t\tpageNumber = 1;\n")
    writeData.write("\t\t\tpageSize= Math.toIntExact(totalCount);\n")
    writeData.write("\t\t\treturn new ResponseEntity<>(new ResultsDao(new ModelMapper().map(getVal,\n")
    writeData.write("\t\t\t\t\tnew TypeToken<List<"+className+"Dao>>() {\n")
    writeData.write("\t\t\t\t\t}.getType()),pageNumber,pageSize,totalCount), HttpStatus.OK);\n")
    writeData.write("\t\t}\n")
else:
    writeData.write("\t@GetMapping(value =\"/"+apiName+"\")\n")
    writeData.write("\tpublic ResponseEntity<?> masterGetAll(HttpServletRequest request) throws Exception {\n")
    writeData.write(
        "\t\tClaimsDao claimsDao = claimsSet.getClaimsDetailsAfterSet(request.getHeader(\"Authorization\"));\n")
    writeData.write("\t\t\tList<" + modelName + "> getVal = ser.getAllData();\n")
    writeData.write("\t\t\tlong totalCount = getVal.size();\n")
    writeData.write("\t\t\treturn new ResponseEntity<>(new ResultsDao(new ModelMapper().map(getVal,\n")
    writeData.write("\t\t\t\t\tnew TypeToken<List<" + className + "Dao>>() {\n")
    writeData.write("\t\t\t\t\t}.getType()),1,Math.toIntExact(totalCount),totalCount), HttpStatus.OK);\n")

writeData.write("\t}\n")
writeData.write("}\n")

# service - > getPk1,getPk2,delData,setData,getAllData,getAllDataByPg
print("Create service class")
# creating a service class
writeData = open(path + "/" + className + "Service.java", 'w+')

writeData.write("package com."+pn+".use_cases."+moduleName+"."+folderName+";\n\n")
writeData.write("import org.springframework.beans.factory.annotation.Autowired;\n")
writeData.write("import org.springframework.data.domain.Page;\n")
writeData.write("import org.springframework.stereotype.Service;\n")
writeData.write("import java.util.List;\n")
writeData.write("import com."+pn+".helpers.utils.OffsetBasedPageRequest;\n")
writeData.write("import com."+pn+".persistence.models."+moduleName+"."+modelName+";\n")
if cstQry == 1 :
    writeData.write("import com."+pn+".use_cases."+moduleName+"."+folderName+".dao."+modelName+"CstPojo;\n")
writeData.write("\n")
writeData.write("@Service\n")
writeData.write("public class "+className+"Service {\n\n")
writeData.write("\t@Autowired\n")
writeData.write("\t" + className + "Repository rep;\n")
writeData.write("\n")
writeData.write("\tpublic "+modelName+" getPk1("+list(pk.values())[0]+" pk0) throws Exception {\n")
writeData.write("\t\ttry {\n")
writeData.write("\t\t\treturn rep.findBy"+list(pk.keys())[0]+"(pk0);\n")
writeData.write("\t\t} catch (Exception e) {\n")
writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
writeData.write("\t\t}\n")
writeData.write("\t}\n")
writeData.write("\n")
#get by id
if len(uk) > 0:
    writeData.write("\tpublic "+modelName+" getPk2("+list(uk.values())[0]+" pk0) throws Exception {\n")
    writeData.write("\t\ttry {\n")
    writeData.write("\t\t\treturn rep.findBy"+list(uk.keys())[0]+"(pk0);\n")
    writeData.write("\t\t} catch (Exception e) {\n")
    writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
    writeData.write("\t\t}\n")
    writeData.write("\t}\n")
    writeData.write("\n")
#save
writeData.write("\tpublic "+list(pk.values())[0]+" setData("+modelName+" val) throws Exception {\n")
writeData.write("\t\ttry {\n")
writeData.write("\t\t\treturn rep.save(val).get"+list(pk.keys())[0]+"();\n")
writeData.write("\t\t} catch (Exception e) {\n")
writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
writeData.write("\t\t}\n")
writeData.write("\t}\n")
writeData.write("\n")
if addAllOpt == 1 :
    #save all
    writeData.write("\tpublic void setAllData(List<"+modelName+"> val) throws Exception {\n")
    writeData.write("\t\ttry {\n")
    writeData.write("\t\t\trep.saveAll(val);\n")
    writeData.write("\t\t} catch (Exception e) {\n")
    writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
    writeData.write("\t\t}\n")
    writeData.write("\t}\n")
    writeData.write("\n")
#delete
writeData.write("\tpublic void delData("+modelName+" val) throws Exception {\n")
writeData.write("\t\ttry {\n")
writeData.write("\t\t\trep.delete(val);\n")
writeData.write("\t\t} catch (Exception e) {\n")
writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
writeData.write("\t\t}\n")
writeData.write("\t}\n")
writeData.write("\n")
if delAllOpt == 1:
    #delete all
    writeData.write("\tpublic void delAllData(List<"+modelName+"> val) throws Exception {\n")
    writeData.write("\t\ttry {\n")
    writeData.write("\t\t\trep.deleteAll(val);\n")
    writeData.write("\t\t} catch (Exception e) {\n")
    writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
    writeData.write("\t\t}\n")
    writeData.write("\t}\n")
    writeData.write("\n")
#get all
writeData.write("\tpublic List<"+modelName+"> getAllData() throws Exception {\n")
writeData.write("\t\ttry{\n")
# writeData.write("\t\t\treturn rep.findByIsActive(true);\n")
writeData.write("\t\t\treturn rep.findAll();\n")
writeData.write("\t\t}catch (Exception e){\n")
writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
writeData.write("\t\t}\n")
writeData.write("\t}\n")
writeData.write("\n")
#get all by pagination
if len(uk) > 0:
    if cstQry == 1 :
        writeData.write("\tpublic Page<"+modelName+"CstPojo> getAllDataByPg(int st, int lt,String sk) throws Exception {\n")
    else:
        writeData.write("\tpublic Page<"+modelName+"> getAllDataByPg(int st, int lt,String sk) throws Exception {\n")

    writeData.write("\t\ttry {\n")
    writeData.write("\t\t\treturn rep.findByIsActiveAnd"+list(uk.keys())[0]+"ContainingIgnoreCase(true,sk,new OffsetBasedPageRequest(st, lt));\n")

    writeData.write("\t\t} catch (Exception e) {\n")
    writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
    writeData.write("\t\t}\n")
    writeData.write("\t}\n")

writeData.write("}\n")
writeData.close();
# service - > getPk1,getPk2,delData,setData,getAllData,getAllDataByPg

print("Create repository class")
# creating a Repo class
writeData = open(path + "/" + className + "Repository.java", 'w+')

writeData.write("package com."+pn+".use_cases."+moduleName+"."+folderName+";\n\n")
writeData.write("import com."+pn+".persistence.models."+moduleName+"."+modelName+";\n")
writeData.write("import org.springframework.data.domain.Page;\n")
writeData.write("import org.springframework.data.domain.Pageable;\n")
writeData.write("import org.springframework.data.jpa.repository.JpaRepository;\n")
writeData.write("import org.springframework.stereotype.Repository;\nimport java.util.List;\n")
if cstQry == 1 :
    writeData.write("import com."+pn+".use_cases."+moduleName+"."+folderName+".dao."+modelName+"CstPojo;\nimport org.springframework.data.jpa.repository.Query;\n")

writeData.write("\n")
writeData.write("@Repository\n")
writeData.write("public interface "+className+"Repository extends JpaRepository<"+modelName+",Long> {\n")
writeData.write("\t"+modelName+" findBy"+list(pk.keys())[0]+"("+list(pk.values())[0]+" pk0);\n")
# writeData.write("\tList<"+modelName+"> findByIsActive(boolean b);\n")
if len(uk) > 0:
    writeData.write("\t"+modelName+" findBy"+list(uk.keys())[0]+"("+list(uk.values())[0]+" pk0);\n")

if len(uk) > 0:
    if cstQry == 1 :
        writeData.write("\t@Query(value = \""+selectQry+"\",nativeQuery = true,countQuery = \"SELECT count(t1.Id) FROM "+selectQry.split("from")[1]+"\")\n")
        writeData.write("\tPage<"+modelName+"CstPojo> findByIsActiveAnd"+list(uk.keys())[0]+"ContainingIgnoreCase(boolean b,String searchKey,Pageable of);\n")
    else:
        writeData.write("\tPage<"+modelName+"> findByIsActiveAnd"+list(uk.keys())[0]+"ContainingIgnoreCase(boolean b,String searchKey,Pageable of);\n")

writeData.write("}\n")


