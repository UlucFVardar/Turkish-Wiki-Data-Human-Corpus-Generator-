# -*- coding: UTF-8 -*-
# encoding=utf8  
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
import itertools
import json
import argparse 
from os import system

# USAGE
# python sentence_combiner.py ../outputs/zemberek_output.txt

def fixZemberekOutput(zemberek_output_path):
    """
        @szemberek_output_path: output path of SentenceSplitter.java
    """
    with open(zemberek_output_path, "r") as f:
        for line in f:
            line_parts = line.strip().split('#')
            first_sentence = line_parts[0]
            second_sentence = ''
            sentences = {}
            d_flag = False
            o_flag = False
            lngth = len(line_parts)
            for j, part in enumerate(line_parts):
                try:
                    if part.endswith('o.') and o_flag == False:
                        first_sentence += line_parts[j+1]
                        o_flag = True
                    
                    if d_flag == True:
                        if o_flag == True:
                            try:
                                second_sentence = line_parts[3]
                            except:
                                second_sentence = 'None'
                        else:
                            try:
                                second_sentence = line_parts[2]
                            except:
                                second_sentence = 'None'
                    
                    if part.endswith('(d.') and d_flag == False:
                        first_sentence = line_parts[j] + " " + line_parts[j+1]
                        d_flag = True
                except:
                    if '(d.' not in part:
                        first_sentence = line_parts[1]
                    else:
                        first_sentence = 'None-Faulty'
            print '\n1. ', first_sentence, '\n2. ',second_sentence, '\n'       
    f.close()
    return (first_sentence, second_sentence)

if __name__ == "__main__":
    # ../outputs/zemberek_output.txt
    # construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	
    ap.add_argument("-rfp", "--read_file_path", required=True,
		help="path to SentenceSplitter.java output (zemberek)")

	args = vars(ap.parse_args())

    fixZemberekOutput(args["read_file_path"])