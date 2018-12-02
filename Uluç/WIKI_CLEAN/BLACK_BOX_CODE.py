#!/usr/bin/env python
# coding: utf-8

# In[1]:


from my_logging import my_outputs_and_logging

log = my_outputs_and_logging('BLACK BOX CODE')

print log.get_output_path()


# > First data Reading from Bulk data and clean it(with lib)

# In[2]:


from file_commander import my_file_commander

commander = my_file_commander()
### TO READ
article_path ='/Users/uluc/Desktop/Bitirme/Wikiparse_WorkSpace/<2018.10.-->Wiki/<2018-10-20>Outputs_Bulk/All_Article.txt'
splitter_patter = '\n\n\n'
dataContains_tuples = ['id','title','infoBox_type','text_infoBox','bulk_paragraph']
articles = commander.my_tub_file_reader(article_path,splitter_patter,dataContains_tuples)

##3 this part otomaticley parse infobox

###Save this clean Data
### TO SAVE
dataContains_tuples = ['id','title','infoBox_type','bulk_infoBox','clean_infoBox','bulk_paragraph']
commander.my_tub_file_recorder(log.get_output_path()+'All_Articles.txt',articles,'\n\n\n',dataContains_tuples)

log.save_log('Read Bulk Data',u'#Articles read -> '+str(commander.read_total)+'\n#Articles read successfully -> '+str(commander.read_successfully)+'\n#Articles saved successfully -> '+str(commander.saved_successfully))



# > Data analysis

# In[3]:


import json
from sapsik_bir_Analyser import Article_Analyser
log.add_splitter()
Analysis_Article = Article_Analyser(articles)

mypath = log.get_output_path() +'InfoBoxType_Analysis/'

# > 4
all_categories_greater_4 = Analysis_Article.get_all_uniq_infoBoxTypes_as_list(4)
log.logging('#Total Uniq InfoBox Type ( > 4 ) : '+ str(len(all_categories_greater_4)))
for one in all_categories_greater_4 : 
    log.create_a_file_in_a_folder('InfoBoxType_Analysis','all_categories( > 4 )',one.encode('utf-8'))
Analysis_Article.draw_Repetition_of_all_InfoBoxTypes(mypath,'all_categories( > 4 )',4)

# > 100
all_categories_greater_100 = Analysis_Article.get_all_uniq_infoBoxTypes_as_list(100)
Analysis_Article.draw_Repetition_of_all_InfoBoxTypes(mypath,'all_categories( > 100 )',100)
log.logging('#Total Uniq InfoBox Type ( > 100 ) : '+ str(len(all_categories_greater_100)))
for one in all_categories_greater_100 : 
    log.create_a_file_in_a_folder('InfoBoxType_Analysis','all_categories( > 100 )',one.encode('utf-8'))

    
# Our interested Info Box Types
Interested_Info_Box_Types = ['Hakem' ,'Manken' ,'Makam sahibi' ,'Filozof' ,'Bilim insanı','Güreşçi' 
                             ,'Bilim adamı' ,'Sporcu' ,'Buz patencisi','Asker' 
                             ,'Voleybolcu' ,'Sanatçı','Futbolcu' ,'Oyuncu' 
                             ,'Müzik sanatçısı' ,'Yazar' ,'Kraliyet' ,'Tenis sporcu' ,'Profesyonel güreşçi'
                             ,'Kişi' ,'Basketbolcu'] #'Çizgi roman karakteri' , 'Kurgusal karakter'
log.save_log('Interested Info Box Types',json.dumps(Interested_Info_Box_Types, ensure_ascii=False, encoding='utf8').encode('utf-8'))

Analysis_Article.ignore_other_types(Interested_Info_Box_Types)

all_categories_interested = Analysis_Article.get_all_uniq_infoBoxTypes_as_list(100)

Analysis_Article.draw_Repetition_of_all_InfoBoxTypes(mypath,'all_categories( > Interested Types )',1)
log.logging('#Total Uniq InfoBox Type ( > Interested ) : '+ str(len(all_categories_interested)))
log.logging('#Total Article ( > Interested ) : '+ str(len(Analysis_Article.articles)))
for one in  all_categories_interested : 
    log.create_a_file_in_a_folder('InfoBoxType_Analysis','all_categories( > interested )',one.encode('utf-8'))
    
    
###Save for all interested clean data
### TO SAVE
dataContains_tuples = ['id','title','infoBox_type','bulk_infoBox','clean_infoBox','bulk_paragraph']
commander.my_tub_file_recorder(log.get_output_path()+'All_Articles_Interested.txt',Analysis_Article.articles,'\n\n\n',dataContains_tuples)
log.logging('#Total Articles saved successfully ( > Interested ) : '+ str(commander.saved_successfully))

