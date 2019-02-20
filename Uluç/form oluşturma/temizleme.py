#!/usr/bin/env python
# coding: utf-8

# In[1]:


import glob
paths = glob.glob('./Dialog_Acts/*')


# In[2]:


maps = {
    'Asker' : 'Askeri',
    'Basketbolcu' : 'Basketbolcuyu',
    'Bilimadamı' : 'Bilim Adamını',
    'Biliminsanı' : 'Bilim İnsanını',
    'Buzpatencisi' : 'Buz Patencisini',
    'Filozof' : 'Filozofu',
    'Güreşçi' : 'Güreşçiyi',
    'Hakem':'Hakemi',
    'Kişi':'Kişiyi',
    'Kraliyet' : 'Kraliyet Mensubunu',
    'Makamsahibi':'Makam Sahibi Kişiyi',
    'Manken':'Mankeni',
    'Müziksanatçısı':'Müzük Sanatçısını',
    'Oyuncu':'Oyuncuyu',
    'Sanatçı':'Sanatçıyı',
    'Sporcu': 'Sporcuyu',
    'Tenissporcu':'Tenis Sporcusunu',
    'Voleybolcu':'Voleybolcuyu',
    'Yazar':'Yazarı',
    'Futbolcu':'Futbolcuyu',
    
    
}


# In[3]:


# "{:0>6}_DA_{}_##.##_(Kişi Türü = \'{}\' ,{})\n"
pattern = "(^[0-9]*)_DA_((.[^\d]*))_(\d+).(\d+)_\(Kişi Türü = '(.[^\(\d\|'\)]*)' ,(.*)\)\n"
new_pattern = "Şu %s, verilen bilgileri kullanarak tanıtınız:\t%s\t%s\t%s\t%s\t%s\n"
import re
paths = glob.glob('./Dialog_Acts/*')
for one_path in paths:
    file = open(one_path,'r')
    file_out_s = open (one_path.replace('Dialog_Acts','silinmeden/Dialog_Acts_forms0').replace('.txt','.tsv'),'w')
    file_out_1 = open (one_path.replace('Dialog_Acts','silinmeden/Dialog_Acts_forms1').replace('.txt','.tsv'),'w')
    file_out_2 = open (one_path.replace('Dialog_Acts','silinmeden/Dialog_Acts_forms2').replace('.txt','.tsv'),'w')
    file_out_3 = open (one_path.replace('Dialog_Acts','silinmeden/Dialog_Acts_forms3').replace('.txt','.tsv'),'w')
    file_out_4 = open (one_path.replace('Dialog_Acts','silinmeden/Dialog_Acts_forms4').replace('.txt','.tsv'),'w')    
    file_out_5 = open (one_path.replace('Dialog_Acts','silinmeden/Dialog_Acts_forms5').replace('.txt','.tsv'),'w')        
    DAs_in_file = file.readlines()
    counter = 1
    flag = True
    for DA in DAs_in_file:
        
        m = re.search(pattern, DA.replace('\t',' '))
        try:
            id = m.group(1)
            BK_type = m.group(2)
            in_cat_DA_number = m.group(4)
            in_DA_row = m.group(5)            
            data = m.group(7).replace('\'','"')
            
            new_string = new_pattern%(maps[BK_type.replace(' ','').replace('_','')],id,BK_type,in_cat_DA_number,in_DA_row,data) 
            if in_DA_row == '0':
                staticlen = data.count('=')
                file_out_s.write(new_string)
            elif staticlen+1 == data.count('='):
                file_out_1.write(new_string)
            elif staticlen+2 == data.count('='):
                file_out_2.write(new_string)
            elif staticlen+3 == data.count('='):
                file_out_3.write(new_string)
            elif staticlen+4 == data.count('='):
                file_out_4.write(new_string)                
            elif staticlen+5 == data.count('='):
                file_out_5.write(new_string)
            counter += 1
        except Exception as e:
            print e
            print 'Sikinti'
            break
    file.close()        
    file_out_s.close()
    file_out_1.close()
    file_out_2.close()
    file_out_3.close()
    file_out_4.close()
    file_out_5.close()
    
    
    
    


# In[4]:


paths = glob.glob('./silinmeden/*/*')
import os
for p in paths:
    f = open(p,'r')
    l = f.readlines()
    if len(l)>1:
        continue
    p = p.replace(' ','\\ ')
    a = os.system('rm '+p)
    #print a,len(l),p


# In[6]:


new_pattern = "'Şu %s, verilen bilgileri kullanarak tanıtınız:'\t%s\t%s\t%s\t%s\t%s"
paths = glob.glob('./silinmeden/*/*')

for path in paths:
    file = open(path,'r')
    lines = file.readlines()
    file.close()
    file = open(path.replace('silinmeden','silerek'),'w+')    
    flag = {}
    for line in lines:
        txt,id,BK_type,in_cat_DA_number,in_DA_row,data = line.split('\t')
        try:
            a = flag[in_cat_DA_number] #dublicaye izin vermemk icin hata olursa dublica degil demektir
        except Exception as e:
            flag[in_cat_DA_number] = 'ok'
            new_string = new_pattern%(maps[BK_type.replace(' ','').replace('_','')],id,BK_type,in_cat_DA_number,in_DA_row,data) 
            file.write(new_string)
        counter +=1
    file.close()
        
    


# In[7]:


paths = glob.glob('./silerek/*/*')
import os
for p in paths:
    f = open(p,'r')
    l = f.readlines()
    if len(l)>1:
        continue
    p = p.replace(' ','\\ ')
    a = os.system('rm '+p)
    #print a,len(l),p


# In[ ]:





# In[ ]:





# In[ ]:




