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
        paragraph = self.clean_dosya(paragraph)

        # delete <.*?>.*?</.*?> TAGS
        paragraph = self.clean_tags_regex(paragraph)


        """ --- --- --- --- --- --- --- --- --- --- """

        # After now sentence is obtained to work on it directly 

        # Uluc has added this clean method
        # Need the check this part 
        # [[ ... | ... ]]
        sentence = self.clean_pipes_in_double_square_brackets(paragraph) 

        # delete {{...}} double curly brackets
        sentence = self.clean_double_curly_brackets(sentence)

        # delete (...) except with ( d. ... - o. ...) 
        # It keeps birth day and death info 
        """ISSUE here! Some dates in brackets are represented not with d. or o."""
        sentence = self.clean_round_brackets_except_with_birth_and_death(sentence)
        
        """
        # delete [[...]] 
        # except that includes numbers like birth date or death 
        # ( i.e. [[5 Mayis]] [[1818]] )
        #sentence = self.clean_double_square_brackets(sentence)
        """

        # remove ==...== double equations from the sentence
        sentence =  self.clean_double_equation_mark(sentence)

        # delete unnecessary infos in before bday in brackets (..... d. 1982) 
        sentence = self.clean_unnecessary_info_before_bday_in_round_brackets(sentence)
       
        # remove ' """ ' and  " ''' " in sentence
        sentence = self.clean_triple_quoates(sentence)
    
        # get rid of extra paragraphs
        sentence = self.clean_extra_paragraphs(sentence)

        # to be continued ...
        
        #-------------------------Cleaning finished------------------------------------



        # Here is the cleaned sentence. Ready to write into output text file
        self.clean_sentence = sentence


    def clean_dosya(self, data):
        try:
            return re.sub(r"\[\[Dosya.*\]\]","",data)
        except:
            return data

    def clean_pipes_in_double_square_brackets(self, data):
        try:
            return re.sub(r"\[\[[^\[\{]*\|","",data).replace('[','').replace(']','') # \[\[.*?\|
        except:
            return data.replace(']','').replace('[','')
        
    def clean_double_equation_mark(self, data): #==
        try:
            return re.sub(r"==.*?==","", data)
        except:
            return data

    def clean_tags_regex(self,data):
        try:
           data = re.sub(r"((<br />.*?<br />|<br />)|(<br>.*?<br>|<br>))","",data)
        except:
            pass
        try:
            return re.sub(r"<.*?\/>|<.*?</.*?>","",data)#re.sub(r"^.*?<[/].*?>|<.*?(.|\s)*?</.*?>|<.*?(.|\s)*","",data)
        except:
            return data

    def clean_double_curly_brackets(self,data):
        try:
            return re.sub(r"\(({{.*?(.|\s).*?}})\)|({{.*?(.|\s).*?}})","",data)
        except:
            return data

    def clean_round_brackets_except_with_birth_and_death(self, data):
        try:
            if 'okunusu:' in data:
                data = re.sub(r"\(okunusu:\s.* +sayfalar:.*\)","", data)
            if 'd.' in data:
                try:
                    return data.replace(';','')
                except:
                    pass
            return data #re.sub(r"\(.*[^\)]*;\s\)|\(.*; ","",data)
        except:
            return data
        """
        # Cancelled for now
        try:
            data = re.sub(r"\([^d]\.*.?(.|\s).*?[^o]\.*.?(.|\s).*?\)","",data)
            return re.sub(r"(;.*?\)(.|\s)*?;.*?\)|;.*?\))","",data)
        except:
            return data
        """

    # Cancelled for now
    def clean_double_square_brackets(self, data):
        # Cancelled for now
        try:
            return re.sub(r"\(.*\)","",data).replace(']]','') # \(.*\) # \(.*?\[\[[\D].*?\]\].*?\)
        except:
            return data

    def clean_unnecessary_info_before_bday_in_round_brackets(self, data):
        # i.e.
        # Gulse Birsel (evlilik oncesi soyadi sener d. 11 Mart 1971), Turk oyuncu, senarist ve gazeteci.
        # Gulse Birsel ( d. 11 Mart 1971), Turk oyuncu, senarist ve gazeteci.
        try:
            matches = re.findall(r"\((.*)d\.",data)
            if matches[0] != ' ' and matches != '\t':
                return data.replace(matches[0],"")
            else:
                return data
        except:
            return data

    def clean_triple_quoates(self, data):
        try:
            return data.replace("'''",'').replace("''",'').replace('"','')
        except:
            return data

    def clean_extra_paragraphs(self, data):
        try:
            return data.strip().split('\n')[0]
        except:
            return data

    # NOT USED YET
    def split_sentences(self, data):
        try:
            sentences_list = re.findall(r"[^\.]*[\.]", data)
            return sentences_list
        except:
            return [data]