text = ['40-60','60-80']
print(text[1].split('-'))
textdata = []
for elem in text:
    textdata.append(elem.split('-'))
print(textdata)
intdata = []
for elem in textdata:
    intdata.append((int(elem[0])+int(elem[1]))/2.0)
print(intdata)