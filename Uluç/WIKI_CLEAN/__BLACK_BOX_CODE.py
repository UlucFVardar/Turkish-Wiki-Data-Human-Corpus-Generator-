#!/usr/bin/env python
# coding: utf-8

# In[3]:


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


# ---
# > To generate clean Paragraph

# In[6]:


'''
from my_logging import my_outputs_and_logging
log = my_outputs_and_logging('BLACK BOX CODE')
print log.get_output_path()
log.add_splitter()
'''
from file_commander import my_file_commander
from sapsik_bir_Analyser import Article_Analyser
commander = my_file_commander()

### TO READ
article_path = log.get_output_path()+'All_Articles_Interested.txt'
splitter_patter = '\n\n\n'
dataContains_tuples = ['id','title','infoBox_type','bulk_infoBox','clean_infoBox','bulk_paragraph']
articles = commander.my_tub_file_reader(article_path,splitter_patter,dataContains_tuples)
Analysis_Article = Article_Analyser(articles)


from dataCleaner import process_bulk_paragraph

count = 0 
for i,a in enumerate(Analysis_Article.articles):
    bulk_paragraph = a.article['bulk_paragraph']
    clean_paragraph = process_bulk_paragraph(bulk_paragraph)
    if 'None' not in clean_paragraph:
        count +=1
    Analysis_Article.articles[i].article['clean_paragraph'] = clean_paragraph



### Save for all interested clean data with clean_paragraph
### TO SAVE
dataContains_tuples = ['id','title','infoBox_type','bulk_infoBox','clean_infoBox','bulk_paragraph','clean_paragraph']
commander.my_tub_file_recorder(log.get_output_path()+'All_Articles_Interested_with_clean_paragraph.txt',Analysis_Article.articles,'\n\n\n',dataContains_tuples)
log.logging('#Total Articles saved successfully ( > Interested + clean_paragraph ) : '+ str(commander.saved_successfully))
log.logging('#Total Articles saved with clean paragraph successfully ( > Interested + clean_paragraph ) : '+ str(count))


# ---
# > To generate sentences

# In[4]:


from dataCleaner import generate_and_save_articles_with_santences

generate_and_save_articles_with_santences( inputfile = log.get_output_path()+'All_Articles_Interested_with_clean_paragraph.txt',
                                           output_file = log.get_output_path()+'All_Articles_Interested_with_clean_paragraph_and_sentences.txt')




# ---
# > Save examples for each type

# In[7]:


## for each info box type one example is saved
import json
examples = Analysis_Article.get_one_example_for_every_infoBox_type()
for type_,one_example, in examples :
    log.create_a_file_in_a_folder('InfoBoxType_Examples',type_,json.dumps(one_example, ensure_ascii=False, encoding='utf8',indent=4).encode('utf-8'))
log.logging('For each info box type one example is saved')
    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




