#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @author =__Uluç Furkan Vardar__

# -*- coding: utf-8 -*-

'''
from sapsik_bir_Analyser import Article_Analyser


aaa = Article_Analyser(articles)
print aaa.get_all_uniq_infoBoxTypes_for_save()

number_of_infobox_type_rep4 = aaa.draw_Repetition_of_all_InfoBoxTypes(output_path = log.get_output_path() ,
                  title = 'Wiki Dump Data InfoBox Types and Repetitions (>100)',
                  min_repetition = 100 )

# after clean json's                  

'''

from collections import Counter
import yaml
import matplotlib.pyplot as plt
import pandas as pd
import json
import os 
class Article_Analyser():
    def __init__(self,articles):
        self.articles = articles
        self.calculate_all_uniq_infoBoxTypes()
        
    def calculate_all_uniq_infoBoxTypes(self):
        c = Counter()
        for article in self.articles:
            infoBox_type = article.article['infoBox_type'].decode('utf-8')
            try:
                c[infoBox_type] +=1
            except Exception as e:
                c[infoBox_type] = 1
        self.all_infoBoxType_counter = c

    def get_all_uniq_infoBoxTypes_for_save(self):
        temp = []
        for type_ in self.all_infoBoxType_counter.items():
            s = ('%-21s -> %d' % (type_[0],type_[1]))
            temp.append(s)
        return '\n'.join(temp)

    # --- Data Field Analysis ----------
    def count_data_fields(self):
        counter_of_fields = {}

        for a in self.articles:
            type_ = a.article['infoBox_type'].decode('utf-8')
            try:
                counter_of_fields[type_]['count'] += Counter(a.article['clean_infoBox'].keys())
                counter_of_fields[type_]['number'] += 1 
            except Exception as e:
                counter_of_fields[type_] = {}
                counter_of_fields[type_]['count'] = Counter(a.article['clean_infoBox'].keys())
                counter_of_fields[type_]['number'] = 1     
        self.counter_of_fields = counter_of_fields

    def save_allCounts_2_file(self,output_path):
        allCounters = Counter()
        number = 0
        for i in self.counter_of_fields.keys():
            allCounters += self.counter_of_fields[i]['count']
            number += self.counter_of_fields[i]['number']

        f = open(output_path+'all_count.txt',"w")
        aa = '#Info Box Types : {}, #Total article with infoBox: {}\n\n'.format(len(self.counter_of_fields.keys()),number)
        a = json.dumps( allCounters.most_common() , ensure_ascii=False, encoding='utf8',indent = 4).encode('utf-8')
        self.allCounters = allCounters
        print aa+a
        f.write(aa)
        f.write(a)
        f.close()

    def save_Counts_for_types(self,output_path):
        # her bir cat için bastırma counter
        if not os.path.isdir(output_path+'Counters/'):
            os.makedirs(output_path+'Counters/')
        for i in self.counter_of_fields.keys():
            name = str(i.encode('utf-8'))
            f = open(output_path+'Counters/'+name+'.txt',"w")
            aa = 'Info Box Type : {}, #Total article with this infoBox: {}\n\n'.format(name,self.counter_of_fields[i]['number'])
            a = json.dumps(self.counter_of_fields[i]['count'].most_common(), ensure_ascii=False, encoding='utf8',indent = 4).encode('utf-8')
            f.write(aa)
            f.write(a)
            f.close()

    def save_uniq_fields(self,output_path):
        path = output_path+'Uniq/'
        if not os.path.isdir(path):
            os.makedirs(path)    
        for who in range (0,len(self.counter_of_fields.keys())):
            st = 'Uniq Data Fields for {} -------\n'.format(self.counter_of_fields.keys()[who].encode('utf-8'))
            one_type = self.counter_of_fields[self.counter_of_fields.keys()[who]]['count']
            other_types = {}
            other_types =  [ self.counter_of_fields[k]['count']  for k in self.counter_of_fields.keys() if k != self.counter_of_fields.keys()[who]]
            result = []
            for element in one_type.keys():
                Flag = False
                for cs in other_types:
                    if cs[element] != 0:
                        Flag=True
                if Flag == False:
                    result.append(element)
            #strr = ' \n'.join(result)
            f= open(path+self.counter_of_fields.keys()[who]+'_Uniq_Fields.txt',"w")
            f.write(st)
            f.write(json.dumps(result, ensure_ascii=False, encoding='utf8',indent = 4).encode('utf-8'))

    def save_dataField_Analysis(self,output_path):

        # çıktı göresterme
        f= open(output_path+'Counts2.txt',"w")
        f.close()
        for i in self.counter_of_fields.keys():
            f= open(output_path+'Counts2.txt',"ab")
            a = []
            for j in self.counter_of_fields[i]['count'].most_common(10):
                y = self.counter_of_fields[i]['number']
                b = json.dumps(j, ensure_ascii=False, encoding='utf8').\
                            replace(']','').replace('[','')\
                            .replace('"','').replace(',',':').strip()
                bb = int(b.split(':')[1].strip())
                a.append( ('%26s|')%( b ))
            u = unicode(i, "utf-8")
            ab = u.rjust(22,' ')+str(self.counter_of_fields[i]['number']).rjust(6,' ')+' ->'
            ab = ab.encode('utf8')
            for bb in a:
                ab += bb.encode('utf-8')
            f.write(ab)
            f.write('\n') 
        
        # çıktı göresterme
        f.write('\n')
        for i in self.counter_of_fields.keys():
            a = []
            for j in self.counter_of_fields[i]['count'].most_common(10):
                y = self.counter_of_fields[i]['number']
                b = json.dumps(j, ensure_ascii=False, encoding='utf8').\
                            replace(']','').replace('[','')\
                            .replace('"','').replace(',',':').strip()
                bb = int(b.split(':')[1].strip())
                a.append( ('%20s: %.2f|')%( b.split(':')[0].strip(),bb/float(y) ))
            u = unicode(i, "utf-8")
            ab = u.rjust(22,' ')+str(self.counter_of_fields[i]['number']).rjust(6,' ')+' ->'
            ab = ab.encode('utf8')
            for bb in a:
                ab += bb.encode('utf-8')
            f.write(ab)
            f.write('\n')

        # çıktı göresterme
        f.write('\n')
        for i in self.counter_of_fields.keys():
            a = []
            for j in self.counter_of_fields[i]['count'].most_common(10):
                y = self.counter_of_fields[i]['number']
                b = json.dumps(j, ensure_ascii=False, encoding='utf8').\
                            replace(']','').replace('[','')\
                            .replace('"','').replace(',',':').strip()
                bb = int(b.split(':')[1].strip())
                if bb/float(y)>=0.60:
                    a.append( ('%20s: %.2f|')%( b.split(':')[0].strip(),bb/float(y) ))
                else:
                    a.append( ('%26s|')%( '' ))
            u = str(i.encode('utf-8'))
            ab = '%36s -> %6s\n' % (i,str(self.counter_of_fields[i]['number']))
            ab = ab.encode('utf8')
            for bb in a:
                ab += bb.encode('utf-8')
            f.write(ab)
            f.write('\n') 
        f.write('\n\nGenel durum\n')    
        total = ('%25s|')%(json.dumps(self.allCounters.most_common(20), ensure_ascii=False, encoding='utf8').\
                            replace(']','').replace('[','')\
                            .replace('"','').replace(',',':').strip() )
        f.write(total.encode('utf-8'))
        f.close()


    





    # --------------------------------


    # ---- Drawing -------- --------- 
    def draw(self,x,y,title,saving_path):
        plt.title(title)
        plt.plot(x, y)
        plt.xticks(x, x, rotation='vertical')
        fig =plt.gcf()
        fig.set_size_inches(20, 11)
        #plt.savefig(saving_path)
        plt.savefig(saving_path,format='eps', dpi=1000)
        plt.show()
        
    def print_info(self,x,y):
        pd.set_option('display.height', 1000)
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        df_more_than_1 = pd.DataFrame({'Info Box Type':x , 'Repetitions':y})
        print df_more_than_1.count()
        print df_more_than_1

    def draw_Repetition_of_all_InfoBoxTypes(self,output_path,title,min_repetition):
        x = []
        y = []
        for type_ in self.all_infoBoxType_counter.items():
            if type_[1] < min_repetition:
                continue
            x.append(type_[0])
            y.append(type_[1])
        self.draw(x = x, 
                  y = y, 
                  title = title, 
                  saving_path = output_path+title)

        self.print_info(x = x,
                        y = y)
        return len(x)
    
            
            
    # --------------------------------