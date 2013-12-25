# About

This program parses a file containing one rect and one path SVG elements.
After the parsing, the information is processed to output a data
structure convenient to test the first part of the SCAD course's project
at UE, which deals with the use of HMMs. That output is composed of a Markov
Chain matrix and an Observation matrix, following the conventions used during
the classes.

# How to Use

Just include the module **path\_maker.py** and use the function **generateMatrices(file\_name)**. Take the following code as an example:

```python
# test_path_maker.py
import sys
from path_maker import generateMatrices

# Take arguments
if len(sys.argv) != 2:
    print "Usage: test_path_maker input_file"
    exit()

mc, om = generateMatrices(sys.argv[1])
print mc
print om
```

The function **generateMatrices(file\_name)** takes one argument which is the name of the file that contains one SVG *path* element and one SVG *rect* element.

Note that the *path* element can only be defined using the *L* instruction as defined by the [W3C recommendation](http://www.w3.org/TR/2000/CR-SVG-20001102/paths.html#PathDataLinetoCommands). The other instructions were not implemented.

