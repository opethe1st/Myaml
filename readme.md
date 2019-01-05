# myaml - Minimal YAML
myaml stands for minimal yaml. It is a subset of Yaml and supports only the basic features. Wrote this so I flex my specification implementation muscles.


### How to use this library
To use myaml,
```bash
pip install myaml
```

```python
import myaml

with open('blah.oyml') as file:
    d = myaml.parse(file.read())

```

### How to write the myaml
Myaml support three types.
Mappings, Sequence and Scalars.
Mappings are written as key values. Here are some examples
```yaml
key: value
```
or
```yaml
key:
    key2: value
    key3: value
```
or
```yaml
key:
    - value
    - valu3
```

Sequences corresponds to arrays. Here are some examples
```yaml
-   value
-   value3
```
or
```yaml
-   key: value
-   key:
        key3: value
-   value
```

Right now, it only support strings as scalars. This will change in the future
```yaml
string value
```