## for each info box type one example is saved
import json
examples = Analysis_Article.get_one_example_for_every_infoBox_type()
for type_,one_example, in examples :
    log.create_a_file_in_a_folder('InfoBoxType_Examples',type_,json.dumps(one_example, ensure_ascii=False, encoding='utf8',indent=4).encode('utf-8'))
log.logging('For each info box type one example is saved')
    


# >Data Field Count

# In[4]:


mypath = log.get_output_path() +'InfoBoxType_DataField_Counts'
if not os.path.isdir(mypath):
    os.makedirs(mypath)
mypath = mypath+'/'    
Analysis_Article.count_data_fields()
Analysis_Article.save_allCounts_2_file(mypath)
Analysis_Article.save_Counts_for_types(mypath)
Analysis_Article.save_uniq_fields(mypath)
Analysis_Article.save_dataField_Analysis(mypath)     
log.logging('All Data Field Countings finished')


# In[5]:


from file_commander import my_file_commander
from sapsik_bir_Analyser import Article_Analyser
commander = my_file_commander()

### TO READ
article_path = log.get_output_path()+'All_Articles_Interested.txt'
splitter_patter = '\n\n\n'
dataContains_tuples = ['id','title','infoBox_type','bulk_infoBox','clean_infoBox','bulk_paragraph']
articles = commander.my_tub_file_reader(article_path,splitter_patter,dataContains_tuples)
Analysis_Article = Article_Analyser(articles)


import combiner as Combiner
rules = Combiner.get_rules('./RULES.txt')
possible_DAs = Combiner.create_DA_combinations(rules,Analysis_Article.articles)
save_path = log.get_output_path() + 'Dialog_Acts'
tried,counter,DA_id = Combiner.save_DAs(save_path,possible_DAs)

log.add_splitter()
log.save_log('DA Convertion',str( '#Tried to convert to DA from infoBox -> '+str(tried) 
             + '\n#Converted to DA from infoBox -> '+ str(counter) 
             + '\n#DA saved succesfully -> '+ str(DA_id) ))


# In[6]:



from my_logging import my_outputs_and_logging

log = my_outputs_and_logging('BLACK BOX CODE')
#log.save_log('BLACK BOX CODE',u'This Code takes the bulk wiki dump data.\nThen Parse it to end up with possible dialog acts')

print log.get_output_path()

from file_commander import my_file_commander
from sapsik_bir_Analyser import Article_Analyser
commander = my_file_commander()
### TO READ
article_path = '../<2018-12-01>Outputs-BLACK BOX CODE/All_Articles_Interested.txt'
splitter_patter = '\n\n\n'
dataContains_tuples = ['id','title','infoBox_type','bulk_infoBox','clean_infoBox','bulk_paragraph']
articles = commander.my_tub_file_reader(article_path,splitter_patter,dataContains_tuples)
Analysis_Article = Article_Analyser(articles)




# In[ ]:





# In[26]:





# In[13]:


type(Analysis_Article.articles[0].article['bulk_paragraph'])


# In[33]:


# -*- coding: UTF-8 -*-

from dataCleaner13 import process_bulk_paragraph, set_environment, clear_environment

# Sample usage of dataCleaner.py

set_environment() # create outputs folder to work in with temporary text files

# process the bulk data
""" 
    @sentences: a tuple that includes (first_sentence, second_sentence)
    @AckMessage: it is a acknowladgement message from dataCleaner.py. You can check if there is a problem by AckMessage to understand problems
"""
sentences, AckMessage = process_bulk_paragraph("Cengiz Han (d. 1162 – ö. 18 Ağustos 1227), Moğol komutan, hükümdar ve Moğol İmparatorluğu'nun kurucusudur. Cengiz Han, 13. Yüzyılın başında Orta Asya'daki tüm göçebe bozkır kavimlerini birleştirerek bir ulus haline getirdi ve o ulusu Moğol siyasi kimliği çatısı altında topladı. Dünya tarihinin en büyük askeri dehalarından biri olarak kabul edilen Cengiz Han, hükümdarlığı döneminde 1206-1227 arasında Kuzey Çin'deki Batı Xia ve Jin Hanedanı, Türkistan'daki Kara Hıtay, Maveraünnehir, Harezm, Horasan ve İran'daki Harzemşahlar ile Kafkasya'da Gürcüler, Deşt-i Kıpçak'taki Rus Knezlikleri ve Kıpçaklar ile İdil Bulgarları üzerine gerçekleştirilen seferler sonucunda Pasifik Okyanusu'ndan Hazar Denizi’ne ve Karadeniz'in kuzeyine kadar uzanan bir imparatorluk kurdu.")

print sentences[0] 
print sentences[1]
print AckMessage

clear_environment() # clear all temporary files


# In[ ]:





# In[ ]:




