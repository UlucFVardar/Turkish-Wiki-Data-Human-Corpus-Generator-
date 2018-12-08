# -*- coding: UTF-8 -*-
# encoding=utf8  
# @author: İlkay Devran

'''
export CLASSPATH=zemberek-full.jar:$CLASSPATH
javac -cp zemberek-full.jar SentenceSplitter.java
'''

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
import re
import os

    
def process_bulk_paragraph( data):
    '''
        data: line.split("#")[4] form bulkd data file
    '''
    # open '\n'
    paragraph = data.replace("<nl>", "\n")

    # delete '[[Dosya.*]]'
    paragraph = clean_dosya(paragraph)

    # delete <.*?>.*?</.*?> TAGS
    paragraph = clean_tags_regex(paragraph)


    """ --- --- --- --- --- --- --- --- --- --- """

    # After now sentence is obtained to work on it directly 

    # Uluc has added this clean method
    # Need the check this part 
    # [[ ... | ... ]]
    sentence = clean_pipes_in_double_square_brackets(paragraph) 

    # delete {{...}} double curly brackets
    sentence = clean_double_curly_brackets(sentence)

    # delete (...) except with ( d. ... - o. ...) 
    # It keeps birth day and death info 
    """ISSUE here! Some dates in brackets are represented not with d. or o."""
    sentence = clean_round_brackets_except_with_birth_and_death(sentence)
    #print sentence
    """
    # delete [[...]] 
    # except that includes numbers like birth date or death 
    # ( i.e. [[5 Mayis]] [[1818]] )
    #sentence = clean_double_square_brackets(sentence)
    """

    # remove ==...== double equations from the sentence
    sentence =  clean_double_equation_mark(sentence)

    # delete unnecessary infos in before bday in brackets (..... d. 1982) 
    sentence = clean_unnecessary_info_before_bday_in_round_brackets(sentence)
    
    # remove ' """ ' and  " ''' " in sentence
    sentence = clean_triple_quoates(sentence)

    # get rid of extra paragraphs
    sentence = clean_extra_paragraphs(sentence)

    # to be continued ...

    #-------------------------Cleaning finished------------------------------------

    if sentence == '':
        return 'None-(Error: Sentence is NULL.)'
    elif '{' in sentence or '}' in sentence or '|' in sentence:
        return 'None-(Error: Bracket faulty[]\{\}| )'
    else:
        return sentence

def generate_and_save_articles_with_santences(inputfile,output_file):
    # Run Java Program   
    # output.txt-->[input]--(SentenceSplitter.java)--[output]--> zemberek_output.txt
    tmpFile = "./temp_zemberek.txt"
    cmd = "java SentenceSplitter "+ tmpFile + " " + inputfile 
    os.system(cmd)

    fixZemberekOutput(output_file, tmpFile)
    os.system('rm ./temp_zemberek.txt')    

def clean_dosya( data):
    try:
        return re.sub(r"\[\[Dosya.*\]\]","",data)
    except:
        return data

def clean_pipes_in_double_square_brackets( data):
    try:
        return re.sub(r"\[\[[^\[\{]*\|","",data).replace('[','').replace(']','') # \[\[.*?\|
    except:
        return data.replace(']','').replace('[','')
    
def clean_double_equation_mark( data): #==
    try:
        return re.sub(r"==.*?==","", data)
    except:
        return data

def clean_tags_regex(data):
    try:
        data = re.sub(r"((<br />.*?<br />|<br />)|(<br>.*?<br>|<br>))","",data)
    except:
        pass
    try:
        return re.sub(r"<.*?\/>|<.*?</.*?>","",data)#re.sub(r"^.*?<[/].*?>|<.*?(.|\s)*?</.*?>|<.*?(.|\s)*","",data)
    except:
        return data

def clean_double_curly_brackets(data):
    try:
        return re.sub(r"\(({{.*?(.|\s).*?}})\)|({{.*?(.|\s).*?}})","",data)
    except:
        return data

def clean_round_brackets_except_with_birth_and_death( data):
    try:
        if 'okunusu:' in data:
            data = re.sub(r"\(okunusu:\s.* +sayfalar:.*\)","", data)
        if 'd.' in data:
            try:
                return data.replace(';','')
            except:
                pass
        return data #re.sub(r"\(.*[^\)]*;\s\)|\(.*; ","",data)
    except:
        return data
    """
    # Cancelled for now
    try:
        data = re.sub(r"\([^d]\.*.?(.|\s).*?[^o]\.*.?(.|\s).*?\)","",data)
        return re.sub(r"(;.*?\)(.|\s)*?;.*?\)|;.*?\))","",data)
    except:
        return data
    """

