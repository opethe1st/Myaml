import myaml
from pprint import pprint


with open('demo.yaml') as file:
    d1 = myaml.load(string=file.read())

with open('demo2.yaml') as file:
    d2 = myaml.load(string=file.read())


pprint(d1)
pprint(d2)
print(d1 == d2)
