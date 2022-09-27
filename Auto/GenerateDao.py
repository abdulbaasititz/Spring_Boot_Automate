import re
def generateDao(path,pn,folderName,moduleName,tableName,className,columnType,columnName,cstQry):
    print("Create dao class")
    i=0
    idSet = 0
    splitBy = " "
    selectQry = ""
    writeData = open(path + "/dao/" + className + "Dao.java", 'w+')
    writeData.write("package com."+pn+".use_cases."+moduleName+"."+folderName+".dao;\n\n")
    writeData.write("import lombok.Getter;\nimport lombok.Setter;\nimport javax.validation.constraints.Size;\n\n")
    writeData.write("@Getter @Setter\n")
    writeData.write("public class "+className+"Dao {\n")
    for name in columnName:
        if idSet == 0 and name == "ID" or name == "(Id" :
            idSet = 1
            if name == "(Id" :
                name = name.split('(')[1]
        columnTypeCk = columnType[i].split("(")[0]
        if (name == "CrAt" or name == "CrBy" or name == "UpAt" or name == "UpBy"):
            i=i+1;continue;
        if len(columnType[i].split("(")) > 1:
           writeData.write("\t@Size(max=")
           writeData.write(columnType[i].split("(")[1] + ")\n")
        #print(columnTypeCk)
        if columnTypeCk == "int" or columnTypeCk == "smallint" or columnTypeCk == "bigint":
            writeData.write("\tprivate Integer " + ''.join([name[0].lower() + name[1:]]) + ";\n")
        elif columnTypeCk == "tinyint" or columnTypeCk == "bit":
            writeData.write("\tprivate Boolean " + ''.join([name[0].lower() + name[1:]]) + ";\n")
        elif columnTypeCk == "float" or columnTypeCk == "amount":
            writeData.write("\tprivate Float " + ''.join([name[0].lower() + name[1:]]) + ";\n")
        elif columnTypeCk == "double":
            writeData.write("\tprivate Double " + ''.join([name[0].lower() + name[1:]]) + ";\n")
        elif columnTypeCk == "date":
            writeData.write("\tprivate Date " + ''.join([name[0].lower() + name[1:]]) + ";\n")
        else:
            writeData.write("\tprivate String "+''.join([name[0].lower()+name[1:]])+";\n")
        i=i+1;

    writeData.write("}")
    writeData.close()

    if cstQry == 1 :
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
        tables=[tableName]
        jn = 1
        i = 0
        # print("Select ",end="")
        selectQry = "Select "
        for name in columnName:
            if (name == "CrAt" and name == "CrBy" and name == "UpAt" and name == "UpBy"):
                i=i+1;continue;
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
                if columnTypeCk == "tinyint" or columnTypeCk == "bit":
                    writeDataCstPojo.write("\tBoolean get" + name + "();\n")
                    writeDataCstDao.write("\tprivate Boolean " + ''.join([name[0].lower() + name[1:]]) + ";\n")
                elif columnTypeCk == "float" or columnTypeCk == "amount":
                    writeDataCstPojo.write("\tFloat get" + name + "();\n")
                    writeDataCstDao.write("\tprivate Float " + ''.join([name[0].lower() + name[1:]]) + ";\n")
                elif columnTypeCk == "double":
                    writeDataCstPojo.write("\tDouble get" + name + "();\n")
                    writeDataCstDao.write("\tprivate Double " + ''.join([name[0].lower() + name[1:]]) + ";\n")
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
                elif len(check) > 2 and check[len(check)-1] == "Id":
                    jn = str(int(jn) + 1)
                    # print("t"+jn+"."+word+",", end="")
                    # selectQry = selectQry + "t" + jn + ".Id as " + check[0]+check[1] + "Id,"
                    selectQry = selectQry + "t" + jn + ".Id as " + ''.join(check) + ","
                    # print(selectQry)
                    # print(''.join([check[0][0].lower() + check[0][1:]]))
                    # writeDataCstPojo.write("\tInteger get" + check[0]+check[1] + "Id();\n")
                    writeDataCstPojo.write("\tInteger get" + ''.join(check) + "();\n")
                    # writeDataCstDao.write("\tprivate Integer " + ''.join([check[0][0].lower() + check[0][1:]])+check[1] + "Id;\n")
                    writeDataCstDao.write(
                        "\tprivate Integer " + ''.join([check[0][0].lower() + check[0][1:]]) + ''.join(map(str.capitalize, check[1:])) + ";\n")
                    selectQry = selectQry + "t" + jn + ".name as " + ''.join(check[:-1]) + "Name,"
                    writeDataCstPojo.write("\tString get" + ''.join(check[:-1]) + "Name();\n")
                    writeDataCstDao.write("\tprivate String "+''.join([check[0][0].lower() + check[0][1:]])+''.join(check[1:-1])+"Name;\n")
                    tables.append(''.join(check[:-1]))
            i=i+1

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

        print("Custom query is "+selectQry)

        writeDataCstPojo.write("}")
        writeDataCstPojo.close()
        writeDataCstDao.write("}")
        writeDataCstDao.close()
    return selectQry;
# --------------------
