from os import listdir
from os.path import isfile, join

mypath = "./train/"
onlyfiles = []
for f in listdir(mypath):
    if isfile(join(mypath,f)):
        onlyfiles.append(f)
#print(onlyfiles)
#onlyfiles = ['train_train_new_1.tsv']
full_count =0
for file in onlyfiles:
        f1 = open("./train/"+file,"r",encoding='UTF-8')
        f2 = open("train_final.tsv", "a",encoding='UTF-8')
        print("Starting with file: "+file)
        
        sentence_count = 0
        for line in f1:
            sentence_count+=1
            sentence = line
            f2.write(sentence)
        full_count+=sentence_count
        print(sentence_count)
print(full_count)            