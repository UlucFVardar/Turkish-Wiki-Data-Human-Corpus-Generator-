// export CLASSPATH=comm.jar:$CLASSPATH
// "../outputs/zemberek_output.txt"
// "../outputs/output.txt"

// USAGE
// java SentenceSplitter outputs/zemberek_output.txt outputs/output.txt

import java.util.List;
import zemberek.tokenization.TurkishSentenceExtractor;
import java.io.*;

/**
 *
 * @author ilkay
 */
public class SentenceSplitter {

    public static TurkishSentenceExtractor extractor = TurkishSentenceExtractor.DEFAULT;

    public static List simpleSentenceBoundaryDetector(String input) {
        extractor = TurkishSentenceExtractor.DEFAULT;
        return extractor.fromParagraph(input);
    }

    public static void main(String[] args) {
        try {

            // Writer
            FileWriter fw = new FileWriter(args[0]);
            PrintWriter pw = new PrintWriter(fw);

            //Reader
            FileReader fr = new FileReader(args[1]);
            BufferedReader br = new BufferedReader(fr);

            String line;
            int counter;
            while ((line = br.readLine()) != null) {

                if ("".equals(line.trim()) == false) {
                    List<String> sentences = simpleSentenceBoundaryDetector(line.split("#")[6]);
                    pw.print(line+"#");                    
                    counter = 0;
                    int len = sentences.size()-1;
                    for (String sentence : sentences) {
                        if (counter == len) {
                            pw.print(sentence);
                        } else {
                            pw.print(sentence + "@");
                        }
                        counter++;
                    }//for end
                    pw.print("\n\n\n");

                }// if end

            }// while end
        pw.close();
        } catch (IOException e) {
            System.out.println("ERROR! " + e);
        }
    }
}

/*
// Reader
            FileReader fr = new FileReader(readableFilePath);
            BufferedReader br = new BufferedReader(fr);

            // Writer
            FileWriter fw = new FileWriter(writableFilePath);
            PrintWriter pw = new PrintWriter(fw);

            int counter = 0;
            String line;
            // Read .txt file line by line
            while ((line = br.readLine()) != null) {
                
                if ("".equals(line.trim()) == false) {
                    
                        List<String> sentences = simpleSentenceBoundaryDetector(line);
                        counter = 0;
                        int len = sentences.size()-1;
                        for (String sentence : sentences) {
                            if (counter == len) {
                                pw.print(sentence);
                            } else {
                                pw.print(sentence + "#");
                            }
                            counter++;
                        }//for end
                        pw.print("\n");

                }// if end
            
            }//while end
            br.close();
            pw.close();
        } catch (IOException e) {
            System.out.println("ERROR! " + e);
        }

        System.out.println("DONE CANIM!");
*/