# Cancelled for now
def clean_double_square_brackets( data):
    # Cancelled for now
    try:
        return re.sub(r"\(.*\)","",data).replace(']]','') # \(.*\) # \(.*?\[\[[\D].*?\]\].*?\)
    except:
        return data

def clean_unnecessary_info_before_bday_in_round_brackets( data):
    # i.e.
    # Gulse Birsel (evlilik oncesi soyadi sener d. 11 Mart 1971), Turk oyuncu, senarist ve gazeteci.
    # Gulse Birsel ( d. 11 Mart 1971), Turk oyuncu, senarist ve gazeteci.
    try:
        matches = re.findall(r"\((.*)d\.",data)
        if matches[0] != ' ' and matches != '\t':
            return data.replace(matches[0],"")
        else:
            return data
    except:
        return data

def clean_triple_quoates( data):
    try:
        return data.replace("'''",'').replace("''",'').replace('"','')
    except:
        return data

def clean_extra_paragraphs( data):
    try:
        return data.strip().split('\n')[0]
    except:
        return data

# NOT USED YET
def split_sentences( data):
    try:
        sentences_list = re.findall(r"[^\.]*[\.]", data)
        return sentences_list
    except:
        return [data]


# ----------------------- Helper Flow function -----------------------

def set_environment():
    os.system("mkdir outputs")
    os.system("export CLASSPATH=zemberek-full.jar:$CLASSPATH")
    os.system("javac -cp zemberek-full.jar SentenceSplitter.java")
    #os.system("./setEnv.sh")

def clear_environment():
    os.system("rm -r outputs")

def flow(sentence):
    # Here is the cleaned sentence. Ready to write into output text file
    with open("outputs/output.txt","w") as o_f:
        o_f.write(sentence.strip() + '\n\n')
    o_f.close()

    # Run Java Program   
    # output.txt-->[input]--(SentenceSplitter.java)--[output]--> zemberek_output.txt
    cmd = "java SentenceSplitter outputs/zemberek_output.txt outputs/output.txt"
    os.system(cmd)

    # Fix output anomalies
    # zemberek_output.txt-->[input]--(dataCleaner.py)--[output]--> (first_sentence, second_sentence), Ack. Message
    f_sent, s_sent = fixZemberekOutput("outputs/zemberek_output.txt")

    # remove text files
    os.system("rm outputs/output.txt outputs/zemberek_output.txt")

    return sentence.strip(), (f_sent.encode("utf-8"), s_sent.encode("utf-8")), '[dataCleaner, line 190] Everything is OK.'


# ----------------------- Sentence Combiner part -----------------------

def fixZemberekOutput(finalOutput, zemberek_output_path):
    """
        @zemberek_output_path: output path of SentenceSplitter.java
    """
    with open(zemberek_output_path, "r") as f:
        with open(finalOutput, "w") as wf:
            
            for line in f:
                if line.strip() == '' :
                    continue
                line_parts = (line.strip().split('#')[7]).split('@')
                first_sentence = line_parts[0]
                second_sentence = 'None'
                sentences = {}
                d_flag = False
                o_flag = False
                lngth = len(line_parts)
                for j, part in enumerate(line_parts):
                    try:
                        if part.endswith('ö.') and o_flag == False:
                            first_sentence += line_parts[j+1]
                            o_flag = True
                        
                        if d_flag == True:
                            if o_flag == True:
                                try:
                                    second_sentence = line_parts[3]
                                except:
                                    second_sentence = 'None'
                            else:
                                try:
                                    second_sentence = line_parts[2]
                                except:
                                    second_sentence = 'None'
                        
                        if part.endswith('(d.') and d_flag == False:
                            first_sentence = line_parts[j] + " " + line_parts[j+1]
                            d_flag = True
                    except:
                        if '(d.' not in part:
                            first_sentence = line_parts[1]
                        else:
                            first_sentence = 'None-Faulty'
                wf.write('#'.join((line.strip().split('#')[:7])) + "#" + first_sentence + "@" + second_sentence +"\n\n\n")
                #print '\n1. ', first_sentence, '\n2. ',second_sentence, '\n'

            
            wf.close()       
    f.close()
    