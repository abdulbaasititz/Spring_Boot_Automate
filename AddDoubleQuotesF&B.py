print("convvert into sql queries for spring boot");

getData = open('GetData', 'r')
writeData = open('output/WriteDataJpa', 'w+')
lines = getData.readlines()
# Strips the newline character
writeData.write("@Query(value=")
for line in lines:
    getVal = line.strip()
    writeData.write("\""+getVal+" \"+\n")
writeData.write(",nativeQuery = true)")
getData.close()
writeData.close()