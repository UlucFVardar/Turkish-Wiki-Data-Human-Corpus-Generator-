# -*- coding: UTF-8 -*-

def main():
    
    with open("../outputs/splitted_outputs_v2.txt", "r") as f:
        with open("../outputs/combined_sentences.txt","w") as o_f:
            for line in f:
                line_parts = line.strip().split('#')
                first_sentence = line_parts[1]
                for i, part in enumerate(line_parts):
                    try:
                        if part.endswith('(d.'):
                            first_sentence += line_parts[i+1]
                        if part.endswith('o.'):
                            first_sentence += line_parts[i+1]
                    except:
                        if '(d.' not in part:
                            first_sentence = line_parts[1]
                        else:
                            first_sentence = 'Faulty'
                    
                o_f.write( line_parts[0] + '#' + first_sentence + '\n')
        o_f.close()
    f.close()

    print 'Done canim! :)'



if __name__ == "__main__":
    main()