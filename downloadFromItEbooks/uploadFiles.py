import os
from mega import Mega
import sys

mega = Mega()
m = mega.login(sys.argv[1],sys.argv[2])
directory = m.find("Books")
for file in os.listdir(sys.argv[3]):
    if (file != sys.argv[0]):
        try:
            mega.upload(arg, directory[0])
            print arg, "uploaded"
            os.remove(arg)
        except Exception,e:
            print e
