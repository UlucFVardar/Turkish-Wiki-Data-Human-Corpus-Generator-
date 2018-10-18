# -*- coding: UTF-8 -*-
import re

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
        paragraph = re.sub(r"\[\[Dosya.*\]\]","",paragraph)
        
        # delete '<ref> *** </ref>'
        lines_of_paragraph = paragraph.split("\n")
        self.clean_ref_tag(lines_of_paragraph)
        
        
        # After now sentence is obtained to work on it directly #
        sentence = "".join(lines_of_paragraph)
        
        sentence = self.clean(sentence) # Uluc has added this clean method
                                        # Need the check this part 
                                        # [[ ... | ... ]]

        # remove ' " ' and  " ' " in sentence
        sentence = sentence.replace("'''",'').replace("''",'').replace('"','')

        # remove ==...== double equations from the sentence
        sentence =  self.clean_double_equation_mark(sentence)
        
        # to be continued ...

        # Here is the cleaned sentence. Ready to write into output text file
        self.clean_sentence = sentence
    
    def clean_ref_tag(self, paragraph):
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

    def clean(self, sentence):
        paragraph = sentence.split('[[')
        for i in range(0,len(paragraph)):
            try:
                paragraph[i] = '[['+(re.search(".*\|(.*\]\].* )",paragraph[i])).group(1)+" "
            except Exception as e:
                if i == 0:
                    pass
                else:
                    paragraph[i] = '[['+paragraph[i]
                pass
        return  ''.join(paragraph)

    def clean_double_equation_mark(self, sentence): #==
        '''
            sentence: it is literally the sentence
                    that is desired to be obtained 
        '''
        if '==' in sentence:
            return sentence[:sentence.find('==')]
        return sentence