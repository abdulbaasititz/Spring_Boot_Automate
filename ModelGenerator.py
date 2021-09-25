print("convert table into spring boot model")
# input
#--------------------------------------
projectName = "uclo.pos"
tableName = "FINCUSTOMERCREDITNOTEHDR"
className = "FinCustomerCreditNoteHdr"
# if plant name in db, mention 1 eg:(plant_table name) else 0
plantName = 1
# if model name and alias name are same except first letter put 0 else 1
aliasName = 1
#--------------------------------------
seperator = " "
getData = open('GetData', 'r')
writeData = open("output/"+className+".java", 'w+')
lines = getData.readlines()
print(lines[0])
idSet = 0
writeData.write("package com."+projectName+".persistence.models;\n")
writeData.write("import lombok.Getter;\nimport lombok.Setter;\nimport javax.persistence.*;\n\n")
if plantName == 1 :
    writeData.write("@Entity @Table(name=\"##plant##"+tableName+"\") \n")
else :
    writeData.write("@Entity @Table(name=\"" + tableName + "\") \n")
writeData.write("@Getter @Setter\n")
writeData.write("public class "+className+" {\n")
for line in lines:
    getVal = line.strip().split(seperator)

    if idSet == 0 and (getVal[0] == "ID" or getVal[0] == "Id"):
        idSet = 1
        writeData.write("\t@Id\n")
        writeData.write("\t@GeneratedValue(strategy=GenerationType.IDENTITY)\n")

    writeData.write("\t@Column(name=\"")
    writeData.write(getVal[0]+"\")\n")

    if getVal[1] == "int" or getVal[1] == "smallint" or getVal[1] == "tinyint":
        if aliasName == 0 :
            writeData.write("\tprivate Integer "+''.join([getVal[0][0].lower()+getVal[0][1:]])+";\n")
        else :
            writeData.write("\tprivate Integer "+getVal[3]+";\n")
    elif getVal[1] == "float":
        if aliasName == 0:
            writeData.write("\tprivate Float "+''.join([getVal[0][0].lower()+getVal[0][1:]])+";\n")
        else:
            writeData.write("\tprivate Float " + getVal[3] + ";\n")
    elif getVal[1] == "double" or getVal[1] == "amount":
        if aliasName == 0:
            writeData.write("\tprivate Double "+''.join([getVal[0][0].lower()+getVal[0][1:]])+";\n")
        else :
            writeData.write("\tprivate Double " + getVal[3] + ";\n")
    elif getVal[1].find("decimal") != -1:
        if aliasName == 0 :
            writeData.write("\tprivate Float "+''.join([getVal[0][0].lower()+getVal[0][1:]])+";\n")
        else:
            writeData.write("\tprivate Float " + getVal[4] + ";\n")
    else:
        if aliasName == 0:
            writeData.write("\tprivate String "+''.join([getVal[0][0].lower()+getVal[0][1:]])+";\n")
        else:
            writeData.write("\tprivate String " + getVal[3] + ";\n")

writeData.write("}")
getData.close()
writeData.close()