import json
with open("text1.json") as j1:
    data1=json.load(j1)
print("data1: ",data1)
with open("text2.json") as j2:
    data2=json.load(j2)
print("data2: ",data2)
# if data1==data2:
#     print("YEAH!!!!")
# else:
#     print("Oops")
assert data1!=data2
