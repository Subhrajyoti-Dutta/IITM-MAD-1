import pyhtml as h
import inspect

# print(inspect.getsource((h.td)))
print(h.td("Hello","2"),h.td(colspan="2")("Hello"))