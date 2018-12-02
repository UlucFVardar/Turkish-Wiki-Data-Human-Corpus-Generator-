#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import json
import os

global DA_id
DA_id = 0

global tried
tried = 0

def save_DAs(file_path,possible_boxes):

    counter =0 
    mypath = file_path
    if not os.path.isdir(mypath):
        os.makedirs(mypath)
    for i in possible_boxes.keys():
        file = open(mypath+"/DA_"+i+".txt","w")
        k=1
        for j in possible_boxes[i].keys():
            file.write(possible_boxes[i][j].replace('##',str(k))) 
            counter+=1
            k+=1
        file.close()
    global DA_id
    global tried
    print '#Tried to convert to DA from infoBox',tried     
    print '#Converted to DA from infoBox',counter     
    print '#DA saved succesfully',DA_id

    return tried,counter,DA_id
def get_rules(file_path):
    global DA_id
    DA_id = 0

    global tried
    tried = 0    
    file = open(file_path, "r") 
    selected =  file.read() 
    lines = selected.split('\n')
    rules = {}
    for line in lines : 
        if  len(line.split(' ')) == 6:
            print line
        boxType,number_static,static,number_dinamik,dinamik = line.split(' ')
        boxType = boxType.replace('_',' ')
        rules[boxType] = {}
        rules[boxType]['static'] = static.split(',')
        rules[boxType]['dynamic'] = dinamik.split(',')
    return rules

def create_DA_combinations(rules,articles):
    global tried
    combinations = {}
    for i in rules.keys():
        combinations[i] = {}
    for i,a in enumerate(articles):
        a = a.article
        try:
            articles[i].article['DA_as_str'] = 'None'
            articles[i].article['DA_fields'] =  'None'
            statics = rules[a['infoBox_type']]['static']
            tried +=1
            flag = contains_all(a['clean_infoBox'].keys(),statics)
            if flag == False:
                continue
            combination_ = combination_of_article(a,statics,rules[a['infoBox_type']]['dynamic'])
            combinations[a['infoBox_type']][a['title'].decode('utf-8')] = combination_.poss_all_str
            articles[i].article['DA_as_str'] = combination_.poss_all_str.replace('##','IN_CAT_NUMBER')
            articles[i].article['DA_fields'] =  combination_.poss_all
        except Exception as e:
            print e,'BURDAAA'
            pass
    return articles,combinations
def contains_all(keys,statics):
    for i in range(0,len(keys)):
        keys[i] = str(keys[i].encode('utf-8'))
    for needed in statics:
        if needed in keys:            
            continue
        else:
            return False
    return True    


class combination_of_article():
    def __init__(self,article,statics,dynamics):
        article = article
        static_box=self.get_static_fields(article,statics)
        dynamics1 = self.clean_dynamics(article,dynamics)
        poss = self.give_possible_index(len(dynamics1))
        self.poss_all = self.create_combinations(static_box,poss,dynamics1,article)
        self.poss_all_str = self.convert_str(self.poss_all,article['infoBox_type'])
            

            
    def clean_dynamics(self,article,dynamics):
        box = article['clean_infoBox']
        dynamics2 = []
        for s in dynamics:
            try:
                if s.decode('utf-8') in article['clean_infoBox'].keys():
                    dynamics2.append(s)
            except Exception as e:
                print e
                pass
        return dynamics2
    def create_combinations(self,static_box,poss,dynamics,article):
        poss_all = []
        for indexes in poss:
            temp = {}
            for k in static_box.keys():
                temp[k] = static_box[k].replace('}','').replace('{','')
            if len(indexes) == 0:
                temp = {}                
                for k in static_box.keys():
                    temp[k] = static_box[k].replace('}','').replace('{','')
                poss_all.append(temp)
                break
            for i in indexes:
                temp[dynamics[i].decode('utf-8')] = article['clean_infoBox'][dynamics[i].decode('utf-8')].replace('}','').replace('{','')
            poss_all.append(temp)
        return poss_all
    def get_static_fields(self,article,statics):
        box = article['clean_infoBox']
        new_box = {}
        for s in statics:
            new_box[s.decode('utf-8')] = box[s.decode('utf-8')]
        return new_box
    def give_possible_index(self,n):
        indexes = []
        for i in range(1,2**n+1):
            info =  str('{0:0>'+str(n)+'b}').format(2**n-i)
            temp = []
            for j in range(0,len(info)):
                if info[j] == '1':
                    temp.append(int(j))
            indexes.append(temp) 
        return indexes
    def convert_str(self,poss_all,box_type):
        global DA_id        
        str_format = "{:0>6}_DA_{}_##.##_(Kişi Türü = \'{}\' ,{})\n"
        poss_strs = []
        for js in poss_all:
            temp=[]
            for k in js.keys():
                k = k.encode('utf-8')
                v = js[k.decode('utf-8')].encode('utf-8')
                temp.append("{} = \'{}\'".format(k,v))
            poss_strs.append(str_format.format(str(DA_id),box_type.replace(' ','_'),box_type,' ,'.join(temp)))
            DA_id +=1
        poss_strs.reverse();
        for v in range(0,len(poss_strs)):
            poss_strs[v] = poss_strs[v].replace('.##','.'+str(v))
        return ''.join(poss_strs)
