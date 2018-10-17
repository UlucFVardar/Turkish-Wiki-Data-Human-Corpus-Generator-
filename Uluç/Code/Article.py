# coding: utf-8

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
        
        infoBox = stack_check(article_txt)
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
    def stack_check(text):
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
        r = self.article_id, \
            self.article_title, \
            self.article_info_box_type, \
            self.article_info_box , \
            self.article_info_box_clean, \
            self.article_first_paragraph 
        saving_string =   str(r[0].encode('utf-8')).replace('\n','<nl>').replace('#','') +'#'+\
                            str(r[1].encode('utf-8')).replace('\n','<nl>').replace('#','') +'#'+\
                            str(r[2].encode('utf-8')).replace('\n','<nl>').replace('#','') +'#'+\
                            str(r[3].encode('utf-8')).replace('\n','<nl>').replace('#','') +'#'+\
                            str(r[4].encode('utf-8')).replace('\n','<nl>').replace('#','') +'#'+\
                            str(r[5].encode('utf-8')).replace('\n','<nl>').replace('#','') +'\n\n\n' 
        return saving_string