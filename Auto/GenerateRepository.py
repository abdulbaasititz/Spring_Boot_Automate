
def createRepository(path,pn,folderName,moduleName,className,modelName,uk,pk,cstQry,selectQry):
    print("Create repository class")
    # creating a Repo class
    writeData = open(path + "/" + className + "Repository.java", 'w+')

    writeData.write("package com." + pn + ".use_cases." + moduleName + "." + folderName + ";\n\n")
    writeData.write("import com." + pn + ".persistence.models." + moduleName + "." + modelName + ";\n")
    writeData.write("import org.springframework.data.domain.Page;\n")
    writeData.write("import org.springframework.data.domain.Pageable;\n")
    writeData.write("import org.springframework.data.jpa.repository.JpaRepository;\n")
    writeData.write("import org.springframework.stereotype.Repository;\nimport java.util.List;\n")
    if cstQry == 1:
        writeData.write(
            "import com." + pn + ".use_cases." + moduleName + "." + folderName + ".dao." + modelName + "CstPojo;\nimport org.springframework.data.jpa.repository.Query;\n")

    writeData.write("\n")
    writeData.write("@Repository\n")
    writeData.write("public interface " + className + "Repository extends JpaRepository<" + modelName + ",Long> {\n")
    writeData.write("\t" + modelName + " findBy" + list(pk.keys())[0] + "(" + list(pk.values())[0] + " pk0);\n")
    # writeData.write("\tList<"+modelName+"> findByIsActive(boolean b);\n")
    if len(uk) > 0:
        writeData.write("\t" + modelName + " findBy" + list(uk.keys())[0] + "(" + list(uk.values())[0] + " pk0);\n")

    if len(uk) > 0:
        if cstQry == 1:
            writeData.write(
                "\t@Query(value = \"" + selectQry + "\",nativeQuery = true,countQuery = \"SELECT count(t1.Id) FROM " +
                selectQry.split("from")[1] + "\")\n")
            # writeData.write("\tPage<" + modelName + "CstPojo> findByIsActiveAnd" + list(uk.keys())[
            #     0] + "ContainingIgnoreCase(boolean b,String searchKey,Pageable of);\n")
            writeData.write("\tPage<" + modelName + "CstPojo> findBy" + list(uk.keys())[
                0] + "ContainingIgnoreCase(boolean b,String searchKey,Pageable of);\n")
        else:
            # writeData.write("\tPage<" + modelName + "> findByIsActiveAnd" + list(uk.keys())[
            #     0] + "ContainingIgnoreCase(boolean b,String searchKey,Pageable of);\n")
            writeData.write("\tPage<" + modelName + "> findBy" + list(uk.keys())[
                0] + "ContainingIgnoreCase(boolean b,String searchKey,Pageable of);\n")

    writeData.write("}\n")