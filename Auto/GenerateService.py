
def createService(path,pn,folderName,moduleName,className,modelName,uk,pk,cstQry,addAllOpt,delAllOpt):
    # service - > getPk1,getPk2,delData,setData,getAllData,getAllDataByPg
    print("Create service class")
    # creating a service class
    writeData = open(path + "/" + className + "Service.java", 'w+')

    writeData.write("package com." + pn + ".use_cases." + moduleName + "." + folderName + ";\n\n")
    writeData.write("import org.springframework.beans.factory.annotation.Autowired;\n")
    writeData.write("import org.springframework.data.domain.Page;\n")
    writeData.write("import org.springframework.stereotype.Service;\n")
    writeData.write("import java.util.List;\n")
    writeData.write("import com." + pn + ".helpers.utils.OffsetBasedPageRequest;\n")
    writeData.write("import com." + pn + ".persistence.models." + moduleName + "." + modelName + ";\n")
    if cstQry == 1:
        writeData.write(
            "import com." + pn + ".use_cases." + moduleName + "." + folderName + ".dao." + modelName + "CstPojo;\n")
    writeData.write("\n")
    writeData.write("@Service\n")
    writeData.write("public class " + className + "Service {\n\n")
    writeData.write("\t@Autowired\n")
    writeData.write("\t" + className + "Repository rep;\n")
    writeData.write("\n")
    writeData.write("\tpublic " + modelName + " getPk1(" + list(pk.values())[0] + " pk0) throws Exception {\n")
    writeData.write("\t\ttry {\n")
    writeData.write("\t\t\treturn rep.findBy" + list(pk.keys())[0] + "(pk0);\n")
    writeData.write("\t\t} catch (Exception e) {\n")
    writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
    writeData.write("\t\t}\n")
    writeData.write("\t}\n")
    writeData.write("\n")
    # get by id
    if len(uk) > 0:
        writeData.write("\tpublic " + modelName + " getPk2(" + list(uk.values())[0] + " pk0) throws Exception {\n")
        writeData.write("\t\ttry {\n")
        writeData.write("\t\t\treturn rep.findBy" + list(uk.keys())[0] + "(pk0);\n")
        writeData.write("\t\t} catch (Exception e) {\n")
        writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
        writeData.write("\t\t}\n")
        writeData.write("\t}\n")
        writeData.write("\n")
    # save
    writeData.write("\tpublic " + list(pk.values())[0] + " setData(" + modelName + " val) throws Exception {\n")
    writeData.write("\t\ttry {\n")
    writeData.write("\t\t\treturn rep.save(val).get" + list(pk.keys())[0] + "();\n")
    writeData.write("\t\t} catch (Exception e) {\n")
    writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
    writeData.write("\t\t}\n")
    writeData.write("\t}\n")
    writeData.write("\n")
    if addAllOpt == 1:
        # save all
        writeData.write("\tpublic void setAllData(List<" + modelName + "> val) throws Exception {\n")
        writeData.write("\t\ttry {\n")
        writeData.write("\t\t\trep.saveAll(val);\n")
        writeData.write("\t\t} catch (Exception e) {\n")
        writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
        writeData.write("\t\t}\n")
        writeData.write("\t}\n")
        writeData.write("\n")
    # delete
    writeData.write("\tpublic void delData(" + modelName + " val) throws Exception {\n")
    writeData.write("\t\ttry {\n")
    writeData.write("\t\t\trep.delete(val);\n")
    writeData.write("\t\t} catch (Exception e) {\n")
    writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
    writeData.write("\t\t}\n")
    writeData.write("\t}\n")
    writeData.write("\n")
    if delAllOpt == 1:
        # delete all
        writeData.write("\tpublic void delAllData(List<" + modelName + "> val) throws Exception {\n")
        writeData.write("\t\ttry {\n")
        writeData.write("\t\t\trep.deleteAll(val);\n")
        writeData.write("\t\t} catch (Exception e) {\n")
        writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
        writeData.write("\t\t}\n")
        writeData.write("\t}\n")
        writeData.write("\n")
    # get all
    writeData.write("\tpublic List<" + modelName + "> getAllData() throws Exception {\n")
    writeData.write("\t\ttry{\n")
    # writeData.write("\t\t\treturn rep.findByIsActive(true);\n")
    writeData.write("\t\t\treturn rep.findAll();\n")
    writeData.write("\t\t}catch (Exception e){\n")
    writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
    writeData.write("\t\t}\n")
    writeData.write("\t}\n")
    writeData.write("\n")
    # get all by pagination
    if len(uk) > 0:
        if cstQry == 1:
            writeData.write(
                "\tpublic Page<" + modelName + "CstPojo> getAllDataByPg(int st, int lt,String sk) throws Exception {\n")
        else:
            writeData.write(
                "\tpublic Page<" + modelName + "> getAllDataByPg(int st, int lt,String sk) throws Exception {\n")

        writeData.write("\t\ttry {\n")
        # writeData.write("\t\t\treturn rep.findByIsActiveAnd" + list(uk.keys())[
        #     0] + "ContainingIgnoreCase(true,sk,new OffsetBasedPageRequest(st, lt));\n")
        writeData.write("\t\t\treturn rep.findBy" + list(uk.keys())[
            0] + "ContainingIgnoreCase(true,sk,new OffsetBasedPageRequest(st, lt));\n")
        writeData.write("\t\t} catch (Exception e) {\n")
        writeData.write("\t\t\tthrow new Exception(e.getMessage());\n")
        writeData.write("\t\t}\n")
        writeData.write("\t}\n")

    writeData.write("}\n")
    writeData.close();