# -*- coding: UTF-8 -*-

from dataCleaner import DataCleaner as DC

def main():
    print '\n\n'

    dc = DC()
    with open("../data/test_data.txt", "r") as f:
        with open("../outputs/output.txt","w") as o_f:
            for line in f:
                if not line.startswith('\n') and line.endswith('\n'):
                    dc.process_bulk_paragraph(line.split("#")[4].strip())
                    print line.split("#")[0].strip(), '\n', dc.clean_sentence
                    o_f.write( line.split("#")[0].strip() + '\n' + dc.clean_sentence + '\n\n')
                else:
                    print '(:'
        o_f.close()
    f.close()

 
if __name__ == '__main__':
    main()