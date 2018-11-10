# -*- coding: UTF-8 -*-
import itertools

def main(splitted_output, data_wo_end_of_line, output):
    with open(splitted_output, "r") as f:
        with open(data_wo_end_of_line, "r") as original_f:
            with open(output,"w") as o_f:
                for line, line2 in itertools.izip(f, original_f):
                    line_parts = line.strip().split('#')
                    first_sentence = line_parts[1]
                    for j, part in enumerate(line_parts):
                        try:
                            if part.endswith('(d.'):
                                first_sentence += line_parts[j+1]
                            if part.endswith('o.'):
                                first_sentence += line_parts[j+1]
                        except:
                            if '(d.' not in part:
                                first_sentence = line_parts[1]
                            else:
                                first_sentence = 'None-Faulty'
                        
                    o_f.write( line_parts[0] + '#' + line2.split("#")[2] + "#" + line2.split("#")[3] + "#" + first_sentence + '\n')
            o_f.close()
        original_f.close()
    f.close()
    print 'Done canim! :)'



if __name__ == "__main__":
    main("../outputs/splitted_outputs_v2.txt",
    "../data/compressed_original_data.txt",
    "../outputs/combined_sentences.txt"
    )