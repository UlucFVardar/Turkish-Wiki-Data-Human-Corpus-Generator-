#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @author =__Uluç Furkan Vardar__


'''Simple usage

'
from file_commander import my_file_commander
commander = my_file_commander()

### TO READ
article_path ='/Users/uluc/Desktop/Bitirme/Wikiparse_WorkSpace/<2018.10.-->Wiki/<2018-10-21>Outputs-ArticleClean/Clean_Interested_Articles.txt'
splitter_patter = '\n\n\n'
dataContains_tuples = ['id','title','infoBox_type','clean_infoBox','bulk_infoBox','bulk_paragraph']
articles = commander.my_tub_file_reader(article_path,splitter_patter,dataContains_tuples)

'

from sapsik_bir_nlp_kit import sapsik_bir_nlp_kit
kit = sapsik_bir_nlp_kit()


for i in range(20,50):
    print json.dumps(articles[i].article['bulk_infoBox'],indent = 4 ,ensure_ascii=False, encoding='utf8')
    a = kit.clean_jsonvalues(articles[i].article['bulk_infoBox']) ## this line cleans the json
    print json.dumps(a,indent = 4 ,ensure_ascii=False, encoding='utf8')


'''

import re
import json

class sapsik_bir_nlp_kit():
    def __init__(self):
        self.month = [  'Ocak'.decode('utf-8'),
                        'Şubat'.decode('utf-8'),
                        'Mart'.decode('utf-8'),
                        'Nisan'.decode('utf-8'),
                        'Mayıs'.decode('utf-8'),
                        'Haziran'.decode('utf-8'),
                        'Temmuz'.decode('utf-8'),
                        'Ağustos'.decode('utf-8'),
                        'Eylül'.decode('utf-8'),
                        'Ekim'.decode('utf-8'),
                        'Kasım'.decode('utf-8'),
                        'Aralık'.decode('utf-8')]
        self.key_banned = ['imza'.decode('utf-8'),
                          'resim'.decode('utf-8'),
                          'resimboyutu'.decode('utf-8'),
                          'websitesi'.decode('utf-8'),
                          'image'.decode('utf-8'),
                          'resimadı'.decode('utf-8'),
                          'genişlet'.decode('utf-8')]

        self.key_name_map =['adı'.decode('utf-8'),
                      'isim'.decode('utf-8'),
                      'ismi'.decode('utf-8'),
                      'adi'.decode('utf-8'),
                      'name'.decode('utf-8'),
                      'karakteradı'.decode('utf-8')]
        self.key_birth_map = ['dogumtarihi'.decode('utf-8')]

        self.maps = {}
        self.maps['ad'] = self.key_name_map
        self.maps['doğumtarihi'.decode('utf-8')] = self.key_birth_map


    # for clean infoBox
    def clean_jsonvalues(self,infobox):
        newjson = {}
        for key in infobox.keys():
            new_key = key.replace(' ','').replace('_','').lower()

            if new_key in self.key_banned or infobox[key] == "" or "<!--" in infobox[key] or 'yalın liste|'.decode('utf-8') in infobox[key]:
                continue

            new_key = self.key_map(new_key)

            temp_value = infobox[key].replace("'",'').replace('\"','')
            if new_key != 'ad':
                temp_value = self.clean_pipes(temp_value)
            else:
                temp_value = self.remove_brackets_with_text(temp_value)

            temp_value = self.clean_tags(temp_value)

            temp_value = self.remove_brackets(temp_value)

            if new_key == 'doğumtarihi'.decode('utf-8') \
                or new_key =='ölümtarihi'.decode('utf-8') \
                or new_key == 'dogumtarihi'.decode('utf-8') :
                temp_value = self.date_map(temp_value)
            
            newjson[new_key] = temp_value        
        return newjson
    

    # . [[asdasda]], deneme ---> , deneme
    def remove_brackets_with_text(self,data):
        pattern= r'({{([^}}]*)}}|\[\[([^\]\]]*)\]\])'
        try:
            data = re.sub(pattern,"",data)
            return data.strip()
        except Exception as e:
            return data


    # . [[Cenova]]{{,}} [[İtalya]] --> Cenova, İtalya
    def remove_brackets(self,data):
        pattern= r'{{|}}|\[\[|\]\]'
        try:
            return re.sub(pattern,"",data)#re.sub(r"^.*?<[/].*?>|<.*?(.|\s)*?</.*?>|<.*?(.|\s)*","",data)
        except:
            return data


    # . ['adı','isim','ismi','adi','name','karakteradı'] --> 'ad'
    def key_map(self,data):
        if data == 'mesleği'.decode('utf-8'):
            return 'meslek'.decode('utf-8')
        if data in self.key_name_map:
            return 'ad'.decode('utf-8')
        if data in self.key_birth_map:
            return 'doğumtarihi'.decode('utf-8')
        return data
    
    # . [[Film yapımcısı|Yapımcı]] , {{Film yönetmeni|Yönetmen}} --->Yapımcı, Yönetmen
    def clean_pipes(self,data):
        pattern  = '(\[\[[^\]\]]*\|([^\]\]]*)\]\])|({{[^}}]*\|([^}}]*)}})' 
        p = re.compile(pattern, re.MULTILINE)
        try:
            if p:
                clean = p.sub(r'\2', data)
                return clean
        except Exception as e:
            return data

    # . <br> --> ,
    def clean_tags(self,data):
        try:
            data = re.sub(r"((<br />.*?<br />|<br />)|(<br>.*?<br>|<br>))",", ",data)
        except:
            pass
        try:
            return re.sub(r"<.*?\/>|<.*?</.*?>",", ",data)#re.sub(r"^.*?<[/].*?>|<.*?(.|\s)*?</.*?>|<.*?(.|\s)*","",data)
        except:
            return data
        
    # . {{Doğum tarihi|1818|5|5}} ---> 5 Mayıs 1818
    # . {{ölüm tarihi ve yaşı|1883|03|14|1818|05|05}} ---> 14 Mart 1883
    # . 1162 ---> 1162   
    # . 123 ---> 123       
    # . 2188 2 2 --->  2 Şubat 2188
    # . 2188.2.2 --->  2 Şubat 2188
    def date_map(self, date_value ):
        orj = date_value
        converted_date = date_value
        try : 
            value = re.findall(r"(\|\d+|\d+)", date_value, re.MULTILINE) ## finding numbersafter pipes
            value = [int(w.replace('|', '')) for w in value]  # clean pipes |
            if len(value) == 3:
                converted_date = str(value[2])+' '+ str(self.month[value[1]-1]) + ' ' + str(value[0])
                return converted_date
            elif len(value) == 6:
                year1 = int(value[0])
                year2 = int(value[0+3])
                if year1 >year2:
                    converted_date = str(value[2])+' '+ str(self.month[value[1]-1]) + ' ' + str(value[0])
                    return converted_date
                    
                else:
                    converted_date = str(value[2+3])+' '+ str(self.month[value[1+3]-1]) + ' ' + str(value[0+3])
                    return converted_date
            elif len(value) == 1:
                if len(str(value[0])) == 4 or len(value[0]) ==3:
                    converted_date = str(value[0])
                    return converted_date
        except Exception as e:
            #print e
            pass
        try:
            '''
            value = orj                
            if value.count('-') >0:
                value = value[:value.find('-')]
                if 'M.' in value[:2] or 'MS' == value[:2] or 'MÖ' == value[:2]:
                    converted_date = str(value.encode('utf-8'))
                    return converted_date
            '''
            value = orj.replace(',',' ').replace('  ',' ').replace('.',' ')
            if len(value.split(' ')) == 3:
                if value.split(' ')[1].decode('utf-8') in self.month:
                    converted_date =  str(value)
                if value.split(' ')[1].isdigit():
                    value = value.split(' ')
                    converted_date = str(value[2])+' '+ str(self.month[value[1]-1]) + ' ' + str(value[0])
            return converted_date            
        except Exception as e:
            #print e
            pass
        return None
        #----------------------------------------------

            
            
#------
