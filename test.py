lst = [1,2,3,4,5,6,7,8,9]

for l in lst:
    if l % 2 == 0:
        print(l)
    else:
        continue
    if l == 3:
        print('this should not print')



content = [1,2,3,4,5,6,'word']
print(content[6][1:-1])