import Config as cnf

import QueryDebug as qd

import GenerateFolder as gf
folderName = '_'.join([x.lower() for x in cnf.re.findall('[A-Z][^A-Z]*', qd.tableName)]) # Should be underscore snake_case
path = gf.createFolder(cnf.parentDir,folderName);


import GenerateModel
# create model
className = qd.tableName # common name for all cntrl,service - PascalCase
GenerateModel.generateModel(cnf.pn, qd.tableName, className, qd.columnType, qd.columnName);

import  GenerateDao

selectQry = GenerateDao.generateDao(path,cnf.pn,folderName,cnf.moduleName, qd.tableName, className, qd.columnType, qd.columnName,cnf.cstQry)



import GenerateController
apiName = folderName.replace('_','-') # Should be hipen snake_case
modelName = qd.tableName # it should be same name which create in model folder #- PascalCase
GenerateController.createController(path, cnf.pn, folderName, cnf.moduleName, apiName, className, modelName, qd.uk,
                                    qd.pk, cnf.cstQry, cnf.addAllOpt, cnf.delAllOpt);

import GenerateService
GenerateService.createService(path, cnf.pn, folderName, cnf.moduleName, className, modelName, qd.uk,
                                    qd.pk, cnf.cstQry, cnf.addAllOpt, cnf.delAllOpt);

import GenerateRepository
GenerateRepository.createRepository(path,cnf.pn,folderName,cnf.moduleName,className,modelName,qd.uk,
                                    qd.pk,cnf.cstQry, selectQry)


baseName = ''.join([qd.tableName[0].lower() + qd.tableName[1:]]) # object name for class camelCase
