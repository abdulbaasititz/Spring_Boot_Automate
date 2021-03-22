print("convert table into spring boot model")
# input
#--------------------------------------
projectName = "uclo.inventory"
tableName = "DODET_REMARKS"
className = "DoDetRemarks"
#--------------------------------------
seperator = " "
getData = open('GetData', 'r')
writeData = open("output/"+className+".java", 'w+')
lines = getData.readlines()
print(lines[0])
idSet = 0
writeData.write("package com."+projectName+".persistence.models;\n")
writeData.write("import lombok.Getter;\nimport lombok.Setter;\nimport javax.persistence.*;\n\n")
writeData.write("@Entity @Table(name=\"##plant##"+tableName+"\") \n")
writeData.write("@Getter @Setter\n")
writeData.write("public class "+className+" {\n")
for line in lines:
    getVal = line.strip().split(seperator)

    if idSet == 0 and getVal[0] == "ID":
        idSet = 1
        writeData.write("\t@Id\n")
        writeData.write("\t@GeneratedValue(strategy=GenerationType.IDENTITY)\n")

    writeData.write("\t@Column(name=\"")
    writeData.write(getVal[0]+"\")\n")

    if getVal[1] == "int" or getVal[1] == "smallint" or getVal[1] == "tinyint":
        writeData.write("\tprivate int "+getVal[3]+";\n")
    elif getVal[1] == "float":
        writeData.write("\tprivate float "+getVal[3]+";\n")
    elif getVal[1] == "double" or getVal[1] == "amount":
        writeData.write("\tprivate double " + getVal[3] + ";\n")
    elif getVal[1].find("decimal") != -1:
        writeData.write("\tprivate float " + getVal[4] + ";\n")
    else:
        writeData.write("\tprivate String " + getVal[3] + ";\n")

writeData.write("}")
getData.close()
writeData.close()