
# coding: utf-8

# 
#  Author = Uluç Furkan Vardar
#  
#  Version = 3.0
#  
# ## Using this code you can manipulate Wiki Dump Extracted data (Depending Interested Data). 
# ### The data you will obtain;
# 
# 
# ###### All article that we are interested
#     * Article id
#     * Article title
#     * Article infoBox type
#     * Article infoBox as bulk
#     * Article infoBox as clean (empty places thrown or normal)
#     * The first sentences of the article as clean
#     * total counts, graphfs
#     * InfoBox Data Field Counts and examples for every one InfoBox Type 
#     * Also infoBox_Clean DataFiled Counts
#     * DataField uniqless flag for InfoBox Types
#     * Also all needed graphs and counts for all 
# 
# 
#  
# ---
# The output of the program is placed in an output folder created for that date. (EX Folder name: <2018-10-07>Output/ )
# The output consists .txt,.pdf,.png files (Grapfhs data etc.).
# 
# 
# #### All Article information. 
#  	file named '<2018-10-07>All_Article.txt'
#  	(Format: ...\n\n\nArticle_id#Article_title#infoBoxType#infoBox_bulk#infoBox_clean#first_paragraph\n\n\n...)
#  
# ####  Hit counter for every infoBox type.
#  	file named '<2018-10-07>infoBoxType_Counter.txt'
#  	(Format: ...\ninfoBoxType#hit_counter\n...)
#  
# ###### Also, A Log file is generated and the important things about the data processing area are printed....
# 
# 

# In[153]:


import re
import json
import codecs

#from dataCleaner import DataCleaner as DC


