from os import listdir
from os.path import isfile, join

mypath = "./data/"
onlyfiles = []
for f in listdir(mypath):
    if isfile(join(mypath,f)):
        onlyfiles.append(f)
print(onlyfiles)
