from pprint import pprint

import yaml

import myaml

with open('demo.yaml') as file:
    string = file.read()
    d1 = myaml.load(string=string)
    d2 = yaml.load(stream=string, Loader=yaml.SafeLoader)

# demonstrate that yaml and myaml give the same result! :)
print(d1 == d2)
