import os, re

directory = os.listdir('/Users/yubeenjo/Desktop/Capstone/obj')
os.chdir('/Users/yubeenjo/Desktop/Capstone/obj')
print ("hi")

for file in directory:
    for i in range(1, 61):
        path = "license_plate" + str(i) + ".txt"
        open_file = open(path, 'r')
        read_file = open_file.read()
        regex = re.compile('15')
        read_file = regex.sub('0', read_file)
        write_file = open(path, 'w')
        write_file.write(read_file)

print('hi')