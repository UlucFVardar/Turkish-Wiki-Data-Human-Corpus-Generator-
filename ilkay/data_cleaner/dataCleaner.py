# -*- coding: UTF-8 -*-
import re

# re.sub(r"<ref(.|\n)*</ref>","",paragraph[i])

class DataCleaner:
    def __init__(self):
        self.clean_sentence = ''
    
    def process_bulk_paragraph(self, data):
        '''
            data: line.split("#")[4] form bulkd data file
        '''

        # open '\n'
        paragraph = data.replace("<nl>", "\n")


        # delete '[[Dosya.*]]'
        paragpah = self.clean_dosya(paragraph)
        #print '__[Dosya...]] OK'

        # delete <.*?>.*?</.*?> TAGS
        paragraph = self.clean_tags_regex(paragraph)
        #print '__Tags OK'

        """ -------------------------- """
        # After now sentence is obtained to work on it directly 

        # Uluc has added this clean method
        # Need the check this part 
        # [[ ... | ... ]]
        sentence = self.clean_pipes_in_double_square_brackets(paragraph) 
        #print '__[[..|..]] OK'

        # delete {{...}} double curly brackets
        sentence = self.clean_double_curly_brackets(sentence)
        #print '__{{...}} OK'

        # delete (...) except with ( d. ... - o. ...) 
        # It keeps birth day and death info 
        """ISSUE here! Some dates in brackets are represented not with d. or o."""
        sentence = self.clean_round_brackets_except_with_birth_and_death(sentence)
        #print '__(...) OK'

        # delete [[...]] 
        # except that includes numbers like birth date or death 
        # ( i.e. [[5 Mayis]] [[1818]] )
        sentence = self.clean_double_square_brackets(sentence)
        #print '__ ( [[...]] ) OK'

        # remove ==...== double equations from the sentence
        sentence =  self.clean_double_equation_mark(sentence)
        #print '__ ==...== OK'

        
        # to be continued ...
       
        
        # remove ' " ' and  " ' " in sentence
        try:
            sentence = sentence.replace("'''",'').replace("''",'').replace('"','')
        except:
            pass
        #print """ '__ " "  ' ' OK """

        
        #-------------------------Cleaning finished------------------------------------
       
        # Here is the cleaned sentence. Ready to write into output text file
        self.clean_sentence = sentence

    def clean_dosya(self, data):
        try:
            return re.sub(r"\[\[Dosya.*\]\]","",paragraph)
        except:
            return data

    def clean_pipes_in_double_square_brackets(self, data):
        try:
            return '[[' + re.sub(r"\[\[.*?\|","",data)
        except:
            return data
        
    def clean_double_equation_mark(self, data): #==
        try:
            return re.sub(r"==.*?==","", data)
        except:
            return data

    def clean_tags_regex(self,data):
        try:
           data = re.sub(r"((<br />.*?<br />|<br />)|(<br>.*?<br>|<br>))","",data)
        except:
            data = data
        try:
            return re.sub(r"^.*?<[/].*?>|<.*?(.|\s)*?</.*?>|<.*?(.|\s)*","",data)
        except:
            return data

    def clean_double_curly_brackets(self,data):
        try:
            return re.sub(r"{{.*?(.|\s).*?}}","",data)
        except:
            return data

    def clean_round_brackets_except_with_birth_and_death(self, data):
        try:
            data = re.sub(r"\([^d]\.*.?(.|\s).*?[^o]\.*.?(.|\s).*?\)","",data)
            return re.sub(r"(;.*?\)(.|\s)*?;.*?\)|;.*?\))","",data)
        except:
            return data

    def clean_double_square_brackets(self, data):
        try:
            return re.sub(r"\(.*?\[\[[\D].*?\]\].*?\)","",data).replace('[[','').replace(']]','')
        except:
            return data

