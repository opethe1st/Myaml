import myaml
from pprint import pprint


with open('demo.yaml') as file:
    d = myaml.parse(string=file.read())


pprint(d)