class InterestedArticles():
    def __init__(self,interested_file_path,all_articles):
        self.Interested_InfoBoxes = []
        
        # Taking info about Interested InfoBoxes        
        self.Interested_InfoBoxTypes_text = open(interested_file_path, "r") .read()
        self.parse_interested_infoBox()
        
        # Taking info about Articles
        self.articles_text  = open(all_articles, "r").read() 
        self.articles_as_list = self.articles_text.split('\n\n\n')
        for i in range(0,len(self.articles_as_list)):
            self.articles_as_list[i] = self.articles_as_list[i].split('#')
            try:
                if self.articles_as_list[i][2] not in self.Interested_InfoBoxes:
                    self.articles_as_list[i] = None
            except Exception as e:
                self.articles_as_list[i] = None
                continue
        self.articles_as_list = [x for x in self.articles_as_list if x is not None]
        self.allinterested_number = len(self.articles_as_list)
    def save_clean_articles(self,path):
        self.canbesaved = 0
        fh = codecs.open(path+'Clean_Interested_Articles.txt','ab','utf8')
        f = open(path+'Clean_Interested_Articles.txt','ab')
        for a in self.articles_as_list:
            try:
                bd = json.dumps(a[3], ensure_ascii=False, encoding='utf8').encode('utf-8')
                cd = json.dumps(a[5], ensure_ascii=False, encoding='utf8').encode('utf-8')
            except Exception as e:
                continue
            #print type(bd)
            #print type('#'+str(a[4])+'#')
            
            f.write(str(a[0]) +'#')
            f.write(str(a[1]) +'#')
            f.write(str(a[2]) +'#')
            f.write(bd)
            f.write('#')
            f.write(cd)
            f.write('#')
            f.write(str(a[4])) 
            f.write('\n\n\n')
            self.canbesaved +=1
            
                    
    def parse_interested_infoBox(self):
        self.Interested_InfoBoxes = self.Interested_InfoBoxTypes_text.split('\n')
        if len(self.Interested_InfoBoxes[len(self.Interested_InfoBoxes)-1] ) <3:
            del self.Interested_InfoBoxes[len(self.Interested_InfoBoxes)-1] 
        for i in range(0,len(self.Interested_InfoBoxes)):
            self.Interested_InfoBoxes[i] = self.Interested_InfoBoxes[i][:self.Interested_InfoBoxes[i].find('#')]

    def save_one_example_of_InfoBoxType_clear_and_bulk(self,output_path):
        mypath = output_path+'InfoBoxType_Examples'
        if not os.path.isdir(mypath):
            os.makedirs(mypath)
            
        templist = [x for x in self.Interested_InfoBoxes]
        
        for t in self.articles_as_list:
            if t[2] in templist:      
                try:
                    file_path = mypath+'/'+t[2]+'.txt'
                    f = codecs.open(file_path,'w','utf8')
                    f.write(json.dumps(t[5], ensure_ascii=False, encoding='utf8',indent=4))
                    f.write('\n\n')
                    f.write(json.dumps(t[3], ensure_ascii=False, encoding='utf8',indent=4))      
                    templist = [x for x in templist if x is not t[2]]
                except Exception as e:
                    print e
                    continue
            if len(templist)==0:
                break


            
    def convert_all_articles_2_clean_json(self):
        for i in range(0,len(self.articles_as_list)):
            try:
                self.articles_as_list[i].append( self.convert_2_json(self.articles_as_list[i][3].replace('<nl>','\n')))
                self.articles_as_list[i][3] = self.clean_jsons(self.articles_as_list[i][5])
            except Exception as e:
                #print e
                continue
    
    def clean_jsons(self,json_text):
        new_json = {}
        for key in json_text.keys():
            temp_key = key
            temp_key.replace('  ',' ')
            temp_value = json_text[key]
            if temp_value.count('|') == 1:
                if '[[' in temp_value:
                    temp_value = self.clean_values(temp_value)
                if '{{' in temp_value:
                    temp_value = self.clean_values2(temp_value)
            temp_value = temp_value.replace('[[','').replace(']]','')
            
            # <br\>
            temp_value = temp_value.replace('<br />',', ').replace('<br/>',', ').replace('<br/ >',', ')            .replace('<br>',', ').replace('<br >',', ').replace("''",'')
            temp_value = self.clean_ref_tag(temp_value)
            
            if temp_value.count('}}') ==1 and temp_value.count('{{') ==0:
                temp_value = temp_value.replace('}}','')
            if temp_value.count('{{') ==1 and temp_value.count('}}') ==0:
                temp_value = temp_value.replace('{{','')
            
            if temp_value != "" :
                if '.png' in temp_value  or '.jpg' in temp_value or '.svg' in temp_value :
                    pass
                else:
                    new_json[temp_key] = temp_value
            
        return new_json
              
    def convert_2_json(self,text):
        lines = text.split('\n')
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
    def clean_values2(self, sentence):
        #print sentence
        paragraph = sentence.split('{{')
        for i in range(0,len(paragraph)):
            try:
                paragraph[i] = (re.search(".*\|(.*)\}\}.*",paragraph[i])).group(1)+" "
            except Exception as e:
                if i == 0:
                    pass
                else:
                    paragraph[i] = paragraph[i]
                pass
        return  ''.join(paragraph)
    
    def clean_values(self, sentence):
        #print sentence
        paragraph = sentence.split('[[')
        for i in range(0,len(paragraph)):
            try:
                paragraph[i] = '[['+(re.search(".*\|(.*\]\].*)",paragraph[i])).group(1)+" "
            except Exception as e:
                if i == 0:
                    pass
                else:
                    paragraph[i] = '[['+paragraph[i]
                pass
        return  ''.join(paragraph)
    def clean_ref_tag(self, paragraph):
        
        paragraph = paragraph.split('\n')
        
        '''
            paragraph: it is a sentencering with '\n'. 
                    Thus, it's able to be porcessed 
                    line by line here.
        '''
        for i,line in enumerate(paragraph):
            open_ref = 0
            close_ref = 0

            # count 'em all in the line
            if '<ref' in line:
                open_ref = line.count("<ref")
            if '</ref>' in line:
                close_ref = line.count("</ref>")


            # if there are many opened and closed 'ref' tags

            # open > close
            if open_ref > close_ref:
                while(open_ref > 0 and close_ref > 0):
                    o_index = line.find('<ref')
                    c_index = line.find('</ref>')
                    if o_index < c_index:
                        firsentence_part = line[:line.find('<ref')]
                        second_part = line[line.find('</ref>')+6:]
                        paragraph[i] = firsentence_part + second_part
                        line = paragraph[i]
                        open_ref-=1
                        close_ref-=1
                o_index = line.find('<ref')
                paragraph[i] = line[:line.find('<ref')]

            # closed > opened
            if close_ref > open_ref:
                paragraph[i] = line[line.find('</ref>')+6:]
                line = paragraph[i]
                close_ref-=1
                while(open_ref > 0 and close_ref > 0):
                    o_index = line.find('<ref')
                    c_index = line.find('</ref>')
                    if o_index < c_index:
                        firsentence_part = line[:line.find('<ref')]
                        second_part = line[line.find('</ref>')+6:]
                        paragraph[i] = firsentence_part + second_part
                        line = paragraph[i]
                        open_ref-=1
                        close_ref-=1

            # (open = close) and > 1 
            if open_ref > 1 and close_ref > 1:
                while(open_ref > 1 and close_ref > 1):
                    o_index = line.find('<ref')
                    c_index = line.find('</ref>')
                    if o_index < c_index:
                        firsentence_part = line[:line.find('<ref')]
                        second_part = line[line.find('</ref>')+6:]
                        paragraph[i] = firsentence_part + second_part
                        open_ref-=1
                        close_ref-=1

            # for 1 opened and 1 closed tags
            if open_ref == 1 and close_ref == 1:
                paragraph[i] = re.sub(r"<ref(.|\n)*</ref>","",paragraph[i])
        return '\n'.join(paragraph)


