#Convert query to model
#--------------------------------------
projectName = "itz.scs"
tableName = ""
className = ""

#--------------------------------------
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
        if check != "NOT" and check != "NULL" and check != "CREATE" and check != "KEY" and check != "UNIQUE":
            #print(check)
            get = 1
            if check == "TABLE":
                tableName = fields[i + 1]
                get=0
            if check == "PRIMARY":
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
print(columnName)
print(columnType)
className = tableName
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
writeData.write("public class "+className+" {\n")
for name in columnName:
    if idSet == 0 and name == "ID" or name == "(Id" :
        idSet = 1
        writeData.write("\t@Id\n")
        writeData.write("\t@generatedvalue(strategy=generationtype.identity)\n")
        if name == "(Id" :
            name = name.split('(')[1]

    writeData.write("\t@Column(name=\"")
    writeData.write(name+"\")\n")
    columnTypeCk = columnType[i].split("(")[0]
    print(columnTypeCk)
    if columnTypeCk == "int" or columnTypeCk == "smallint" or columnTypeCk == "bigint":
        writeData.write("\tprivate Integer " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "tinyint":
        writeData.write("\tprivate Boolean " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "float":
        writeData.write("\tprivate Float " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "double" or columnTypeCk == "amount":
        writeData.write("\tprivate Float " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "float":
        writeData.write("\tprivate Float " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    elif columnTypeCk == "date":
        writeData.write("\tprivate Date " + ''.join([name[0].lower() + name[1:]]) + ";\n")
    else:
        writeData.write("\tprivate String "+''.join([name[0].lower()+name[1:]])+";\n")
    i=i+1;

writeData.write("}")
writeData.close()