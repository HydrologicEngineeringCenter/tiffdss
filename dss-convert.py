import sys
from hec.heclib.util import Heclib
from hec.heclib.dss import HecDss, DSSPathname, HecDataManager,HecDSSUtilities

#def gridCompare()

dss7=sys.argv[1]
dss6=sys.argv[2]
print(dss7)
print(dss6)

u = HecDSSUtilities()
u.setDSSFileName(dss7)
status = u.convertVersion(dss6)
u.close()
if status != 0:
    print("error converting ")

#gridCompare(dss7,dss7)
