# -*- coding: UTF-8 -*-
# In[6]:



from my_logging import my_outputs_and_logging

log = my_outputs_and_logging('BLACK BOX CODE')
#log.save_log('BLACK BOX CODE',u'This Code takes the bulk wiki dump data.\nThen Parse it to end up with possible dialog acts')

print log.get_output_path()

from file_commander import my_file_commander
from sapsik_bir_Analyser import Article_Analyser
commander = my_file_commander()
### TO READ
article_path = '../<2018-12-02>Outputs-BLACK BOX CODE/All_Articles_Interested_V2.txt'
splitter_patter = '\n\n\n'
dataContains_tuples = ['id','title','infoBox_type','bulk_infoBox','clean_infoBox','bulk_paragraph','DA_as_str','DA_fields']
articles = commander.my_tub_file_reader(article_path,splitter_patter,dataContains_tuples)
Analysis_Article = Article_Analyser(articles)



# -*- coding: UTF-8 -*-
import json 
from dataCleaner import process_bulk_paragraph, set_environment, clear_environment

# Sample usage of dataCleaner.py

set_environment() # create outputs folder to work in with temporary text files

# process the bulk data
""" 
    @sentences: a tuple that includes (first_sentence, second_sentence)
    @AckMessage: it is a acknowladgement message from dataCleaner.py. You can check if there is a problem by AckMessage to understand problems
"""
clean_sentence_number = 0 
for i,a in enumerate(Analysis_Article.articles):
    try:
        clean_paragraph ,sentences, AckMessage = process_bulk_paragraph(a.article['bulk_paragraph'])
        sentance_str = sentences[0] + '@'+sentences[1]
        Analysis_Article.articles[i].article['clean_paragraph'] = clean_paragraph  
        Analysis_Article.articles[i].article['clean_sentences'] = sentance_str
        if sentences[0] != 'None':
            clean_sentence_number +=1
    except Exception as e:
        Analysis_Article.articles[i].article['clean_paragraph'] = 'None'
        Analysis_Article.articles[i].article['clean_sentences'] = 'None'        
        pass


clear_environment() # clear all temporary files


###Save for all interested clean data
### TO SAVE
dataContains_tuples = ['id','title','infoBox_type','bulk_infoBox','clean_infoBox','bulk_paragraph','DA_as_str','DA_fields','clean_paragraph','clean_sentences']
commander.my_tub_file_recorder(log.get_output_path()+'All_Articles_Interested_V3.txt',Analysis_Article.articles,'\n\n\n',dataContains_tuples)
log.logging('#Total Articles saved successfully ( > Interested_V3 ) : '+ str(commander.saved_successfully))
log.logging('#Total Articles saved with Sentence/s ( > Interested_V3 ) : '+ str(clean_sentence_number))



