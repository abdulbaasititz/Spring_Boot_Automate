# Accessing a text file - www.101computing.net/mp3-playlist/

file = open("GetData", "r")
name = []
flag = 0
for line in file:
    fields = line.rstrip('\n').split(" ")
    for word in fields :
        if flag == 1:
            print(word.rstrip(','))

            flag = 0
        if word == 'as':
            flag = 1
    #print(fields)

# It is good practice to close the file at the end to free up resources
file.close()