import importlib
import testq
importlib.reload(testq)
z = testq.convertToRaw("ksuk\tsdf")
print(z)