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
                self.error_count +=1
                continue
            # -----
            
            self.info_box_types.append( article.get_infoBoxType() )
            self.number_of_article +=1
            
            self.save_articles(article)
        self.save_infoBoxTypes()
        s =  "\n#Scanned Total Article {} \n#Scanned Article that has InfoBox {} \n#No InfoBox Count {}\n#None Article Count {} (article Area is None)\n#Error Count {} (infoBox clean or getting paragraph error)".\
                        format(self.number_of_total_article,
                               self.number_of_article,
                               self.no_infoBox_count,
                               self.non_article_count,
                               self.error_count)
        print s
        self.save_log("Wiki Dump Extracted",s)
