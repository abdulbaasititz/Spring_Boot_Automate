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
# ----------------
# --------------------
# tableName = "CarBrand"
folderName = '_'.join([x.lower() for x in re.findall('[A-Z][^A-Z]*', tableName)])
print("folderName :"+folderName)
modelName = tableName
className = tableName
baseName = ''.join([tableName[0].lower() + tableName[1:]])



# ---------------------------
print("convert get data into spring boot pojo")
seperator = " "
writeData = open("output/"+className+"Pojo.java", 'w+')
idSet = 0
writeData.write("package com." + pn + ".persistence.dao;\n\n")
writeData.write("public interface "+className+"Pojo {\n")

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
        print(columnTypeCk)
        if name == "Id" or name == "(Id":
            # print("t1."+word+",",end="")
            selectQry = selectQry+"t1."+name+","
            writeData.write("\tInteger getId();\n")
        elif len(check) == 1 :
            # print("t1."+word+",",end="")
            selectQry = selectQry + "t1." + name + ","
            if columnTypeCk == "tinyint":
                writeData.write("\tBoolean get" + name + "();\n")
            elif columnTypeCk == "float" or columnTypeCk == "double" or columnTypeCk == "amount":
                writeData.write("\tFloat get" + name + "();\n")
            else:
                writeData.write("\tString get" + name + "();\n")
        elif len(check) > 1:
            if check[1] == "Id":
                jn = str(int(jn) + 1)
                # print("t"+jn+"."+word+",", end="")
                selectQry = selectQry + "t" + jn + ".Id as " + check[0] + "Id,"
                writeData.write("\tInteger get"+check[0]+"Id();\n")
                selectQry = selectQry + "t" + jn + ".name as " + check[0] + "Name,"
                writeData.write("\tString get"+check[0]+"Name();\n")
                tables.append(check[0])
            elif len(check) > 2 and check[2] == "Id":
                jn = str(int(jn) + 1)
                # print("t"+jn+"."+word+",", end="")
                selectQry = selectQry + "t" + jn + ".Id as " + check[0]+check[1] + "Id,"
                writeData.write("\tInteger get" + check[0]+check[1] + "Id();\n")
                selectQry = selectQry + "t" + jn + ".name as " + check[0]+check[1] + "Name,"
                writeData.write("\tString get" + check[0]+check[1] + "Name();\n")
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

writeData.write("}")
writeData.close()
