import os

parent_dir = "E:/pycharm/spring-boot-automation/output"


print("Create a controller , service & repo ")

projectName = "inventory"
tableName = "DOHDRTABLE"
modelName = "DoHdr"
className = "DoHeader"
baseName = "doHeader"
primaryKey = "DoNo"
createdBy = "abdul"

# Creating a new directory
path = os.path.join(parent_dir, baseName)
os.mkdir(path)
print(path)
# creating a controller class
writeData = open(path+"/"+className+"Controller.java",'w+')
writeData.write("package com.uclo."+projectName+".usecases."+baseName+";\n\n")
writeData.write("import org.springframework.web.bind.annotation.RequestMapping;\n")
writeData.write("import org.springframework.web.bind.annotation.RestController;\n")
writeData.write("import org.springframework.web.bind.annotation.RequestMethod;\n")
writeData.write("import org.springframework.beans.factory.annotation.Autowired;\n")
writeData.write("import org.springframework.http.ResponseEntity;\n")
writeData.write("import javax.servlet.http.HttpServletRequest;\n")
writeData.write("import org.springframework.web.bind.annotation.RequestBody;\n")
writeData.write("import com.uclo.inventory.persistence.models."+modelName+";\n")
writeData.write("import com.uclo.inventory.helpers.common.token.ClaimsDao;\n")
writeData.write("import com.uclo.inventory.helpers.common.calc.DateTimeCalc;\n")
writeData.write("import com.uclo.inventory.helpers.common.token.ClaimsSet;\n")
writeData.write("import org.springframework.http.HttpStatus;\n\n")
writeData.write("\n")
writeData.write("\n")

writeData.write("@RestController\n@RequestMapping(\"${spring.base.path}\")\n")
writeData.write("public class "+className+"Controller {\n")

writeData.write("\t@Autowired\n")
writeData.write("\t"+className+"Service "+baseName+"Service;\n")
writeData.write("\t@Autowired\n")
writeData.write("\tClaimsSet claimsSet;\n")

writeData.write("\t@RequestMapping(value = \"/set-"+baseName+"/new\", method = RequestMethod.POST)\n")
writeData.write("\tpublic ResponseEntity<?> new"+baseName+"(HttpServletRequest request,")
writeData.write("@RequestBody "+modelName+" val) throws Exception {\n")
writeData.write("\t\tClaimsDao claimsDao = claimsSet.getClaimsDetailsAfterSet(request.getHeader(\"Authorization\"));\n")

writeData.write("\t\tString plant = claimsDao.getPlt();\n")
writeData.write("\t\tString sub = claimsDao.getSub();\n")
writeData.write("\t\tString empId = claimsDao.getEid();\n")
writeData.write("\t\tDateTimeCalc dateTimeCalc = new DateTimeCalc();\n")

writeData.write("\t\tString createdAt = dateTimeCalc.getUcloTodayDateTime();\n")
writeData.write("\t\tString createdBy = \""+createdBy+"\";\n")
writeData.write("\t\tString valCheck = "+baseName+"Service.check"+modelName+"Pk(val.get"+primaryKey+"());\n")
writeData.write("\t\tif(valCheck == \"1\"){\n")

writeData.write("\t\t\t"+baseName+"Service.set"+modelName+"Details(val);\n")
writeData.write("\t\t}else{\n")
writeData.write("\t\t\tthrow new Exception(\"value already set\");\n")
writeData.write("\t\t}\n")
writeData.write("\treturn new ResponseEntity<>(\"Success\", HttpStatus.OK);")
writeData.write("\t}\n")
writeData.write("}\n")

# creating a service class
writeData = open(path+"/"+className+"Service.java",'w+')
writeData.write("package com.uclo."+projectName+".usecases."+baseName+";\n\n")
writeData.write("import org.springframework.beans.factory.annotation.Autowired;\n")
writeData.write("import org.springframework.stereotype.Service;\n")
writeData.write("import com.uclo.inventory.persistence.models."+modelName+";\n")
writeData.write("@Service\n")
writeData.write("public class "+className+"Service {\n")
writeData.write("\t@Autowired\n")
writeData.write("\t"+className+"Repository "+baseName+"Repository;\n")
# function to check the primary key
writeData.write("\tpublic String check"+modelName+"Pk(String val) throws Exception {\n")
writeData.write("\t\ttry {\n")
writeData.write("\t\t\t"+modelName+" getVal = "+baseName+"Repository.findBy"+primaryKey+"(val);\n")
writeData.write("\t\t\tif(getVal == null)\n")
writeData.write("\t\t\t\treturn \"1\";\n")
writeData.write("\t\t} catch (Exception e) {\n")
writeData.write("\t\t\tthrow new Exception(\"SQL Error!!!\");\n")
writeData.write("\t\t}\n")
writeData.write("\treturn \"0\";\n")
writeData.write("\t}\n")
# function to save the model
writeData.write("\tpublic String set"+modelName+"Details("+modelName+" val) throws Exception {\n")
writeData.write("\t\ttry {\n")
writeData.write("\t\t\t"+baseName+"Repository.save(val);\n")
writeData.write("\t\t} catch (Exception e) {\n")
writeData.write("\t\t\tthrow new Exception(\"SQL Error!!!\");\n")
writeData.write("\t\t}\n")
writeData.write("\t\treturn \"1\";\n")
writeData.write("\t}\n")
writeData.write("}\n")

# creating a Repository class
writeData = open(path+"/"+className+"Repository.java",'w+')
writeData.write("package com.uclo."+projectName+".usecases."+baseName+";\n\n")
writeData.write("import com.uclo.inventory.persistence.models."+modelName+";\n")
writeData.write("import org.springframework.data.jpa.repository.JpaRepository;\n")
writeData.write("import org.springframework.stereotype.Repository;\n\n")
writeData.write("@Repository\n")
writeData.write("public interface "+className+"Repository extends JpaRepository<"+modelName+",Long> {\n")
# function to check the primary key
writeData.write("\t"+modelName+" findBy"+primaryKey+"(String val);\n")
writeData.write("}\n")