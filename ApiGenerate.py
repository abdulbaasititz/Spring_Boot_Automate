#Convert query to model
#--------------------------------------
pn = "itz.scs" #Project Name
tableName = "CarBrand"
# SHould be underscore snake_case
folderName = "car_brand"

# it should be same name which create in model folder #- PascalCase
modelName = tableName
# common name for all cntrl,service - PascalCase
className = tableName
# object name for class camelCase
baseName = ''.join([tableName[0].lower() + tableName[1:]])
# SHould be hipen snake_case
apiName = folderName.replace('_','-')
# Generate Pk,FK,unique to set,get data in db
pk = {"Id": "Integer"}
uk = {"Name": "String"}
#fk = [{"ItemId": "String","ItemSku": "String"},{"ItemId": "String","VariantId": "String"}]
createdBy = "Abdul Baasit"
#--------------------------------------

import os

parent_dir = "E:/pycharm/spring-boot-automation/output"
print("Create a controller , service & repo ")

path = os.path.join(parent_dir, folderName)

if os.path.exists(path):
   print("Folder is not empty")
else:
    os.mkdir(path)
daoPath=os.path.join(path, "dao")
if os.path.exists(daoPath):
   print("Folder is not empty")
else:
    os.mkdir(daoPath)

print(path)
writeData = open(path + "/" + className + "Controller.java", 'w+')


writeData.write("package com."+pn+".usecases."+folderName+";\n")
writeData.write("import org.springframework.data.domain.Page;\nimport org.springframework.web.bind.annotation.*;\nimport org.springframework.beans.factory.annotation.Autowired;\n")
writeData.write("import org.springframework.http.ResponseEntity;\nimport javax.servlet.http.HttpServletRequest;\nimport java.util.List;\n")
writeData.write("import org.springframework.http.HttpStatus;\nimport org.modelmapper.ModelMapper;\nimport org.modelmapper.TypeToken;\n")

writeData.write("import com."+pn+".helpers.common.results.*;\nimport com."+pn+".helpers.common.token.*;\n")
writeData.write("import com."+pn+".usecases."+folderName+".dao.*;\n")
writeData.write("import com."+pn+".persistence.models." + modelName + ";\n")

writeData.write("@RestController\n@RequestMapping(\"${spring.base.path}\")\n")
writeData.write("public class " + className + "Controller {\n")
# Add a service class
writeData.write("\t@Autowired\n")
writeData.write("\t" + className + "Service ser;\n")
writeData.write("\t@Autowired\n")
writeData.write("\tClaimsSet claimsSet;\n")
# Create
writeData.write("\t@PostMapping(value =\"/"+apiName+"\")\n")
writeData.write("\tpublic ResponseEntity<?> masterSet(HttpServletRequest request,@RequestBody "+className+"Dao getVal) throws Exception {\n")
writeData.write("\t\tClaimsDao claimsDao = claimsSet.getClaimsDetailsAfterSet(request.getHeader(\"Authorization\"));\n")
writeData.write("\t\tif(ser.getPk2(getVal.get"+list(uk.keys())[0]+"())!=null)\n")
writeData.write("\t\t\tthrow new Exception(getVal.get"+list(uk.keys())[0]+"()+\" Value Already Set\");\n")
writeData.write("\t\tser.setData(new ModelMapper().map(getVal,"+modelName+".class));\n")
writeData.write("\t\treturn new ResponseEntity<>(new ReportDao(\"Added Successfully\",true), HttpStatus.OK);\n")
writeData.write("\t}\n")
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
writeData.write("\t}\n")
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
writeData.write("\t}\n")
writeData.write("\n")
# Get by id
writeData.write("\t@GetMapping(value =\"/"+apiName+"/{id}\")\n")
writeData.write("\tpublic ResponseEntity<?> masterGet(HttpServletRequest request\n")
writeData.write("\t\t\t,@PathVariable(name=\"id\") "+list(pk.values())[0]+" id) throws Exception {\n")
writeData.write("\t\tClaimsDao claimsDao = claimsSet.getClaimsDetailsAfterSet(request.getHeader(\"Authorization\"));\n")
writeData.write("\t\t"+modelName+" getVal = ser.getPk1(id);\n")
writeData.write("\t\tif(getVal == null)\n")
writeData.write("\t\t\tthrow new Exception(id+\" Not Found To Get\");\n")
writeData.write("\t\treturn new ResponseEntity<>(new ResultDao( new ModelMapper().map(getVal, "+className+"Dao.class),\"Car Brand Fetched Successfully\",true), HttpStatus.OK);\n")
writeData.write("\t}\n")
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
writeData.write("\t\t\tPage<"+modelName+"> getAllWtPg = ser.getAllDataByPg(pageNumber-1,pageSize);\n")
writeData.write("\t\t\tgetVal = getAllWtPg.getContent();\n")
writeData.write("\t\t\ttotalCount = getAllWtPg.getTotalElements();\n")
writeData.write("\t\t}else{\n")
writeData.write("\t\t\tgetVal = ser.getAllData();\n")
writeData.write("\t\t}\n")
writeData.write("\t\tif(getVal == null)\n")
writeData.write("\t\t\tthrow new Exception(\"Not Found To Get\");\n")
writeData.write("\n")
writeData.write("\t\treturn new ResponseEntity<>(new ResultsDao(new ModelMapper().map(getVal,\n")
writeData.write("\t\t\t\tnew TypeToken<List<"+className+"IdDao>>() {\n")
writeData.write("\t\t\t\t}.getType()),pageNumber,pageSize,totalCount), HttpStatus.OK);\n")
writeData.write("\t}\n")
writeData.write("}\n")

