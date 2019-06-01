# Myaml - Minimal YAML
This is a code kata that implements a subset of the yaml spec.
It is NOT intended to be used by anyone. It's just a way for me to deliberately practice my software engineering skills (design in particular)

You can demo the code here


[![Edit on repl.it](https://repl-badge.jajoosam.repl.co/edit.png)](https://repl.it/github/https://github.com/opethe1st/myaml?lang=python&ref=button)


### How to use this library
-----
To use myaml, clone this repo, then do.
```bash
cd src/
pip install .
```
create a yaml file called `blah.yaml` that has some yaml in it.
Then do this

```python
import myaml


with open('blah.yaml') as file:
    blah = myaml.load(file.read())

```

## How to write the Myaml
----
Myaml support three types.
* Mappings
* Sequences
* Scalars

### *Scalars*

Scalars represent strings (they could also represent other primitive types but only strings are supported at the moment)

Mappings and Sequences are the collection types. They are recursive structures i.e they can contain other mappings and sequences.

### *Mappings*

Mappings correspond to dictionaries and can be nested.
The key has to be a scalar and the value can be a scalar like in the example below
```yaml
key: value
```
or the value can be a mapping that is indented one level more than the key
```yaml
key:
    key2: value
    key3: value
```
or the value can be a sequence that is indented one level more than the key
```yaml
key:
    - value
    - valu3
```
or look like this example, that has keys with values of different types
```yaml
key:
    key: value
key2:
    - value
key3: value
```

### *Sequences*

Sequences corresponds to arrays.
An item in a sequence is denoted by a `- ` where the length of this should be equal to the indentSize(number of spaces that make up an indent).
Here are some examples
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
