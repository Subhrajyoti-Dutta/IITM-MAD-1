import sys
import pyhtml as h
import jinja2 as j
import matplotlib.pyplot as plt

req = sys.argv[1]
req_id = sys.argv[2]

data = open('data.csv', 'r').read()
print(type(data))

# if req == '-c' and req_id in :
    # pass