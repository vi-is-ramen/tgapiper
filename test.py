import os
import importlib


for m in  os.listdir(os.path.dirname(__file__) + '/tg/methods'):
    if m.startswith("__"):
        continue
    mod = importlib.import_module('tg.methods.' + m[:-3])
    # print(m[:-3])


for m in  os.listdir(os.path.dirname(__file__) + '/tg/types'):
    if m.startswith("__"):
        continue
    mod = importlib.import_module('tg.types.' + m[:-3])
    # print(m[:-3])
