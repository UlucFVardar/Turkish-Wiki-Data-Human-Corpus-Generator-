#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from datetime import date
import os
'''Simple usage

from my_logging as my_outputs_and_logging

log = my_outputs_and_logging('Script_Porpuse')
log.logging('to notify any event or operation')
log.logging('works only english alfabet')
log.logging('json cleaning operation -> "olumtarihi" Done ')

log.save_log('Script_Porpuse',u'#.... 2344\n#.... 23454')

print log.get_output_path()

'''
class my_outputs_and_logging():
    def __init__(self,output_folder_name):
        self.output_folder_name = output_folder_name
        self.create_files()
        
    def create_files(self):
        today = date.today().strftime('<%Y-%m-%d>')
        mypath = '../'+today+'Outputs-'+self.output_folder_name
        if not os.path.isdir(mypath):
            os.makedirs(mypath)
        log_path = mypath+'/'+self.output_folder_name+'_Report.txt'
        f= open(log_path,"w")
        f.close()
        self.log_path = log_path
        self.output_path = mypath+'/'
    
    def logging(self,text):

        with open(self.log_path, "ab") as myfile:
            myfile.write( 'INFO : ')
            myfile.write( text )
            myfile.write(str('\n'))
            
    def save_log(self,title, text):
        with open(self.log_path, "ab") as myfile:
            myfile.write( title+str(" ---------\n") )
            myfile.write( text + str("\n") )
            myfile.write("--------------------------\n\n")            
    def get_output_path(self):
        return self.output_path