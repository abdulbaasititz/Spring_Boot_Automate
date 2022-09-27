
#--------------------------------------
# Create Path and Folder
import os

def createFolder(parentDir,folderName):
    path = os.path.join(parentDir, folderName)
    if not os.path.exists(path):
        os.mkdir(path)
    daoPath=os.path.join(path, "dao")
    if not os.path.exists(daoPath):
        os.mkdir(daoPath)
    print("Created folder path is "+path)
    return path
