import os

parent_dir = "/spring-boot-automation/output"
print("Create a controller , service & repo ")

# input to set the controller,service and model name
projectName = "uclo.shopee"
#tableName = "SHOPIFY_ITEM"
# it should be same name which create in model folder
modelName = "ShopeeItem"
# common name for all cntrl,service
className = "ShopeeItem"
# object name for class
baseName = "shopeeItem"
folderName = "Shopee_item"
# key -  first letter caps and same like model alias name
# value - type
#pk1 = ["Id","Item","Location","UserFieldFour"]
#pkType1 = ["Integer","String","String","String"]
methodPk = [{"ItemId": "String","ItemSku": "String"},{"ItemId": "String","VariantId": "String"}]
createdBy = "Abdul Baasit"
valSet = ""
pkFuncName = 1
# Creating a new directory
path = os.path.join(parent_dir, folderName)
os.mkdir(path)
print(path)

# "AND" , "PK"
def serviceNameForPkFindBy(getPrefix, getSuffix,pk,pkType):
    valSet = ""
    i = 0
    if getPrefix != "":
        for pkVal in pk:
            valSet = valSet + pkVal + getPrefix
        valSet = valSet[:-3]
    valSet = valSet + "("
    for pkTypeVal in pkType:
        valSet = valSet + getSuffix + str(i) + ","
        i = i + 1
    valSet = valSet[:-1] + ")"
    return valSet


def serviceNameForPk(getPrefix, getSuffix,pk,pkType):
    valSet = ""
    i = 0
    if getPrefix != "":
        for pkVal in pk:
            valSet = valSet + pkVal + getPrefix
        valSet = valSet[:-3]
    valSet = valSet + "("
    for pkTypeVal in pkType:
        valSet = valSet + pkTypeVal + " " + getSuffix + str(i) + ","
        i = i + 1
    valSet = valSet[:-1] + ")"
    return valSet


def controllerPassValForPk(getPrefix, getSuffix,pk,pkType):
    valSet = ""
    for pkVal in pk:
        valSet = valSet + getPrefix + pkVal + getSuffix
    return valSet[:-1]


# creating a controller class
writeData = open(path + "/" + className + "Controller.java", 'w+')
writeData.write("package com." + projectName + ".usecases." + folderName + ";\n\n")
writeData.write("import org.springframework.web.bind.annotation.RequestMapping;\n")
writeData.write("import org.springframework.web.bind.annotation.RestController;\n")
writeData.write("import org.springframework.web.bind.annotation.RequestMethod;\n")
writeData.write("import org.springframework.beans.factory.annotation.Autowired;\n")
writeData.write("import org.springframework.http.ResponseEntity;\n")
writeData.write("import javax.servlet.http.HttpServletRequest;\n")
writeData.write("import org.springframework.web.bind.annotation.RequestBody;\n")
writeData.write("import com." + projectName + ".persistence.models." + modelName + ";\n")
writeData.write("import com." + projectName + ".helpers.common.token.ClaimsDao;\n")
writeData.write("import com." + projectName + ".helpers.common.calc.DateTimeCalc;\n")
writeData.write("import com." + projectName + ".helpers.common.token.ClaimsSet;\n")
writeData.write("import org.springframework.http.HttpStatus;\n")
writeData.write("@RestController\n@RequestMapping(\"${spring.base.path}\")\n")
writeData.write("public class " + className + "Controller {\n")
# Add a service class
writeData.write("\t@Autowired\n")
writeData.write("\t" + className + "Service " + baseName + "Service;\n")
writeData.write("\t@Autowired\n")
writeData.write("\tClaimsSet claimsSet;\n")
# Creating a function to check and save the models
writeData.write("\t@RequestMapping(value = \"/set-" + baseName + "/new\", method = RequestMethod.POST)\n")
writeData.write("\tpublic ResponseEntity<?> new" + baseName + "(HttpServletRequest request,")
writeData.write("@RequestBody " + modelName + " val) throws Exception {\n")
# Header information get
# writeData.write("\t\tClaimsDao claimsDao = claimsSet.getClaimsDetailsAfterSet(request.getHeader(\"Authorization\"));\n")
# writeData.write("\t\tString plant = claimsDao.getPlt();\n")
# writeData.write("\t\tString sub = claimsDao.getSub();\n")
# writeData.write("\t\tString empId = claimsDao.getEid();\n")
writeData.write("\t\tDateTimeCalc dateTimeCalc = new DateTimeCalc();\n")
writeData.write("\t\tString createdAt = dateTimeCalc.getUcloTodayDateTime();\n")
writeData.write("\t\tString createdBy = \"" + createdBy + "\";\n")
# to check primary key existing in db
pkFuncName = 1
for pkDet in methodPk :
    writeData.write("\t\tBoolean status"+str(pkFuncName)+" = " + baseName + "Service.check" + modelName
                    + "Pk"+str(pkFuncName)+"(" + controllerPassValForPk("val.get","(),",list(pkDet.keys()),list(pkDet.values())) + ");\n")
    pkFuncName=pkFuncName+1
