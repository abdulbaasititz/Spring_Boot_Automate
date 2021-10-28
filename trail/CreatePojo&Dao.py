import string
import os
print("convert dao into pojo for spring boot model")

parent_dir = "/spring-boot-automation/output"

# input to set the controller,service and model name
projectName = "uclo.poc"
tableName = "UOM"
modelName = "uomMaster"
className = "uomMaster"
baseName = "uomMaster"
folderName = "uom_master"

# Creating a new directory
path = os.path.join(parent_dir, folderName)
os.mkdir(path)
print(path)

getData = open('../GetData', 'r')
writeData = open(path + "/" + className + "Pojo.java", 'w+')
lines = getData.readlines()
# create pojo
writeData.write("package com." + projectName + ".usecases." + folderName + ";\n\n")
writeData.write("public interface " + className + "Pojo {\n")
for line in lines:
    getVal = line.strip().split(" ")
    if getVal[4] == '1':
        if getVal[1] == "int" or getVal[1] == "smallint" or getVal[1] == "tinyint":
            writeData.write("\tint get"+''.join([getVal[3][0].upper()+getVal[3][1:]])+"();\n")
        elif getVal[1] == "float" or getVal[1] == "double":
            writeData.write("\tfloat get"+''.join([getVal[3][0].upper()+getVal[3][1:]])+"();\n")
        else:
            writeData.write("\tString get"+''.join([getVal[3][0].upper()+getVal[3][1:]])+"();\n")

writeData.write("}")
writeData.close()
writeData = open(path + "/" + className + "Dao.java", 'w+')
# create Dao
writeData.write("package com." + projectName + ".usecases." + folderName + ";\n\n")
writeData.write("import lombok.Getter;\nimport lombok.Setter;\n\n")
writeData.write("@Getter @Setter\n")
writeData.write("public class " + className + "Dao {\n")
for line in lines:
    getVal = line.strip().split(" ")
    if getVal[4] == '1':
        if getVal[1] == "int" or getVal[1] == "smallint" or getVal[1] == "tinyint":
            writeData.write("\tprivate int "+getVal[3]+";\n")
        elif getVal[1] == "float" or getVal[1] == "double":
            writeData.write("\tprivate float "+getVal[3]+";\n")
        else:
            writeData.write("\tprivate String "+getVal[3]+";\n")
writeData.write("}")
getData.close()
writeData.close()