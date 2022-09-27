

def generateModel(pn,tableName,className,columnType,columnName):
    # --------------------------
    print("Create model class")
    i=0
    get = 0
    idSet = 0
    splitBy = " "
    writeData = open("output/"+className+".java", 'w+')
    writeData.write("package com." + pn + ".persistence.models;\n")
    writeData.write("import com." + pn + ".helpers.utils.JwtUtil;\n")
    writeData.write("import com." + pn + ".persistence.models.common.Auditable;\n")
    writeData.write("import lombok.Getter;\nimport lombok.Setter;\nimport javax.persistence.*;\n\n")
    writeData.write("@Entity @Table(name=\"" + tableName + "\") \n")
    writeData.write("@Getter @Setter\n")
    if "UpAt" in columnName:
        writeData.write("public class " + className + " extends Auditable<String> {\n")
    else:
        writeData.write("public class "+className+"  {\n")
    for name in columnName:
        if idSet == 0 and name == "ID" or name == "(Id" :
            idSet = 1
            writeData.write("\t@Id\n")
            writeData.write("\t@GeneratedValue(strategy=GenerationType.IDENTITY)\n")
            if name == "(Id" :
                name = name.split('(')[1]
        columnTypeCk = columnType[i].split("(")[0]
        #print(columnTypeCk)
        if columnTypeCk == "int" or columnTypeCk == "smallint" or columnTypeCk == "bigint":
            if idSet == 1:
                writeData.write("\tprivate Integer " + ''.join([name[0].lower() + name[1:]]) + " = 0;\n")
                idSet = 2
            else :
                if (get == 0 and name == "CrBy"):
                    writeData.write("\tprivate Integer crBy = JwtUtil.usr;\n")
                    get = 1;
                    i = i + 1;
                    continue;
                writeData.write("\tprivate Integer " + ''.join([name[0].lower() + name[1:]]) + ";\n")
        elif columnTypeCk == "tinyint" or columnTypeCk == "bit":
            writeData.write("\tprivate Boolean " + ''.join([name[0].lower() + name[1:]]) + ";\n")
        elif columnTypeCk == "float" or columnTypeCk == "amount":
            writeData.write("\tprivate Float " + ''.join([name[0].lower() + name[1:]]) + ";\n")
        elif columnTypeCk == "double":
            writeData.write("\tprivate Double " + ''.join([name[0].lower() + name[1:]]) + ";\n")
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
# ---------