pkFuncName = 1
writeData.write("\t\tif(!status1){\n")
# if not save the value
writeData.write("\t\t\t" + baseName + "Service.set" + modelName + "Details(val);\n")
writeData.write("\t\t}else{\n")
writeData.write("\t\t\tthrow new Exception(\"value already set\");\n")
writeData.write("\t\t}\n")
writeData.write("\treturn new ResponseEntity<>(\"Success\", HttpStatus.OK);")
writeData.write("\t}\n")
writeData.write("}\n")

# creating a service class
writeData = open(path + "/" + className + "Service.java", 'w+')
writeData.write("package com." + projectName + ".usecases." + folderName + ";\n\n")
writeData.write("import org.springframework.beans.factory.annotation.Autowired;\n")
writeData.write("import org.springframework.stereotype.Service;\n")
writeData.write("import com." + projectName + ".helpers.configs.LoggerConfig;\n")
writeData.write("import com." + projectName + ".persistence.models." + modelName + ";\n\n")
writeData.write("@Service\n")
writeData.write("public class " + className + "Service {\n")
writeData.write("\t@Autowired\n")
writeData.write("\t" + className + "Repository " + baseName + "Repository;\n")
pkFuncName=1
for pkDet in methodPk :
    # function to check the primary key
    writeData.write("\tpublic Boolean check" + modelName + "Pk"+str(pkFuncName)+ serviceNameForPk("", "pk",list(pkDet.keys()),list(pkDet.values())) + " throws Exception {\n")
    writeData.write("\t\ttry {\n")
    writeData.write(
        "\t\t\t" + modelName + " getVal = " + baseName + "Repository.findBy" + serviceNameForPkFindBy("And", "pk",list(pkDet.keys()),list(pkDet.values())) + ";\n")
    writeData.write("\t\t\tif(getVal == null)\n")
    writeData.write("\t\t\t\treturn false;\n")
    writeData.write("\t\t} catch (Exception e) {\n")
    writeData.write("\t\t\tLoggerConfig.logger.error(e.getMessage());\n")
    writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
    writeData.write("\t\t}\n")
    writeData.write("\t\treturn true;\n")
    writeData.write("\t}\n\n")
    pkFuncName = pkFuncName+1
# function to get value using primary key
pkFuncName=1
for pkDet in methodPk :
    writeData.write(
        "\tpublic " + modelName + " get" + modelName + "Pk"+str(pkFuncName)+ serviceNameForPk("", "pk",list(pkDet.keys()),list(pkDet.values())) + " throws Exception {\n")
    writeData.write("\t\t" + modelName + " getVal;\n")
    writeData.write("\t\ttry {\n")
    writeData.write("\t\t\tgetVal = " + baseName + "Repository.findBy" + serviceNameForPkFindBy("And", "pk",list(pkDet.keys()),list(pkDet.values())) + ";\n")
    writeData.write("\t\t} catch (Exception e) {\n")
    writeData.write("\t\t\tLoggerConfig.logger.error(e.getMessage());\n")
    writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
    writeData.write("\t\t}\n")
    writeData.write("\t\treturn getVal;\n")
    writeData.write("\t}\n\n")
    pkFuncName = pkFuncName+1
# function to save the model
writeData.write("\tpublic String set" + modelName + "Details(" + modelName + " val) throws Exception {\n")
writeData.write("\t\ttry {\n")
writeData.write("\t\t\t" + baseName + "Repository.save(val);\n")
writeData.write("\t\t} catch (Exception e) {\n")
writeData.write("\t\t\tLoggerConfig.logger.error(e.getMessage());\n")
writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
writeData.write("\t\t}\n")
writeData.write("\t\treturn \"1\";\n")
writeData.write("\t}\n")
writeData.write("}\n")

# creating a Repository class
writeData = open(path + "/" + className + "Repository.java", 'w+')
writeData.write("package com." + projectName + ".usecases." + folderName + ";\n\n")
writeData.write("import com." + projectName + ".persistence.models." + modelName + ";\n")
writeData.write("import org.springframework.data.jpa.repository.JpaRepository;\n")
writeData.write("import org.springframework.stereotype.Repository;\n\n")
writeData.write("@Repository\n")
writeData.write("public interface " + className + "Repository extends JpaRepository<" + modelName + ",Long> {\n")
# function to check the primary key
for pkDet in methodPk :
    writeData.write("\t" + modelName + " findBy" + serviceNameForPk("And", "pk",list(pkDet.keys()),list(pkDet.values())) + ";\n")
writeData.write("}\n")
