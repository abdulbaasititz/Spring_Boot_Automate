#Convert query to model
#--------------------------------------
pn = "itz.scs" #Project Name
tableName = "CarBrand"

# it should be same name which create in model folder #- PascalCase
modelName = "CarBrand"
# common name for all cntrl,service - PascalCase
className = "CarBrand"
# object name for class camelCase
baseName = "carBrand"
# SHould be underscore snake_case
folderName = "car_brand"
# SHould be hipen snake_case
apiName = "car-brand"
# Generate Pk,FK,unique to set,get data in db
pk = {"Id": "Integer"}
uk = {"Name": "String"}
fk = [{"ItemId": "String","ItemSku": "String"},{"ItemId": "String","VariantId": "String"}]
createdBy = "Abdul Baasit"
#--------------------------------------

import os

parent_dir = "E:/pycharm/spring-boot-automation/output"
print("Create a controller , service & repo ")

# creating a service class
writeData = open("output/" + className + "Service.java", 'w+')

writeData.write("package com."+pn+".usecases."+folderName+";\n\n")
writeData.write("\n")
writeData.write("import org.springframework.beans.factory.annotation.Autowired;\n")
writeData.write("import org.springframework.data.domain.Page;\n")
writeData.write("import org.springframework.data.domain.PageRequest;\n")
writeData.write("import org.springframework.stereotype.Service;\n")
writeData.write("import java.util.List;\n")
writeData.write("\n")
writeData.write("import com."+pn+".persistence.models." + modelName + ";\n")
writeData.write("\n")
writeData.write("@Service\n")
writeData.write("public class "+className+"Service {\n")
writeData.write("\t@Autowired\n")
writeData.write("\t" + className + "Repository rep;\n")
writeData.write("\n")
writeData.write("\tpublic "+modelName+" getPk1("+list(pk.values())[0]+" pk0) throws Exception {\n")
writeData.write("\t\ttry {\n")
writeData.write("\t\t\treturn rep.findBy"+list(pk.keys())[0]+"(pk0);\n")
writeData.write("\t\t} catch (Exception e) {\n")
writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
writeData.write("\t\t}\n")
writeData.write("\t}\n")
writeData.write("\n")
#get by id
writeData.write("\tpublic "+modelName+" getPk2("+list(uk.values())[0]+" pk0) throws Exception {\n")
writeData.write("\t\ttry {\n")
writeData.write("\t\t\treturn rep.findBy"+list(uk.keys())[0]+"(pk0);\n")
writeData.write("\t\t} catch (Exception e) {\n")
writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
writeData.write("\t\t}\n")
writeData.write("\t}\n")
writeData.write("\n")
#save
writeData.write("\tpublic "+list(pk.values())[0]+" setData("+modelName+" val) throws Exception {\n")
writeData.write("\t\ttry {\n")
writeData.write("\t\t\treturn rep.save(val).get"+list(pk.keys())[0]+"();\n")
writeData.write("\t\t} catch (Exception e) {\n")
writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
writeData.write("\t\t}\n")
writeData.write("\t}\n")
writeData.write("\n")
#delete
writeData.write("\tpublic void delData("+modelName+" val) throws Exception {\n")
writeData.write("\t\ttry {\n")
writeData.write("\t\t\trep.delete(val);\n")
writeData.write("\t\t} catch (Exception e) {\n")
writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
writeData.write("\t\t}\n")
writeData.write("\t}\n")
writeData.write("\n")
#get all
writeData.write("\tpublic List<"+modelName+"> getAllData() throws Exception {\n")
writeData.write("\t\ttry{\n")
writeData.write("\t\t\treturn rep.findByIsActive(true);\n")
writeData.write("\t\t}catch (Exception e){\n")
writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
writeData.write("\t\t}\n")
writeData.write("\t}\n")
writeData.write("\n")
#get all by pagination
writeData.write("\tpublic Page<"+modelName+"> getAllDataByPg(int pn, int ps) throws Exception {\n")
writeData.write("\t\ttry {\n")
writeData.write("\t\t\treturn rep.findByIsActive(true,PageRequest.of(pn, ps));\n")
writeData.write("\t\t} catch (Exception e) {\n")
writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
writeData.write("\t\t}\n")
writeData.write("\t}\n")
writeData.write("}\n")

writeData.close();
# service - > getPk1,getPk2,delData,setData,getAllData,getAllDataByPg

# creating a service class
writeData = open("output/" + className + "Repository.java", 'w+')

writeData.write("package com."+pn+".usecases."+folderName+";\n")
writeData.write("import com."+pn+".persistence.models." + modelName + ";\n")
writeData.write("import org.springframework.data.domain.Page;\n")
writeData.write("import org.springframework.data.domain.Pageable;\n")
writeData.write("import org.springframework.data.jpa.repository.JpaRepository;\n")
writeData.write("import org.springframework.stereotype.Repository;\nimport java.util.List;\n")
writeData.write("\n")
writeData.write("@Repository\n")
writeData.write("public interface "+className+"Repository extends JpaRepository<"+modelName+",Long> {\n")
writeData.write("\t"+modelName+" findBy"+list(pk.keys())[0]+"("+list(pk.values())[0]+" pk0);\n")
writeData.write("\t"+modelName+" findBy"+list(uk.keys())[0]+"("+list(uk.values())[0]+" pk0);\n")
writeData.write("\tList<"+modelName+"> findByIsActive(boolean b);\n")
writeData.write("\tPage<"+modelName+"> findByIsActive(boolean b, Pageable pg);\n")
writeData.write("}\n")
