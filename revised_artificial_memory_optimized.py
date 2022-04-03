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



             
def change_sentence(morph,word,sent,data_input):
    #tmp=morph
    #strm="+".join(morph[0])
    #first_tags = ['1pl',"1sg","2pl","2plh","2sg","2sgh","2sgm","2sgf","3ple","3plhe","3pln","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn']
    
    dict = {
            '3sgf':['1pl',"2pl","2plh","3ple","3plhe","3pln","3sgm","3sgn"],
            '1pl':["1sg","2sg","2sgh","2sgm","2sgf","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn',"2pl","2plh","3ple","3plhe","3pln"],
            "1sg":['1pl',"2pl","2plh","3ple","3plhe","3pln","2sg","2sgh","2sgm","2sgf","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn'],
            "2pl":["1sg","2sg","2sgh","2sgm","2sgf","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn','1pl','3ple','3plhe','3pln'],
            "2plh":["1sg","2sg","2sgh","2sgm","2sgf","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn','1pl','3ple','3plhe','3pln'],
            "2sg":['1pl',"2pl","2plh","3ple","3plhe","3pln","1sg","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn'],
            "2sgh":['1pl',"2pl","2plh","3ple","3plhe","3pln","1sg","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn'],
            "2sgm":['1pl',"2pl","2plh","3ple","3plhe","3pln","1sg","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn'],
            "2sgf":['1pl',"2pl","2plh","3ple","3plhe","3pln","1sg","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn'],
            "3ple":["1sg","2sg","2sgh","2sgm","2sgf","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn','1pl','2pl','2plh'],
            "3plhe":["1sg","2sg","2sgh","2sgm","2sgf","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn','1pl','2pl','2plh'],
            "3pln":["1sg","2sg","2sgh","2sgm","2sgf","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn','1pl','2pl','2plh'],
            "3sge":['1pl',"2pl","2plh","3ple","3plhe","3pln","1sg","2sg","2sgh","2sgm","2sgf"],
            "3sgf":['1pl',"2pl","2plh","3ple","3plhe","3pln","1sg","2sg","2sgh","2sgm","2sgf"],
            "3sgh":['1pl',"2pl","2plh","3ple","3plhe","3pln","1sg","2sg","2sgh","2sgm","2sgf"],
            "3sghe":['1pl',"2pl","2plh","3ple","3plhe","3pln","1sg","2sg","2sgh","2sgm","2sgf"],
            "3sgm":['1pl',"2pl","2plh","3ple","3plhe","3pln","3sgf","3sgn","1sg","2sg","2sgh","2sgm","2sgf"],
            '3sgn':['1pl',"2pl","2plh","3ple","3plhe","3pln","3sgf","3sgm","1sg","2sg","2sgh","2sgm","2sgf"]     
    }
    
    if morph[0][-1] in dict.keys():
        lst = dict[ morph[0][-1]]
        for tag in lst:
            t = morph[0]#strm.split("+")
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
                changed_sent = make_sent(sent)#sent.text #make_sent(sent)
                save_data = data_input + '\t'+ changed_sent +'\t'+right_tag+'\t'+tag+'\t'+right_tag[0:1]+'\t'+right_tag[1:3]+'\t'+right_tag[3:]+'\n'
                #f2 = open("train_newssfirst.tsv", "a",encoding='UTF-8')
                f2.write(save_data)
                #f2.close()
                #print(save_data)
            elif len(changed_word) > 1:
                #print("Hello")
                for i in range(1,len(changed_word)):
                    word.text = changed_word[i]
                    changed_sent = make_sent(sent)
                    save_data = data_input + '\t'+ changed_sent +'\t'+right_tag+'\t'+tag+'\t'+right_tag[0:1]+'\t'+right_tag[1:3]+'\t'+right_tag[3:]+'\n'

               
                    f2.write(save_data)
               
            else:
                None#print("Hi")
               # change_verb(strm,word,sent,data_input,tag=tag,right_tag=morph[0][-1])
               # 
dict = {
            '3sgf':['1pl',"2pl","2plh","3ple","3plhe","3pln","3sgm","3sgn"],
            '1pl':["1sg","2sg","2sgh","2sgm","2sgf","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn',"2pl","2plh","3ple","3plhe","3pln"],
            "1sg":['1pl',"2pl","2plh","3ple","3plhe","3pln","2sg","2sgh","2sgm","2sgf","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn'],
            "2pl":["1sg","2sg","2sgh","2sgm","2sgf","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn','1pl','3ple','3plhe','3pln'],
            "2plh":["1sg","2sg","2sgh","2sgm","2sgf","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn','1pl','3ple','3plhe','3pln'],
            "2sg":['1pl',"2pl","2plh","3ple","3plhe","3pln","1sg","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn'],
            "2sgh":['1pl',"2pl","2plh","3ple","3plhe","3pln","1sg","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn'],
            "2sgm":['1pl',"2pl","2plh","3ple","3plhe","3pln","1sg","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn'],
            "2sgf":['1pl',"2pl","2plh","3ple","3plhe","3pln","1sg","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn'],
            "3ple":["1sg","2sg","2sgh","2sgm","2sgf","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn','1pl','2pl','2plh'],
            "3plhe":["1sg","2sg","2sgh","2sgm","2sgf","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn','1pl','2pl','2plh'],
            "3pln":["1sg","2sg","2sgh","2sgm","2sgf","3sge","3sgf","3sgh","3sghe","3sgm",'3sgn','1pl','2pl','2plh'],
            "3sge":['1pl',"2pl","2plh","3ple","3plhe","3pln","1sg","2sg","2sgh","2sgm","2sgf"],
            "3sgf":['1pl',"2pl","2plh","3ple","3plhe","3pln","1sg","2sg","2sgh","2sgm","2sgf"],
            "3sgh":['1pl',"2pl","2plh","3ple","3plhe","3pln","1sg","2sg","2sgh","2sgm","2sgf"],
            "3sghe":['1pl',"2pl","2plh","3ple","3plhe","3pln","1sg","2sg","2sgh","2sgm","2sgf"],
            "3sgm":['1pl',"2pl","2plh","3ple","3plhe","3pln","3sgf","3sgn","1sg","2sg","2sgh","2sgm","2sgf"],
            '3sgn':['1pl',"2pl","2plh","3ple","3plhe","3pln","3sgf","3sgm","1sg","2sg","2sgh","2sgm","2sgf"]     
    }
        
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
                            
                            if morphs[0][-1] in dict.keys():
                                lst = dict[ morphs[0][-1]]
                                for tag in lst:
                                    t = morphs[0]#strm.split("+")
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
                                        changed_sent = make_sent(sent)#sent.text #make_sent(sent)
                                        save_data = data_input + '\t'+ changed_sent +'\t'+right_tag+'\t'+tag+'\t'+right_tag[0:1]+'\t'+right_tag[1:3]+'\t'+right_tag[3:]+'\n'
                                        #f2 = open("train_newssfirst.tsv", "a",encoding='UTF-8')
                                        f2.write(save_data)
                                        #f2.close()
                                        #print(save_data)
                                    elif len(changed_word) > 1:
                                        #print("Hello")
                                        for i in range(1,len(changed_word)):
                                            word.text = changed_word[i]
                                            changed_sent = make_sent(sent)
                                            save_data = data_input + '\t'+ changed_sent +'\t'+right_tag+'\t'+tag+'\t'+right_tag[0:1]+'\t'+right_tag[1:3]+'\t'+right_tag[3:]+'\n'

                                
                                            f2.write(save_data)
                                
                                    else:
                                        None#print("Hi")
                                # change_verb(strm,word,sent,data_input,tag=tag,right_tag=morph[0][-1])
                        
                                                
                        elif len(morphs) > 1:
    
                            if morphs[0][-1] in dict.keys():
                                lst = dict[ morphs[0][-1]]
                                right_tag = morphs[0][-1]
                                for tag in lst:
                                    t = morphs[0]#strm.split("+")
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
                                        changed_sent = make_sent(sent)#sent.text #make_sent(sent)
                                        save_data = data_input + '\t'+ changed_sent +'\t'+right_tag+'\t'+tag+'\t'+right_tag[0:1]+'\t'+right_tag[1:3]+'\t'+right_tag[3:]+'\n'
                                        #f2 = open("train_newssfirst.tsv", "a",encoding='UTF-8')
                                        f2.write(save_data)
                                        #f2.close()
                                        #print(save_data)
                                    elif len(changed_word) > 1:
                                        #print("Hello")
                                        for i in range(1,len(changed_word)):
                                            word.text = changed_word[i]
                                            changed_sent = make_sent(sent)
                                            save_data = data_input + '\t'+ changed_sent +'\t'+right_tag+'\t'+tag+'\t'+right_tag[0:1]+'\t'+right_tag[1:3]+'\t'+right_tag[3:]+'\n'

                                
                                            f2.write(save_data)
                                
                                    else:
                                        None#print("Hi")
                                # change_verb(strm,word,sent,data_input,tag=tag,right_tag=morph[0][-1])
                        
                       
                        
                       
                        else:
                            None #print("inside_fineding not have morphemes")
                    else:
                        if guess_morphemes(word.text):
                            
                            #print("inside guessing")
                            morphs = guess_morphemes(word.text) 
                           
                            if len(morphs) == 1 and len(morphs[0])>0:
                                #print("in")
                                
    
                                if morphs[0][-1] in dict.keys():
                                    lst = dict[ morphs[0][-1]]
                                    for tag in lst:
                                        t = morphs[0]#strm.split("+")
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
                                            changed_sent = make_sent(sent)#sent.text #make_sent(sent)
                                            save_data = data_input + '\t'+ changed_sent +'\t'+right_tag+'\t'+tag+'\t'+right_tag[0:1]+'\t'+right_tag[1:3]+'\t'+right_tag[3:]+'\n'
                                        #f2 = open("train_newssfirst.tsv", "a",encoding='UTF-8')
                                            f2.write(save_data)
                                        #f2.close()
                                        #print(save_data)
                                        elif len(changed_word) > 1:
                                        #print("Hello")
                                            for i in range(1,len(changed_word)):
                                               word.text = changed_word[i]
                                               changed_sent = make_sent(sent)
                                               save_data = data_input + '\t'+ changed_sent +'\t'+right_tag+'\t'+tag+'\t'+right_tag[0:1]+'\t'+right_tag[1:3]+'\t'+right_tag[3:]+'\n'

                                
                                               f2.write(save_data)
                                
                                        else:
                                            None#print("Hi")
                                # change_verb(strm,word,sent,data_input,tag=tag,right_tag=morph[0][-1])
                        
                         
                            elif len(morphs) > 1:
                                
                                
                                if morphs[0][-1] in dict.keys():
                                    lst = dict[ morphs[0][-1]]
                                    for tag in lst:
                                        t = morphs[0]#strm.split("+")
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
                                            changed_sent = make_sent(sent)#sent.text #make_sent(sent)
                                            save_data = data_input + '\t'+ changed_sent +'\t'+right_tag+'\t'+tag+'\t'+right_tag[0:1]+'\t'+right_tag[1:3]+'\t'+right_tag[3:]+'\n'
                                        #f2 = open("train_newssfirst.tsv", "a",encoding='UTF-8')
                                            f2.write(save_data)
                                        #f2.close()
                                        #print(save_data)
                                        elif len(changed_word) > 1:
                                        #print("Hello")
                                            for i in range(1,len(changed_word)):
                                               word.text = changed_word[i]
                                               changed_sent = make_sent(sent)
                                               save_data = data_input + '\t'+ changed_sent +'\t'+right_tag+'\t'+tag+'\t'+right_tag[0:1]+'\t'+right_tag[1:3]+'\t'+right_tag[3:]+'\n'

                                
                                               f2.write(save_data)
                                
                                        else:
                                            None#print("Hi")
                                # change_verb(strm,word,sent,data_input,tag=tag,right_tag=morph[0][-1])


                        else:
                            None#print("inside guessing not have morphemes")


from os import listdir
from os.path import isfile, join

#mypath = "./data/"
#onlyfiles = []
#for f in listdir(mypath):
#    if isfile(join(mypath,f)):
#        onlyfiles.append(f)
#print(depTag(sentence,depModel))
#files = #['train_final.tsv']#,'valid_2.tsv']#['test.tsv','test_1.tsv','test_2.tsv','test_3.tsv','test_4.tsv','test_5.tsv','test_6.tsv','test_7.tsv','test_8.tsv','hiru news.txt']# 'train_new_20.tsv','train_new_71.tsv','train_new_30.tsv','train_new_63.tsv', 'train_new_1.tsv','train_new_2.tsv', 'train_new_87.tsv', 'train_new_3.tsv', 'train_new_43.tsv', 
onlyfiles = [ 'train_new_79.tsv', 'train_new_66.tsv', 'train_new_32.tsv', 'train_new_15.tsv', 'train_new_25.tsv', 'train_new_44.tsv', 'train_new_34.tsv', 'train_new_28.tsv', 'train_new_8.tsv', 'train_new_46.tsv', 'train_new_27.tsv', 'train_new_69.tsv', 'train_new_38.tsv', 'train_new_86.tsv', 'train_new_76.tsv', 'train_new_26.tsv', 'train_new_83.tsv', 'train_new_61.tsv', 'train_new_55.tsv', 'train_new_0.tsv', 'train_new_81.tsv', 'train_new_82.tsv', 'train_new_77.tsv', 'train_new_65.tsv', 'train_new_62.tsv', 'train_new_52.tsv', 'train_new_48.tsv', 'train_new_18.tsv', 'train_new_7.tsv', 'train_new_75.tsv', 'train_new_19.tsv', 'train_new_35.tsv', 'train_new_31.tsv', 'train_new_21.tsv', 'train_new_68.tsv', 'train_new_12.tsv', 'train_new_9.tsv', 'train_new_42.tsv', 'train_new_29.tsv', 'train_new_11.tsv', 'train_new_17.tsv', 'train_new_60.tsv', 'train_new_67.tsv', 'train_new_37.tsv', 'train_new_70.tsv', 'train_new_23.tsv', 'train_new_6.tsv', 'train_new_78.tsv', 'train_new_16.tsv', 'train_new_33.tsv', 'train_new_59.tsv', 'train_new_88.tsv', 'train_new_56.tsv', 'train_new_74.tsv', 'train_new_13.tsv', 'train_new_54.tsv', 'train_new_49.tsv', 'train_new_22.tsv', 'train_new_80.tsv', 'train_new_39.tsv', 'train_new_50.tsv', 'train_new_5.tsv', 'train_new_24.tsv', 'train_new_14.tsv', 'train_new_64.tsv', 'train_new_73.tsv', 'train_new_41.tsv', 'train_new_45.tsv', 'train_new_51.tsv', 'train_new_58.tsv', 'train_new_36.tsv', 'train_new_84.tsv', 'train_new_47.tsv', 'train_new_4.tsv', 'train_new_53.tsv', 'train_new_85.tsv', 'train_new_72.tsv', 'train_new_10.tsv', 'train_new_40.tsv', 'train_new_57.tsv']
for file in onlyfiles:
        f1=open("./data/"+file,"r",encoding='UTF-8')
        f2 = open("./train/"+"train_"+file.split(".")[0]+".tsv", "a",encoding='UTF-8')
        print("Starting with file: "+file)
        sentence_count =0

        for line in f1:
            sentence_count+=1
            sentence = line.strip('"')

            depTag(sentence.strip(),depModel)
           
            if sentence_count%100==0:
                time.sleep(5)
                print(sentence_count)
        print("Ending file: "+file)
    

















