import stanza
import sys
import subprocess
import os
import json
import datetime
from urllib.request import urlopen
from zipfile import ZipFile
from pathlib import Path
import tqdm
from fst_lookup import FST
from thamizhilip import tamil
import time
#dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = str(Path.home())+"/thamizhi-models"

##word = 
##gussers=[]
##f1=open(dir_path+"/fsts/guesser-list","r")
##for line in f1:
##    gussers.append(line.strip())
##f1.close()
#print(gussers) #['adv-guess.fst', 'adj-guess.fst', 'verb-guess.fst', 'noun-guess.fst']

def find_morphemes(word):
        #reading fsts, fsts in fst_list has to be placed in a priority order in which look up should happen
        #this needs to be passed to the function using which morphemes are extracted
        fsts=['verb-c3.fst','verb-c-rest.fst','verb-c11.fst','verb-c4.fst','verb-c12.fst','verb-c62.fst']
##        f1=open(dir_path+"/fsts/fst-list","r")
##        for line in f1:
##                fsts.append(line.strip())
##        f1.close()
        analyses=[]
        for fst in fsts:
                p1 = subprocess.Popen(["echo", word], stdout=subprocess.PIPE)
                file_name=dir_path+"/fsts/"+fst
                #print(file_name)
                p2 = subprocess.Popen(['flookup',file_name], stdin=p1.stdout, stdout=subprocess.PIPE)
                p1.stdout.close()
                output,err = p2.communicate()
                #print(output.decode("utf-8"))

                #1st analysis is broken by new line to tackle cases with multiple analysis
                #then analysis with one output is handled
                #1st each line is broken by tab to find lemma and analysis
                #then those are store in a list and returned back to main

                lines=output.decode("utf-8").strip().split("\n")
                if len(lines) > 1:
                        #print(line)
                        for line in lines:
                                analysis=line.split()
                                if len(analysis) > 1:
                                        if "?" in output.decode("utf-8"):
                                                results=0
                                        else:
                                                #print(analysis[1].strip().split("+"))
                                                analyses.append(analysis[1].strip().split("+"))
                                else:
                                        return 0
                #this is to handle cases with one output, 1st each line is broken by tab to
                #find lemma and analysis
                #then those are store in a list and returned back to main
                else:
                        analysis=output.decode("utf-8").split()
                        if len(analysis) > 1:
                                if "?" in output.decode("utf-8"):
                                        results=0
                                else:
                                        #print(analysis[1].strip().split("+"))
                                        analyses.append(analysis[1].strip().split("+"))
                                        #print(analyses)
                        else:
                                return 0
                        
        #print(analyses)
        if analyses :
                return analyses
        else:
                return 0


def guess_morphemes(word):
        gussers=['verb-guess.fst']
##        f1=open(dir_path+"/fsts/guesser-list","r")
##        for line in f1:
##                gussers.append(line.strip())
##        f1.close()
        
        analyses=[]
        for fst in gussers:
                p1 = subprocess.Popen(["echo", word], stdout=subprocess.PIPE)
                file_name=dir_path+"/fsts/"+fst
                p2 = subprocess.Popen(["flookup", file_name], stdin=p1.stdout, stdout=subprocess.PIPE)
                p1.stdout.close()
                output,err = p2.communicate()
                #1st analysis is broken by new line to tackle cases with multiple analysis
                #then analysis with one output is handled
                #1st each line is broken by tab to find lemma and analysis
                #then those are store in a list and returned back to main

                lines=output.decode("utf-8").strip().split("\n")
                if len(lines) > 1:
                        for line in lines:
                                analysis=line.split("	")
                                if len(analysis) > 1:
                                        if "?" in output.decode("utf-8"):
                                                results=0
                                        else:
                                                #print(analysis[1].strip().split("+"))
                                                analyses.append(analysis[1].strip().split("+"))
                                else:
                                        return 0

                #this is to handle cases with one output, 1st each line is broken by tab to
                #find lemma and analysis
                #then those are store in a list and returned back to main
                analysis=output.decode("utf-8").split("	")
                if len(analysis) > 1:
                        if "?" in output.decode("utf-8"):
                                results=0
                        else:
                                #print(analysis[1].strip().split("+"))
                                analyses.append(analysis[1].strip().split("+"))
                else:
                        return 0
        if analyses :
                return analyses
        else:
                return 0





#In order to use the dependency parser, you always need to load various models. 
depModel=tamil.loadModels()

#Then you can load them as shown below, 
#when parsing a sentence. Need to feed one sentence at a time. 
#print(tamil.depTag(sentence,depModel))
file_name=dir_path+"/fsts/"+"verb-guess.fst"
verbfst = FST.from_file(file_name)
#guess = list(verbfst.generate(word))

fsts_files=['verb-c3.fst','verb-c-rest.fst','verb-c11.fst','verb-c4.fst','verb-c12.fst','verb-c62.fst']

#print(guess)


def make_sent(sent_obj):
    changed_sent = []
    for word in sent_obj.words:
        if word.text.strip()!= "." :#not in changed_sent:
            changed_sent.append(word.text.strip())
    changed_sent.append(".")
        #if word.text.strip() != ".":
             #+= word.text + " changed_sent"   
        #else:
            #changed_sent += word.text
    return " ".join(changed_sent).strip()



