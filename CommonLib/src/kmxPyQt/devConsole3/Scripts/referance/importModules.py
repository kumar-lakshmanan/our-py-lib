import kumarx
import imp
import sys

for t in sys.modules.keys():
        mod = sys.modules[t]
        if (mod):
                imp.reload(mod)
                        
import importlib
importlib.reload(kumarx)
print(kumarx.getInfo(1))
                        