# myaml - Minimal YAML
myaml stands for minimal yaml. It is a subset of Yaml and supports only the basic features. Wrote this so flex my specification implementation muscles.


### How to use
To use myaml,
```bash
pip install myaml
```
```python
import myaml

with open('blah.oyml') as file:
    d = myaml.parse(file.read())

```
