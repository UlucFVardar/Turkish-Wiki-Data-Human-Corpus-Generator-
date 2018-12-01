# -*- coding: UTF-8 -*-

from dataCleaner import process_bulk_paragraph, set_environment, clear_environment

def main():

    # Sample usage of dataCleaner.py
    
    set_environment() # create outputs folder to work in with temporary text files

    # process the bulk data
    """ 
        @sentences: a tuple that includes (first_sentence, second_sentence)
        @AckMessage: it is a acknowladgement message from dataCleaner.py. You can check if there is a problem by AckMessage to understand problems
    """
    clean_paragraph, sentences, AckMessage = process_bulk_paragraph("Cengiz Han (d. 1162 – ö. 18 Ağustos 1227), Moğol komutan, hükümdar ve Moğol İmparatorluğu'nun kurucusudur. Cengiz Han, 13. Yüzyılın başında Orta Asya'daki tüm göçebe bozkır kavimlerini birleştirerek bir ulus haline getirdi ve o ulusu Moğol siyasi kimliği çatısı altında topladı. Dünya tarihinin en büyük askeri dehalarından biri olarak kabul edilen Cengiz Han, hükümdarlığı döneminde 1206-1227 arasında Kuzey Çin'deki Batı Xia ve Jin Hanedanı, Türkistan'daki Kara Hıtay, Maveraünnehir, Harezm, Horasan ve İran'daki Harzemşahlar ile Kafkasya'da Gürcüler, Deşt-i Kıpçak'taki Rus Knezlikleri ve Kıpçaklar ile İdil Bulgarları üzerine gerçekleştirilen seferler sonucunda Pasifik Okyanusu'ndan Hazar Denizi’ne ve Karadeniz'in kuzeyine kadar uzanan bir imparatorluk kurdu.")
    
    print sentences[0] 
    print sentences[1]
    print AckMessage
    
    clear_environment() # clear all temporary files

if __name__ == '__main__':
    main()