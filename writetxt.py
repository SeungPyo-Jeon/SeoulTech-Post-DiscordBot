print('original file')
with open('a.txt','r') as f:
    print(f.read())

with open('a.txt','w') as f:
    f.write("nice to me you to")
print('written file')
with open('a.txt','r') as f:
    print(f.read())    