def change_verb(strm,word,sent,data_input,tag,right_tag):
    #print(morph)
    
    #tmp=morph.copy()
    t = strm.split("+")
    t[-1] = tag
    change = '+'.join(t).strip()
    #print(change)
    changed_word =[]
    
    for fst in fsts_files:
        file_name=dir_path+"/fsts/"+fst
        _fst = FST.from_file(file_name)
        _verbfst = list(_fst.generate(change))
        changed_word += _verbfst

    #print(changed_word)
    if len(changed_word) == 0:
        #print("inguess")
        changed_word += list(verbfst.generate(change))
    #print(changed_word)
    if len(changed_word) == 1:
        word.text = changed_word[0]
        changed_sent = sent.text #make_sent(sent)
        save_data = data_input + '\t'+ changed_sent +'\t'+right_tag+'\t'+tag+'\t'+right_tag[0:1]+'\t'+right_tag[1:3]+'\t'+right_tag[3:]+'\n'
        f2 = open("train_news.tsv", "a",encoding='UTF-8')
        f2.write(save_data)
        f2.close()
        #print(save_data)
    elif len(changed_word) > 1:
        #print("Hello")
        for i in range(1,len(changed_word)):
            word.text = changed_word[i]
            changed_sent = make_sent(sent)
            save_data = data_input + '\t'+ changed_sent +'\t'+right_tag+'\t'+tag+'\t'+right_tag[0:1]+'\t'+right_tag[1:3]+'\t'+right_tag[3:]+'\n'

            #save_data = data_input + '\t'+ changed_sent + '\t' +'number'+'\n'
            f2 = open("train_news.tsv", "a",encoding='UTF-8')
            f2.write(save_data)
            f2.close()
            #print(save_data)
    else:
        print("Hi")         
def change_sentence(morph,word,sent,data_input):
    tmp=morph.copy()
    strm="+".join(morph[0])
    tags = ['1pl',"1sg","2pl","2pl","2plh","2sg","2sgh","2sgm","2sgf","3ple","3plhe","3pln","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn']
    for tag in tags:
        if morph[0][-1] == tag:
            continue
        change_verb(strm,word,sent,data_input,tag=tag,right_tag=morph[0][-1])
    
def depTag(data_input,nlp):
        doc = nlp(data_input+ " .")
        taggeddata=data_input+"\t"
        #print(taggeddata)
        for sent in doc.sentences :
            #print(sent)
            for word in sent.words :
                #print(word.deprel,word.upos)
                if word.deprel == "root" and word.upos == "VERB":
                    #print(list(verbfst.analyze(word.text)))
                    #print(type(word.text))
                    
                    if find_morphemes(word.text) != 0:
                        morphs = find_morphemes(word.text)
                     
                        #print("inside finding")
                        if len(morphs) == 1 and len(morphs[0])>0:
                            #print("indng")
                            #print(morphs)
                            change_sentence(morphs,word,sent,data_input)
                            #print(morphs)
                            #change_gender(morphs,word,sent,data_input)
                            #change_person(morphs,word,sent,data_input)
                        elif len(morphs) > 1:
                            #for morph in morphs:
                            #print("iinding")
                            change_sentence(morphs,word,sent,data_input)
                            #change_gender(morphs,word,sent,data_input)
                            #change_person(morphs,word,sent,data_input)
                        else:
                            None #print("inside_fineding not have morphemes")
                    else:
                        if guess_morphemes(word.text):
                            
                            #print("inside guessing")
                            morphs = guess_morphemes(word.text) 
                           
                            if len(morphs) == 1 and len(morphs[0])>0:
                                #print("in")
                                change_sentence(morphs,word,sent,data_input)
                                #change_gender(morphs,word,sent,data_input)
                                #change_person(morphs,word,sent,data_input)
                            elif len(morphs) > 1:
                                #for morph in morphs:
                                change_sentence(morphs,word,sent,data_input)
                                #change_gender(morphs,word,sent,data_input)
                                #change_person(morphs,word,sent,data_input)

                        else:
                            None#print("inside guessing not have morphemes")
                        
               # taggeddata=taggeddata+str(word.id)+ "|" + word.upos + "|" + str(word.deprel)+ "|" + str(word.head) + "\n"
#        return taggeddata



#print(depTag(sentence,depModel))
from os import listdir
from os.path import isfile, join

mypath = "./data/"
onlyfiles = []
for f in listdir(mypath):
    if isfile(join(mypath,f)):
        onlyfiles.append(f)
#files = #['train_final.tsv']#,'valid_2.tsv']#['test.tsv','test_1.tsv','test_2.tsv','test_3.tsv','test_4.tsv','test_5.tsv','test_6.tsv','test_7.tsv','test_8.tsv','hiru news.txt']#
for file in onlyfiles:
        f1=open("./data/"+file,"r",encoding='UTF-8')
        print("Starting with file: "+file)
        sentence_count =0

        for line in f1:
            sentence = line.strip('"')#.split("\t")[0]

            depTag(sentence,depModel)
            sentence_count+=1
            if sentence_count%100==0:
                time.sleep(5)
                print(sentence_count)
        print("Ending file: "+file)
    


















