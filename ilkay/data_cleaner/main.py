# -*- coding: UTF-8 -*-

from dataCleaner import DataCleaner as DC

def main():
    print '\n\n'

    dc = DC()
    with open("../data/test_data.txt", "r") as f:
        for line in f:
            if not line.startswith('\n') and line.endswith('\n'):
                dc.process_bulk_paragraph(line.split("#")[4].strip())
                print dc.clean_sentence, ''
            else:
                print '(:'
    f.close()

 
if __name__ == '__main__':
    main()