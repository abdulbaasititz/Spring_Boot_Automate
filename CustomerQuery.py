import re
#Convert query to model
#--------------------------------------
pn = "itz.base" #Project Name
tableName = "" #No Need
moduleName = "customer_module"
cstQry = 1
addAllOpt = 0
delAllOpt = 0
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
selectQry = "Select t1.*,"
for name in columnName:
    if (name == "CrAt" and name == "CrBy" and name == "UpAt" and name == "UpBy"):
        i=i+1;continue;
    check = rx.sub(' ', name).split(' ')
    columnTypeCk = columnType[i].split("(")[0]
    print(columnTypeCk)
    if len(check) > 1:
        if check[len(check)-1] == "Id":
            jn = str(int(jn) + 1)
            #print("t"+jn+"."+word+",", end="")
            # selectQry = selectQry + "t" + jn + ".Id as " + check[0]+check[1] + "Id,"
            selectQry = selectQry + "(select name from " + ''.join(check[:-1]) + " where id=t1." + ''.join(check) + " )as " + ''.join(check[:-1]) + "Name,"
            print(selectQry)

    i=i+1

selectQry = selectQry.rstrip(',')+' from ' +tableName +" t1"

print("Custom query is "+selectQry)

writeDataCstPojo.write("}")
writeDataCstPojo.close()
writeDataCstDao.write("}")
writeDataCstDao.close()