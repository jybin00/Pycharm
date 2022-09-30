a = ['승연', '구현', '유빈']
b = [1, 2, 3]
c = a + b

a = open("hi.txt", "w")

for i in c:
    a.write(str(i) + "\n")
    print(i)

a.close()