# In[154]:


interested_path = '/Users/uluc/Desktop/Bitirme/Wikiparse_WorkSpace/<2018.10.-->Wiki/<2018-10-20>Outputs-InfoBoxClean/Interested_InfoBoxType_Count.txt'
all_articles = '/Users/uluc/Desktop/Bitirme/Wikiparse_WorkSpace/<2018.10.-->Wiki/<2018-10-20>Outputs_Bulk/All_Article.txt'

intrested = InterestedArticles(interested_path,all_articles)


intrested.convert_all_articles_2_clean_json()


# In[155]:


from datetime import date
import os

def create_files():
    today = date.today().strftime('<%Y-%m-%d>')
    mypath = '../'+today+'Outputs-ArticleClean'
    if not os.path.isdir(mypath):
        os.makedirs(mypath)
    log_path = '../'+today+'Outputs-ArticleClean/ArticleCleaner_Report.txt'
    f= open(log_path,"w")

    '''    
    article_path = '../'+today+'Outputs-InfoBoxClean/'+today+'All_Article.txt'
    counter_path = '../'+today+'Outputs-InfoBoxClean/'+today+'infoBoxType_Counter.txt'
    log_path = '../'+today+'Outputs-InfoBoxClean/'+today+'Extractor Report.txt'
    f= open(article_path,"w")
    f= open(counter_path,"w")
    f= open(log_path,"w")
    '''
    return mypath+'/',log_path


# In[156]:


output_path,log_path = create_files()

intrested.save_one_example_of_InfoBoxType_clear_and_bulk(output_path = output_path )


# In[162]:


def savelog(path,title,text):
    with open(path, "ab") as myfile:
            myfile.write(title +" ---------\n")
            myfile.write( text+"\n")
            myfile.write("--------------------------\n\n")  
    


# In[158]:


intrested.save_clean_articles(output_path)


# In[164]:


savelog(log_path,'Article Cleaning',(' #Total Interested Article: {}\n #Total Saved Interested Article: {}\n'.format(intrested.allinterested_number,intrested.canbesaved)))
savelog(log_path,'Operations',' All interested articles are taken\n All infoboxes convert to to json\n All info boxes cleaned')

