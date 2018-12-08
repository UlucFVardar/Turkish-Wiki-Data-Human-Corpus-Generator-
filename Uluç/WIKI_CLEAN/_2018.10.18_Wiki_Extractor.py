
# coding: utf-8

# Author = Uluç Furkan Vardar
# 
# Version = 3.0
# 
# ## Using this code you can manipulate Wiki Dump data. 
# ##### The data you will obtain;
# 	* Article id
# 	* Article title
# 	* Article infoBox type
#     * Article infoBox as bulk
# 	* Article infoBox as clean (empty places thrown or normal)
# 	* The first paragraph of the article as bulk
# 
# 
# The output of the program is placed in an output folder created for that date. (EX Folder name: <2018-10-07>Output/ )
# The output consists of three .txt files.
# #### All Article information. 
# 	file named '<2018-10-07>All_Article.txt'
# 	(Format: ...\n\n\nArticle_id#Article_title#infoBoxType#infoBox_bulk#infoBox_clean#first_paragraph\n\n\n...)
# 
# ####  Hit counter for every infoBox type.
# 	file named '<2018-10-07>infoBoxType_Counter.txt'
# 	(Format: ...\ninfoBoxType#hit_counter\n...)
# 
# ###### Also, A Log file is generated and the important things about the data processing area are printed....

# In[11]:



class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)


# In[12]:


import xml.etree.ElementTree as ET
from collections import Counter

import os
import re



class WikiDumpParser:
    def __init__(self,file_path):
        self.error_count = 0
        self.number_of_article = 0## has infoBox 
        self.number_of_total_article = 0 ## total article in the WikiDump data
        self.no_infoBox_count = 0
        self.non_article_count = 0 
        self.info_box_types = []
        

        self.allArticles_path = ""
        self.infoBoxTypes_path = ""        
        self.log_path = ""
        #generation of tree
        tree = ET.parse(file_path)
        self.root = tree.getroot()
        
    def get_title(self,page):
        return page.find('{http://www.mediawiki.org/xml/export-0.10/}title').text
    def get_id(self,page):
        return page.find('{http://www.mediawiki.org/xml/export-0.10/}id').text
    def get_all_text(self,page):
        Whole_ARC = page.find('{http://www.mediawiki.org/xml/export-0.10/}revision')
        Whole_ARC_without_many_unnecessary_tag = Whole_ARC.find('{http://www.mediawiki.org/xml/export-0.10/}text', {'xml:space': 'preserve'})
        return Whole_ARC_without_many_unnecessary_tag.text
    
    def save_articles(self,article):
        with open(self.allArticles_path, "ab")  as f:
            f.write(article.get_Saving_String())
            
    def save_infoBoxTypes(self):
        self.info_box_types = self.unique( self.info_box_types )
        with open(self.infoBoxTypes_path, "ab")  as f:
            for info_b_type in self.info_box_types:
                f.write(str(info_b_type[0].encode('utf-8'))+'#'+str(info_b_type[1])+'\n')
                
    def save_log(self,title, text):
        with open(self.log_path, "ab") as myfile:
            myfile.write(title +" ---------\n")
            myfile.write( text+"\n")
            myfile.write("--------------------------\n\n")            

    def unique(self,list1):
        c = Counter( list1 )
        return list(c.items())
    def extract_pages(self,allArticles_path,infoBoxTypes_path,log_path):        
        '''This function must extract all pages with InfoBox,and also info boz type must be counted'''
        self.allArticles_path = allArticles_path
        self.infoBoxTypes_path = infoBoxTypes_path 
        self.log_path = log_path
   
        
        for page in self.root.findall('{http://www.mediawiki.org/xml/export-0.10/}page'):
            self.number_of_total_article +=1
            article = Article()
            
            # Getting title, id, whole text of the article
            article.set_title( title = self.get_title(page) )
            article.set_id( id = self.get_id(page) )
            article_text = self.get_all_text(page)
            # -----
            
            # if there is no article text
            if article_text == None:
                self.non_article_count +=1
                continue
            # -----
            
            # Is the article contains a info box or not
            if 'bilgi kutusu' in article_text :
                pass
            else:
                self.no_infoBox_count +=1
                continue
            # -----
            
            article.set_article_text_bulk ( bulk_text = article_text )
            
            # cleaning the article text     
            try:
                article.parse_infoBox()
                article.clean_infoBox()
                article.parse_firstPragraph()
            except Exception as e:
                print e
                self.error_count +=1
                continue
            # -----
            
            self.info_box_types.append( article.get_infoBoxType() )
            self.number_of_article +=1
            self.save_articles(article)
        self.save_infoBoxTypes()
        s =  "\n#Scanned Total Article {} \n#Scanned Article that has InfoBox {} \n#No InfoBox Count {}\n#None Article Count {} (article Area is None)\n#Error Count {} (infoBox clean or getting paragraph error)".                        format(self.number_of_total_article,
                               self.number_of_article,
                               self.no_infoBox_count,
                               self.non_article_count,
                               self.error_count)
        print s
        self.save_log("Wiki Dump Extracted",s)


# In[13]:


