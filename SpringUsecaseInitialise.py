import os

parent_dir = "E:/pycharm/spring-boot-automation/output"
print("Create a controller , service & repo ")

# input to set the controller,service and model name
projectName = "uclo.inventory"
tableName = "DODET"
modelName = "DoDet"
className = "DoDet"
baseName = "doDet"
folderName = "do_det"
#primaryKey = "DoNoAndDoLineNo"
pk = ["DoNo","DoLineNo"]
pkType = ["String","int"]
createdBy = "abdul"
valSet = ""

# Creating a new directory
path = os.path.join(parent_dir, folderName)
os.mkdir(path)
print(path)

def serviceNameForPk(getPrefix, getSuffix):
    valSet = ""
    i=0
    if getPrefix != "":
        for pkVal in pk:
            valSet = valSet + pkVal + getPrefix
        valSet = valSet[:-3]
    valSet = valSet + "("
    for pkTypeVal in pkType:
        valSet = valSet + pkTypeVal+" "+getSuffix + str(i) + ","
        i = i+1
    valSet = valSet[:-1] + ")"
    return valSet

def controllerPassValForPk (getPrefix , getSuffix):
    valSet=""
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
writeData.write("\t\tClaimsDao claimsDao = claimsSet.getClaimsDetailsAfterSet(request.getHeader(\"Authorization\"));\n")
writeData.write("\t\tString plant = claimsDao.getPlt();\n")
writeData.write("\t\tString sub = claimsDao.getSub();\n")
writeData.write("\t\tString empId = claimsDao.getEid();\n")
writeData.write("\t\tDateTimeCalc dateTimeCalc = new DateTimeCalc();\n")
writeData.write("\t\tString createdAt = dateTimeCalc.getUcloTodayDateTime();\n")
writeData.write("\t\tString createdBy = \"" + createdBy + "\";\n")
# to check primary key existing in db
writeData.write(
    "\t\tString status = " + baseName + "Service.check" + modelName + "Pk(" + controllerPassValForPk("val.get","(),")+");\n")
writeData.write("\t\tif(status == \"1\"){\n")
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
writeData.write("import com." + projectName + ".persistence.models." + modelName + ";\n\n")
writeData.write("@Service\n")
writeData.write("public class " + className + "Service {\n")
writeData.write("\t@Autowired\n")
writeData.write("\t" + className + "Repository " + baseName + "Repository;\n")
# function to check the primary key
writeData.write("\tpublic String check" + modelName + "Pk"+ serviceNameForPk(" ","val")+" throws Exception {\n")
writeData.write("\t\ttry {\n")
writeData.write("\t\t\t" + modelName + " getVal = " + baseName + "Repository.findBy" + serviceNameForPk("And","pk")+";\n")
writeData.write("\t\t\tif(getVal == null)\n")
writeData.write("\t\t\t\treturn \"1\";\n")
writeData.write("\t\t} catch (Exception e) {\n")
writeData.write("\t\t\tthrow new Exception(\"SQL Error!!!\");\n")
writeData.write("\t\t}\n")
writeData.write("\treturn \"0\";\n")
writeData.write("\t}\n")
# function to save the model
writeData.write("\tpublic String set" + modelName + "Details(" + modelName + " val) throws Exception {\n")
writeData.write("\t\ttry {\n")
writeData.write("\t\t\t" + baseName + "Repository.save(val);\n")
writeData.write("\t\t} catch (Exception e) {\n")
writeData.write("\t\t\tthrow new Exception(\"SQL Error!!!\");\n")
writeData.write("\t\t}\n")
writeData.write("\t\treturn \"1\";\n")
writeData.write("\t}\n")
writeData.write("}\n")

# creating a Repository class
writeData = open(path + "/" + className + "Repository.java", 'w+')
writeData.write("package com." + projectName + ".usecases." + folderName + ";\n\n")
writeData.write("import com.uclo.inventory.persistence.models." + modelName + ";\n")
writeData.write("import org.springframework.data.jpa.repository.JpaRepository;\n")
writeData.write("import org.springframework.stereotype.Repository;\n\n")
writeData.write("@Repository\n")
writeData.write("public interface " + className + "Repository extends JpaRepository<" + modelName + ",Long> {\n")
# function to check the primary key
writeData.write("\t" + modelName + " findBy" + serviceNameForPk("And", "pk")+";\n")
writeData.write("}\n")
