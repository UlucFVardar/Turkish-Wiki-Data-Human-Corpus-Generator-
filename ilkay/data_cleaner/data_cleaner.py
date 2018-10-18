# -*- coding: UTF-8 -*-
import re

"""
#some cleaning operations from tags etc.
    paragraph = re.sub(r"\[\[Dosya.*\]\]","",paragraph)
    paragraph = re.sub(r"<ref(.|\n)*</ref>","",paragraph)
    # paragraph = re.sub(r"\n","",paragraph)
    paragraph = paragraph.replace('[[','').replace(']]','').replace("'''",'').replace("''",'')
    paragraph = re.sub(r"{{.*}}","",paragraph)

    #cleaning | piped worlds
    p = paragraph.split(' ')
    for i in range(0,len(p)):
        if '|' in p[i]:
            p[i] = p[i].split('|')[1]
    paragraph = ' '.join(p)
    if paragraph.count('}}') == 1 :
        paragraph =paragraph[paragraph.index('}}')+2:]
"""

def ref_tag_cleaner(a):
    for i,line in enumerate(a):
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
            #print("open > close")
            while(open_ref > 0 and close_ref > 0):
                o_index = line.find('<ref')
                c_index = line.find('</ref>')
                if o_index < c_index:
                    first_part = line[:line.find('<ref')]
                    second_part = line[line.find('</ref>')+6:]
                    a[i] = first_part + second_part
                    line = a[i]
                    open_ref-=1
                    close_ref-=1
            o_index = line.find('<ref')
            a[i] = line[:line.find('<ref')]

        # closed > opened
        if close_ref > open_ref:
            #print("closed > opened")
            a[i] = line[line.find('</ref>')+6:]
            line = a[i]
            close_ref-=1
            while(open_ref > 0 and close_ref > 0):
                o_index = line.find('<ref')
                c_index = line.find('</ref>')
                if o_index < c_index:
                    first_part = line[:line.find('<ref')]
                    second_part = line[line.find('</ref>')+6:]
                    a[i] = first_part + second_part
                    line = a[i]
                    open_ref-=1
                    close_ref-=1

        # (open = close) and > 1 
        if open_ref > 1 and close_ref > 1:
            #print("(open = close) and > 1 ")
            while(open_ref > 1 and close_ref > 1):
                o_index = line.find('<ref')
                c_index = line.find('</ref>')
                if o_index < c_index:
                    first_part = line[:line.find('<ref')]
                    second_part = line[line.find('</ref>')+6:]
                    #print(first_part)
                    #print(second_part)
                    a[i] = first_part + second_part
                    open_ref-=1
                    close_ref-=1

        # for 1 opened and 1 closed tags
        if open_ref == 1 and close_ref == 1:
            a[i] = re.sub(r"<ref(.|\n)*</ref>","",a[i])

def clean(st):
    a = st.split('[[')
    for i in range(0,len(a)):
        try:
            a[i] = '[['+(re.search(".*\|(.*\]\].* )",a[i])).group(1)+" "
        except Exception as e:
            if i == 0:
                pass
            else:
                a[i] = '[['+a[i]
            pass
    return  ''.join(a)
def clean_other(st): #==
    if '==' in st:
        return st[:st.find('==')]
    return st


    

def process_line(paragraph):
    paragraph = paragraph.replace("<nl>", "\n")
    #print ("\n\n Original\n")
    #print (paragraph)

    #print ("\n\n [[Dosya.*]] deleted")
    paragraph = re.sub(r"\[\[Dosya.*\]\]","",paragraph)
    #print (paragraph)
    
    #print ("\n\n <ref(.|\n)*</ref> deleted")
    lines = paragraph.split("\n")
    ref_tag_cleaner(lines)
    
    # Last Cleaning Processes
    desired_sentence = "".join(lines)
    desired_sentence = clean(desired_sentence)
    #desired_sentence = desired_sentence.replace('[[','').replace(']]','')
    desired_sentence = desired_sentence.replace("'''",'').replace("''",'').replace('"','')
    #desired_sentence = desired_sentence.split(" ")
    """
    for i, part in enumerate(desired_sentence):
        if '|' in part:
            desired_sentence[i] = part.split('|')[1]
    desired_sentence = " ".join(desired_sentence)
    """

    desired_sentence =  clean_other(desired_sentence)
    print desired_sentence,'\n\n\n'





def main():
    with open("../data/test_data.txt", "r") as f:
        for line in f:
            process_line(line.split("#")[4].strip())
            #breakclea
    f.close()
     
 
if __name__ == '__main__':
    main()