class Article:
    def _init_(self):
        self.article_id = -1
        self.article_title = ""
        self.article_info_box = ""
        self.article_text_bulk = ""
        self.article_info_box_clean = ""
        self.article_info_box_type = ""
        self.article_first_paragraph = ""



    def set_id(self,id):
        self.article_id = id
    def set_title(self,title):
        self.article_title = title
    def set_infoBox(self,infoBox):
        self.article_info_box = infoBox
    def set_infoBox_clean(self,infoBox_clean):
        self.article_info_box_clean = infoBox_clean
    def set_infoBox_type(self,infoBox_type):
        self.article_info_box_type = infoBox_type
    def set_infoBox_firts_paragraph(self,paragraph):
        self.article_first_paragraph = paragraph
    def set_article_text_bulk(self,bulk_text):
        self.article_text_bulk = bulk_text
    def get_infoBoxType(self):
        return self.article_info_box_type
    #----
    def parse_infoBox(self):
        text = self.article_text_bulk
        article_txt = text[:text.find("==")]
        infoBoxType = (re.search('{{(.*) bilgi kutusu', article_txt)).group(1)
        self.set_infoBox_type(infoBoxType)
        
        # a little cleaning
        temp = article_txt.split('\n')
        for i in range(0,len(temp)):
            if 'bilgi kutusu' in temp[i]:
                break
            else:
                temp[i]=''
        article_txt = '\n'.join(temp)
        
        infoBox = self.stack_check(article_txt)
        self.set_infoBox( infoBox )

    def clean_infoBox(self):
        infoBox = self.article_info_box
        
        #some cleanings
        infoBox = re.sub(r"\[\[Dosya.*\]\]","",infoBox)
        infoBox = re.sub(r"<br/>","",infoBox)
        infoBox = re.sub(r"<br />","",infoBox)    
        infoBox = re.sub(r"<br>","",infoBox)
        infoBox = infoBox.replace('[[','').replace(']]','').replace("\'\'\'",'').replace("''",'')
        infoBox = infoBox.replace('{{','').replace('}}','')
        infoBox = re.sub(r"<ref(.|\n)*</ref>","",infoBox)
        infoBox = infoBox.replace(u'\xa0', u' ')
        
        #empty place will be deleted
        t = infoBox.split('\n')
        infoBox = []
        for i in range(0,len(t)):
            line = t[i]
            if ' ' == line or ' ' == line or '  ' == line or '' == line:
                continue
            elif line.count('=') == 1:
                if len(line[line.find('='):].replace(' ','')) <3:
                    continue
                else:
                    infoBox.append(t[i])
            else:
                infoBox.append(t[i])
        infoBox = '\n'.join(infoBox)
        self.set_infoBox_clean( '{{'+infoBox+'}}' )
    
    def parse_firstPragraph(self):
        infoBox = self.article_info_box
        article_text = self.article_text_bulk
        #generate end of the infobox to end of the paragrafs
        paragraph = article_text[:article_text.find("==")]
        paragraph = paragraph[paragraph.find(infoBox)+len(infoBox):]

        # nd of the infobox to end of the ONE paragraf
        paragraph_number = paragraph.count('\n\n')
        for i in range(0,paragraph_number-1):
            paragraph = paragraph [:paragraph.rfind('\n\n')]
        self.set_infoBox_firts_paragraph( paragraph ) 
    #----
    def stack_check(self,text):
        stack = Stack()
        lines = text.split("\n")
        isFirst = True
        isFinish = False
        infoBox = []
        for line in lines:
            openB = line.count("{{")
            closeB = line.count("}}")
            for i in range(0,openB):
                stack.push('{{')
            if isFirst == True and openB!=0:
                isFirst=False
                n = stack.pop()
            for i in range(0,closeB):
                if stack.size()>0:
                    if stack.peek() == '{{':
                        n = stack.pop()
                    else:
                        isFinish = True
                else:
                    isFinish = True
            infoBox.append(line)
            if isFinish == True:
                break
        infoBox = '\n'.join(infoBox)
        return infoBox
    
    def get_Saving_String(self):
        r = self.article_id,             self.article_title,             self.article_info_box_type,             self.article_info_box ,             self.article_info_box_clean,             self.article_first_paragraph 
        saving_string =   str(r[0].encode('utf-8')).replace('\n','<nl>').replace('#','') +'#'+                            str(r[1].encode('utf-8')).replace('\n','<nl>').replace('#','') +'#'+                            str(r[2].encode('utf-8')).replace('\n','<nl>').replace('#','') +'#'+                            str(r[3].encode('utf-8')).replace('\n','<nl>').replace('#','') +'#'+                            str(r[5].encode('utf-8')).replace('\n','<nl>').replace('#','') +'\n\n\n' 
        #str(r[4].encode('utf-8')).replace('\n','<nl>').replace('#','') +'#'+\
        return saving_string


# In[14]:


def create_files():
    today = date.today().strftime('<%Y-%m-%d>')
    mypath = '../'+today+'Outputs_Bulk'
    if not os.path.isdir(mypath):
        os.makedirs(mypath)
    article_path = '../'+today+'Outputs_Bulk/All_Article.txt'
    counter_path = '../'+today+'Outputs_Bulk/infoBoxType_Counter.txt'
    log_path = '../'+today+'Outputs_Bulk/Extractor Report.txt'
    f= open(article_path,"w")
    f= open(counter_path,"w")
    f= open(log_path,"w")
    return article_path,counter_path,log_path


# In[ ]:


from datetime import date

article_path,counter_path,log_path = create_files()
wp = WikiDumpParser('../wikidump.xml')
wp.extract_pages(article_path,counter_path,log_path)