# service - > getPk1,getPk2,delData,setData,getAllData,getAllDataByPg


# creating a service class
writeData = open(path + "/" + className + "Service.java", 'w+')

writeData.write("package com."+pn+".usecases."+folderName+";\n\n")
writeData.write("\n")
writeData.write("import org.springframework.beans.factory.annotation.Autowired;\n")
writeData.write("import org.springframework.data.domain.Page;\n")
writeData.write("import org.springframework.data.domain.PageRequest;\n")
writeData.write("import org.springframework.stereotype.Service;\n")
writeData.write("import java.util.List;\n")
writeData.write("\n")
writeData.write("import com."+pn+".persistence.models." + modelName + ";\n")
writeData.write("\n")
writeData.write("@Service\n")
writeData.write("public class "+className+"Service {\n")
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
#delete
writeData.write("\tpublic void delData("+modelName+" val) throws Exception {\n")
writeData.write("\t\ttry {\n")
writeData.write("\t\t\trep.delete(val);\n")
writeData.write("\t\t} catch (Exception e) {\n")
writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
writeData.write("\t\t}\n")
writeData.write("\t}\n")
writeData.write("\n")
#get all
writeData.write("\tpublic List<"+modelName+"> getAllData() throws Exception {\n")
writeData.write("\t\ttry{\n")
writeData.write("\t\t\treturn rep.findByIsActive(true);\n")
writeData.write("\t\t}catch (Exception e){\n")
writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
writeData.write("\t\t}\n")
writeData.write("\t}\n")
writeData.write("\n")
#get all by pagination
writeData.write("\tpublic Page<"+modelName+"> getAllDataByPg(int pn, int ps) throws Exception {\n")
writeData.write("\t\ttry {\n")
writeData.write("\t\t\treturn rep.findByIsActive(true,PageRequest.of(pn, ps));\n")
writeData.write("\t\t} catch (Exception e) {\n")
writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
writeData.write("\t\t}\n")
writeData.write("\t}\n")
writeData.write("}\n")

writeData.close();
# service - > getPk1,getPk2,delData,setData,getAllData,getAllDataByPg

# creating a Repo class
writeData = open(path + "/" + className + "Repository.java", 'w+')

