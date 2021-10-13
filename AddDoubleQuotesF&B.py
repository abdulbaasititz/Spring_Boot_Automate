print("convert into sql queries for spring boot");

getData = open('GetData', 'r')
writeData = open('output/WriteDataJpa', 'w+')
lines = getData.readlines()
# Strips the newline character
# writeData.write("@Query(value=")
for line in lines:
    getVal = line.replace('\t', '\\t')
    getVal = getVal.replace('\"', '\\"').strip()
    writeData.write("writeData.write(\""+getVal+"\\n\")\n");
# writeData.write(",nativeQuery = true)")
getData.close()
writeData.close()