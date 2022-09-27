print("Query debug process start ....")
# Find Table name and other attributes
pk={};pkType="";uk={};ukType=""
# -------------------
file = open("../GetData", "r")
name = []
flag = 0
check = ""
get = ""

columnName=[]
columnType=[]
i =0
toggle=-1
for line in file:
    fields = line.rstrip('\n').split(" ")
    for word in fields :
        check = word.rstrip(',()')

        if check != "NOT" and check != "NULL" and check != "CREATE" \
                and check != "KEY" and check != "AUTO_INCREMENT" and check != "DEFAULT" and check != "1":
            #print(check)
            get = 1
            if check == "TABLE":
                tableName = fields[i + 1]
                get=0
            if check == "UNIQUE":
                ukTemp = fields[i - 3].rstrip(',();')
                ukTemp = ukTemp.replace('(','')
                uk[ukTemp] = 'String'
                ukType = fields[i - 2].rstrip(',();')
                continue
            if check == "PRIMARY":
                pkTemp = fields[len(fields)-1].rstrip(',();')
                pkTemp = pkTemp.replace('(','')
                pk[pkTemp]='Integer'
                break;
        if get ==1:
            if tableName == word:
                toggle = 0
                continue
            if toggle == 0:
                columnName.append(check)
                toggle = 1
            else:
                columnType.append(check)
                toggle = 0
            get =0
        i=i+1

# print("tablename :"+tableName)
# print("primaryKey :"+str(pk))
# print("uniqueKey :"+str(uk))
# print("uniqueKeyType :"+ukType)
# print("Column Name and Column Type below :")
# print(columnName)
# print(columnType)
file.close()
# ----------------------