writeData.write("package com."+pn+".usecases."+folderName+";\n\n")
writeData.write("import com."+pn+".persistence.models." + modelName + ";\n")
writeData.write("import org.springframework.data.domain.Page;\n")
writeData.write("import org.springframework.data.domain.Pageable;\n")
writeData.write("import org.springframework.data.jpa.repository.JpaRepository;\n")
writeData.write("import org.springframework.stereotype.Repository;\nimport java.util.List;\n")
writeData.write("\n")
writeData.write("@Repository\n")
writeData.write("public interface "+className+"Repository extends JpaRepository<"+modelName+",Long> {\n")
writeData.write("\t"+modelName+" findBy"+list(pk.keys())[0]+"("+list(pk.values())[0]+" pk0);\n")
writeData.write("\t"+modelName+" findBy"+list(uk.keys())[0]+"("+list(uk.values())[0]+" pk0);\n")
writeData.write("\tList<"+modelName+"> findByIsActive(boolean b);\n")
writeData.write("\tPage<"+modelName+"> findByIsActive(boolean b, Pageable pg);\n")
writeData.write("}\n")



pk=""
pkType=""
uk=""
ukType=""

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
                uk = fields[i - 3].rstrip(',();')
                uk = uk.replace('(','')
                ukType = fields[i - 2].rstrip(',();')
                continue
            if check == "PRIMARY":
                pk = fields[i + 4].rstrip(',();')
                pk = pk.replace('(','')
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
print("primaryKey :"+pk)
print("uniqueKey :"+uk)
print("uniqueKeyType :"+ukType)
print(columnName)
print(columnType)
file.close()
i=0
get = 0
print("convert get data into spring boot model")
seperator = " "
writeData = open("output/"+className+".java", 'w+')
idSet = 0
writeData.write("package com."+pn+".persistence.models;\n")
writeData.write("import lombok.Getter;\nimport lombok.Setter;\nimport javax.persistence.*;\n\n")
writeData.write("@Entity @Table(name=\"" + tableName + "\") \n")
writeData.write("@Getter @Setter\n")
writeData.write("public class "+className+" extends Auditable<String> {\n")
for name in columnName:
    if idSet == 0 and name == "ID" or name == "(Id" :
        idSet = 1
        writeData.write("\t@Id\n")
        writeData.write("\t@GeneratedValue(strategy=GenerationType.IDENTITY)\n")
        if name == "(Id" :
            name = name.split('(')[1]
    # if (name != "CrAt" and name != "UpAt"):
    #     writeData.write("\t@Column(name=\"")
    #     writeData.write(name+"\")\n")
    columnTypeCk = columnType[i].split("(")[0]
    #print(columnTypeCk)
    if columnTypeCk == "int" or columnTypeCk == "smallint" or columnTypeCk == "bigint":
        if idSet == 1:
            writeData.write("\tprivate Integer " + ''.join([name[0].lower() + name[1:]]) + " = 0;\n")
            idSet = 2
        else :
            writeData.write("\tprivate Integer " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "tinyint":
        writeData.write("\tprivate Boolean " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "float":
        writeData.write("\tprivate Float " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "double" or columnTypeCk == "amount":
        writeData.write("\tprivate Float " + ''.join([name[0].lower() + name[1:]]) + ";\n")
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
    i=i+1;

writeData.write("}")
writeData.close()

get=0
i=0
print("convert get data into spring boot idDao")
seperator = " "
#writeData = open("output/"+className+"IdDao.java", 'w+')
writeData = open(path + "/dao/" + className + "IdDao.java", 'w+')
idSet = 0
writeData.write("package com."+pn+".persistence.dao;\n")
writeData.write("import lombok.Getter;\nimport lombok.Setter;\n\n")
writeData.write("@Getter @Setter\n")
writeData.write("public class "+className+"IdDao {\n")
for name in columnName:
    if idSet == 0 and name == "ID" or name == "(Id" :
        idSet = 1
        if name == "(Id" :
            name = name.split('(')[1]
    columnTypeCk = columnType[i].split("(")[0]
    #print(columnTypeCk)
    if columnTypeCk == "int" or columnTypeCk == "smallint" or columnTypeCk == "bigint":
        writeData.write("\tprivate Integer " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "tinyint":
        writeData.write("\tprivate Boolean " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "float":
        writeData.write("\tprivate Float " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "double" or columnTypeCk == "amount":
        writeData.write("\tprivate Float " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "date":
        if (name != "CrAt" and name != "CrBy" and name != "UpAt" and name != "UpBy"):
            writeData.write("\tprivate Date " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    else:
        if (name != "CrAt" and name != "CrBy" and name != "UpAt" and name != "UpBy"):
            writeData.write("\tprivate String "+''.join([name[0].lower()+name[1:]])+";\n")
    i=i+1;

writeData.write("}")
writeData.close()


i=0
print("convert get data into spring boot dao")
seperator = " "
# writeData = open("output/"+className+"Dao.java", 'w+')
writeData = open(path + "/dao/" + className + "Dao.java", 'w+')
idSet = 0
writeData.write("package com."+pn+".persistence.dao;\n")
writeData.write("import lombok.Getter;\nimport lombok.Setter;\n\n")
writeData.write("@Getter @Setter\n")
writeData.write("public class "+className+"Dao {\n")
for name in columnName:
    if idSet == 0 and name == "ID" or name == "(Id" :
        i = i + 1;
        continue;
        idSet = 1
        if name == "(Id" :
            name = name.split('(')[1]
    columnTypeCk = columnType[i].split("(")[0]
    #print(columnTypeCk)
    if columnTypeCk == "int" or columnTypeCk == "smallint" or columnTypeCk == "bigint":
        writeData.write("\tprivate Integer " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "tinyint":
        writeData.write("\tprivate Boolean " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "float":
        writeData.write("\tprivate Float " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "double" or columnTypeCk == "amount":
        writeData.write("\tprivate Float " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "date":
        if (name != "CrAt" and name != "CrBy" and name != "UpAt" and name != "UpBy"):
            writeData.write("\tprivate Date " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    else:
        if (name != "CrAt" and name != "CrBy" and name != "UpAt" and name != "UpBy"):
            writeData.write("\tprivate String "+''.join([name[0].lower()+name[1:]])+";\n")
    i=i+1;

writeData.write("}")
writeData.close()



i=0
print("convert get data into spring boot pojo")
seperator = " "
# writeData = open("output/"+className+"Pojo.java", 'w+')
writeData = open(path + "/dao/" + className + "Pojo.java", 'w+')
idSet = 0
writeData.write("package com."+pn+".persistence.dao;\n\n")
writeData.write("public interface "+className+"Pojo {\n")
for name in columnName:
    if idSet == 0 and name == "ID" or name == "(Id" :
        idSet = 1
        if name == "(Id" :
            name = name.split('(')[1]
    columnTypeCk = columnType[i].split("(")[0]
    #print(columnTypeCk)
    if columnTypeCk == "int" or columnTypeCk == "smallint" or columnTypeCk == "bigint":
        writeData.write("\tInteger get"+name+"();\n")
    elif columnTypeCk == "tinyint":
        if (name != "IsActive"):
            writeData.write("\tBoolean get"+name+"();\n")
    elif columnTypeCk == "float":
        writeData.write("\tFloat get" + name + "();\n")
    elif columnTypeCk == "double" or columnTypeCk == "amount":
        writeData.write("\tFloat get"+name+"();\n")
    elif columnTypeCk == "date":
        if (name != "CrAt" and name != "CrBy" and name != "UpAt" and name != "UpBy"):
            writeData.write("\tDate get"+name+"();\n")
    else:
        if (name != "CrAt" and name != "CrBy" and name != "UpAt" and name != "UpBy"):
            writeData.write("\tString get"+name+"();\n")
    i=i+1;

writeData.write("}")
writeData.close()
