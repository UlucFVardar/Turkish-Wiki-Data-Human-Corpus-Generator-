# -*- coding: UTF-8 -*-
import itertools
import json

def main(splitted_output, data_wo_end_of_line, output):
    """
        @splitted_output: output from zemberek Java Code
        @data_wo_end_of_line: this is the new format is created from bulk data file
        @output: is the last version that is required
    """

    with open(splitted_output, "r") as splitted_f:
        with open(data_wo_end_of_line, "r") as original_f:
            with open(output,"w") as output_f:
                
                for line, line2 in itertools.izip(splitted_f, original_f):
                    line_parts = line.strip().split('#')
                    first_sentence = line_parts[1]
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
                                        second_sentence = line_parts[4]
                                    except:
                                        second_sentence = 'None'
                                else:
                                    try:
                                        second_sentence = line_parts[3]
                                    except:
                                        second_sentence = 'None'
                            
                            if part.endswith('(d.') and d_flag == False:
                                first_sentence = line_parts[j] + line_parts[j+1]
                                d_flag = True
                        except:
                            if '(d.' not in part:
                                first_sentence = line_parts[1]
                            else:
                                first_sentence = 'None-Faulty'
                    #print line_parts[0], '\n1. ', first_sentence, '\n2. ',second_sentence, '\n'
                    sentences['s1'] = first_sentence
                    sentences['s2'] = second_sentence
                    output_f.write(line_parts[0] + '#' + line2.split("#")[2] + "#" + line2.split("#")[3] + "#" + json.dumps(sentences) + '\n')
            output_f.close()
        original_f.close()
    splitted_f.close()
    print 'Done canim! :)'



if __name__ == "__main__":
    main("../outputs/splitted_outputs_v2.txt",
    "../data/compressed_original_data.txt",
    "../outputs/combined_sentences.txt"
    )