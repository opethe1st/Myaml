

import cProfile
import pstats
import time
import timeit

import yaml

import myaml

with open('benchmarks/sample.yaml') as f:
    string = f.read()
    times = 500
    print(timeit.timeit(stmt='myaml.load(string)', number=times, globals=globals()))
    print(timeit.timeit(stmt='yaml.load(string, Loader=yaml.SafeLoader)', number=times, globals=globals()))

    cProfile.run(statement='for i in range(100):   myaml.load(string)', sort='time')
    cProfile.run(statement='for i in range(100):   yaml.load(string, Loader=yaml.SafeLoader)', sort='time')
