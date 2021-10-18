import re
#Convert query to model
#--------------------------------------
projectName = "itz.scs"
tableName = "CarBrand"

# it should be same name which create in model folder
modelName = "CarBrand"
# common name for all cntrl,service
className = "CarBrand"
# object name for class
baseName = "carBrand"
folderName = "car_brand"
# Generate Pk to set,get data in db
#methodPk = [{"Id": "Integer","Name": "String"}]
createdBy = "Abdul Baasit"
#--------------------------------------

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
print("convert get data into spring boot model")
seperator = " "
writeData = open("output/"+className+".java", 'w+')
idSet = 0
writeData.write("package com."+projectName+".persistence.models;\n")
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
            writeData.write("\tprivate Integer " + ''.join([name[0].lower() + name[1:]]) + "=0;\n")
            idSet = 2
        else :
            writeData.write("\tprivate Integer " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "tinyint":
        writeData.write("\tprivate Boolean " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "float":
        writeData.write("\tprivate Float " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "double" or columnTypeCk == "amount":
        writeData.write("\tprivate Float " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "date":
        if (name != "CrAt" and name != "UpAt"):
            writeData.write("\tprivate Date " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    else:
        writeData.write("\tprivate String "+''.join([name[0].lower()+name[1:]])+";\n")
    i=i+1;

writeData.write("}")
writeData.close()

i=0
print("convert get data into spring boot idDao")
seperator = " "
writeData = open("output/"+className+"IdDao.java", 'w+')
idSet = 0
writeData.write("package com."+projectName+".persistence.dao;\n")
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
writeData = open("output/"+className+"Dao.java", 'w+')
idSet = 0
writeData.write("package com."+projectName+".persistence.dao;\n")
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
writeData = open("output/"+className+"Pojo.java", 'w+')
idSet = 0
writeData.write("package com."+projectName+".persistence.dao;\n\n")
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
