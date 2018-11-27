#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @author =__Uluç Furkan Vardar__

import yaml
import json
from collections import OrderedDict
import re

    
'''Simple usage

from file_commander import my_file_commander

commander = my_file_commander()

### TO READ
article_path ='/Users/uluc/Desktop/Bitirme/Wikiparse_WorkSpace/<2018.10.-->Wiki/<2018-10-25>Outputs-DataFieldClean/Clean_Interested_Articles_V2.txt'
splitter_patter = '\n\n\n'
dataContains_tuples = ['valid_bit',id','title','infoBox_type','clean_infoBox','bulk_paragraph']
articles = commander.my_tub_file_reader(article_path,splitter_patter,dataContains_tuples)

---
for a in articles[:1]:
    print a.get_string_for_print()
---

## ADD ANY NEW TUBLE TO DATA IN MAIN 
articles[0].article['denemeee'] = 'olduuu'

### TO SAVE
dataContains_tuples = ['id','title','infoBox_type','clean_infoBox','bulk_paragraph','denemeee']
commander.my_tub_file_recorder('./tesssst.txt',articles,'\n\n\n',dataContains_tuples)

'''
class my_file_commander():
    def __init__(self):
        self.max_tuple = ['id','title','infoBox_type','text_infoBox','bulk_infoBox','clean_infoBox','bulk_paragraph','clean_paragraph']
        self.saved_successfully = 0
        self.read_successfully = 0

    def my_tub_file_reader(self,input_articles_path,splitter_patter,dataContains_tuples):
        article_text = open(input_articles_path, "r") .read()
        articles = []
        for a in article_text.split(splitter_patter):
            article = Article(a,dataContains_tuples)
            if article.kill == False:
                articles.append(article)
        print '#Articles read successfully ->',len(articles)
        self.read_successfully = len(articles)
        return articles

    def my_tub_file_recorder(self,output_articles_path,articles,splitter_patter,dataContains_tuples):
        f = open(output_articles_path,'w')
        i= 0
        for a in articles[:1]:
            i+=1
            f.write(a.get_string(dataContains_tuples)+splitter_patter)
        print '#Articles saved successfully ->',i
        self.read_successfully = i
        f.close()


class Article():
    def __init__(self,text,dataContains_tuples):
        try:
            bulk = text.split('#')
            if len(bulk) != len(dataContains_tuples) :
                self.kill = True
            else:
                self.kill = False
                article = OrderedDict()
                i = 0
                for tuple_key in dataContains_tuples:
                    if tuple_key == 'bulk_infoBox' or tuple_key == 'clean_infoBox' or tuple_key == 'clean_paragraph':
                        article[tuple_key] = json.loads(bulk[i])
                    elif tuple_key == 'text_infoBox':
                        article['bulk_infoBox'] = self.convert_2_json(bulk[i])
                    else:
                        article[tuple_key] = bulk[i]
                    i+=1
                self.article = article
        except Exception as e:
            if str(e) == "'NoneType' object has no attribute 'group'":
                pass
            else:
                print e
    def get_string(self,dataContains_tuples):
        s = ''
        for tuple_key in dataContains_tuples:
            if tuple_key == 'bulk_infoBox' or tuple_key == 'clean_infoBox' or tuple_key == 'clean_paragraph':
                s += json.dumps(self.article[tuple_key], ensure_ascii=False, encoding='utf8').encode('utf-8')+'#'
            else:
                s += self.article[tuple_key]+'#'
        return s[:-1]

    def convert_2_json(self,text):

        lines = text.replace('<nl>','\n').split('\n')
        temp = {}
        for i in range(1,len(lines)):
            temp_key = ""
            temp_value = ""
            lines[i] = lines[i].strip()
            if lines[i].count('=') == 1:
                if '|' in lines[i]:
                    m = re.search(".*\|(.*)=(.*)",lines[i])
                    #print lines[i]
                    temp_key = (m.group(1)).replace('|','').strip()
                    temp_value = m.group(2).strip()
                    temp[temp_key] = temp_value
                else:
                    #print lines[i],"-----"
                    #print 'HATA!! PİPE YOK..'
                    continue
            else:
                if '}}' == lines[i]:
                    continue
                #print lines[i],"-----"
                #print 'HATA! BİRDEN FAZLA EŞİTTİR/Yok......\n\n\n\n'
                continue  
        return temp


    def get_string_for_print(self):
        return json.dumps(self.article, ensure_ascii=False, encoding='utf8',indent = 4)
    def get_infoBox(self):
        return self.article['clean_infoBox']
    def get_infoBoxType(self):
        return self.article['infoBox_type']        


    
