# myaml - Minimal YAML
myaml stands for minimal yaml. It is a subset of Yaml and supports only the basic features. I wrote this to flex my specification implementation muscles.


### How to use this library
To use myaml,
```bash
pip install myaml
```

```python
import myaml

with open('blah_m.yml') as file:
    d = myaml.parse(file.read())

```

### How to write the myaml
Myaml support three types.
Mappings, Sequences and Scalars.
Mappings are written as key values and they can be nested. Here are some examples. Please, note that right now, we only support indenting by 4 spaces. It is currently undefined
what happens when you used spaces that are not multiplies of 4.
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
or
```yaml
key:
    key: value
key2:
    - value
key3: value
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

Right now, it only support strings as scalars. This could change in the future
```yaml
string value
```
