# -*- coding: UTF-8 -*-

from dataCleaner import DataCleaner as DC

def main():
    print '\n\n'

    dc = DC()
    with open("../data/O4_2018-10-06_articles-allwere alooking.txt", "r") as f:
        with open("../outputs/output.txt","w") as o_f:
            for line in f:
                if not line.startswith('\n') and line.endswith('\n'):
                    dc.process_bulk_paragraph(line.split("#")[4].strip())
                    #print line.split("#")[0].strip(), '\n', dc.clean_sentence
                    o_f.write( line.split("#")[0].strip() + '\n' + dc.clean_sentence + '\n\n')
        o_f.close()
    f.close()
    
    """
    with open("../data/O4_2018-10-06_articles-allwere alooking.txt", "r") as f:
        with open("../data/compressed_original_data.txt","w") as o_f:
            for line in f:
                if not line.startswith('\n') and line.endswith('\n'):
                    o_f.write(line)
        o_f.close()
    f.close()
    """
 
if __name__ == '__main__':
    main()