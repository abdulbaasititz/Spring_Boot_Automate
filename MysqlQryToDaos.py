import re
#Convert query to model
#--------------------------------------
pn = "itz.scs"


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
get = 0

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
        if get == 1:
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
# --------------------
# tableName = "CarBrand"
folderName = '_'.join([x.lower() for x in re.findall('[A-Z][^A-Z]*', tableName)])
print("folderName :"+folderName)
modelName = tableName
className = tableName
baseName = ''.join([tableName[0].lower() + tableName[1:]])

# ----------------------
i=0
get = 0
print("convert get data into spring boot model")
seperator = " "
writeData = open("output/"+className+".java", 'w+')
idSet = 0
writeData.write("package com." + pn + ".persistence.models;\n")
writeData.write("import com.itz.scs.helpers.utils.JwtUtil;\n")
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
    #     writeData.write("\t@Column(size=\"")
    #     writeData.write(columnType[i].split("(")[1] + "\")\n")
        # writeData.write("\t@Column(name=\"")
        # writeData.write(name+"\")\n")
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
    i=i+1

writeData.write("}")
writeData.close()

get=0
i=0
print("convert get data into spring boot Dao")
seperator = " "
writeData = open("output/"+className+"Dao.java", 'w+')
idSet = 0
writeData.write("package com."+pn+".use_cases."+folderName+".dao;\n\n")
writeData.write("import lombok.Getter;\nimport lombok.Setter;\n\n")
writeData.write("@Getter @Setter\n")
writeData.write("public class "+className+"Dao {\n")
for name in columnName:
    if idSet == 0 and name == "ID" or name == "(Id" :
        idSet = 1
        if name == "(Id" :
            name = name.split('(')[1]
    columnTypeCk = columnType[i].split("(")[0]
    if (name != "CrAt" and name != "CrBy" and name != "UpAt" and name != "UpBy"):
        writeData.write("\t@Size(max=")
        writeData.write(columnType[i].split("(")[1] + ")\n")
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




# ---------------------------
print("convert get data into spring boot pojo")
seperator = " "
writeDataCstPojo = open("output/"+className+"CstPojo.java", 'w+')
writeDataCstDao = open("output/"+className+"CstDao.java", 'w+')
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
    if (name != "CrAt" and name != "CrBy" and name != "UpAt" and name != "UpBy"):
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
            if columnTypeCk == "tinyint":
                writeDataCstPojo.write("\tBoolean get" + name + "();\n")
                writeDataCstDao.write("\tprivate Boolean " + ''.join([name[0].lower() + name[1:]]) + ";\n")
            elif columnTypeCk == "float" or columnTypeCk == "double" or columnTypeCk == "amount":
                writeDataCstPojo.write("\tFloat get" + name + "();\n")
                writeDataCstDao.write("\tprivate Float " + ''.join([name[0].lower() + name[1:]]) + ";\n")
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
            elif len(check) > 2 and check[2] == "Id":
                jn = str(int(jn) + 1)
                # print("t"+jn+"."+word+",", end="")
                selectQry = selectQry + "t" + jn + ".Id as " + check[0]+check[1] + "Id,"
                print(''.join([check[0][0].lower() + check[0][1:]]))
                writeDataCstPojo.write("\tInteger get" + check[0]+check[1] + "Id();\n")
                writeDataCstDao.write("\tprivate Integer " + ''.join([check[0][0].lower() + check[0][1:]])+check[1] + "Id;\n")
                selectQry = selectQry + "t" + jn + ".name as " + check[0]+check[1] + "Name,"
                writeDataCstPojo.write("\tString get" + check[0]+check[1] + "Name();\n")
                writeDataCstDao.write("\tprivate String "+''.join([check[0][0].lower() + check[0][1:]])+check[1]+"Name;\n")
                tables.append(check[0]+check[1])
    i=i+1


print()
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

print(selectQry)
# -------------------------------

writeDataCstPojo.write("}")
writeDataCstPojo.close()
writeDataCstDao.write("}")
writeDataCstDao.close()