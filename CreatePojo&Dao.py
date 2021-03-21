import string
print("convert dao into pojo for spring boot model")

getData = open('GetData', 'r')
writeData = open('WriteDataPojo', 'w')
lines = getData.readlines()
# create pojo
writeData.write("POJO\n\n")
for line in lines:
    getVal = line.strip().split(" ")
    if getVal[4] == '1':
        if getVal[1] == "int" or getVal[1] == "smallint" or getVal[1] == "tinyint":
            writeData.write("int get"+''.join([getVal[3][0].upper()+getVal[3][1:]])+"();\n")
        elif getVal[1] == "float" or getVal[1] == "double":
            writeData.write("float get"+''.join([getVal[3][0].upper()+getVal[3][1:]])+"();\n")
        else:
            writeData.write("String get"+''.join([getVal[3][0].upper()+getVal[3][1:]])+"();\n")
# create Dao
writeData.write("\nDAO\n\n")
for line in lines:
    getVal = line.strip().split(" ")
    if getVal[4] == '1':
        if getVal[1] == "int" or getVal[1] == "smallint" or getVal[1] == "tinyint":
            writeData.write("private int "+getVal[3]+";\n")
        elif getVal[1] == "float" or getVal[1] == "double":
            writeData.write("private float "+getVal[3]+";\n")
        else:
            writeData.write("private String "+getVal[3]+";\n")

writeData.write("done")
getData.close()
writeData.close()