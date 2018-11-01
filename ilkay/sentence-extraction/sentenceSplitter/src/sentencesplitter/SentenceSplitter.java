package sentencesplitter;

import java.util.List;
import zemberek.core.logging.Log;
import zemberek.tokenization.TurkishSentenceExtractor;
import java.io.*;
import java.lang.System.*;

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
        String readableFilePath = "../../outputs/output.txt";
        String writableFilePath = "../../outputs/splitted_outputs.txt";

        try {
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
                    try {
                        Integer.parseInt(line);
                        pw.println("Artcl No: " + line);
                    } catch (NumberFormatException e) {

                        List<String> sentences = simpleSentenceBoundaryDetector(line);
                        counter = 1;
                        for (String sentence : sentences) {
                            pw.println(counter + ". " + sentence);
                            counter++;
                        }//for end
                        pw.println("\n");

                    }// catch end
                }// if end
            }//while end
            br.close();
            pw.close();
        } catch (IOException e) {
            System.out.println("ERROR! " + e);
        }

        System.out.println("DONE CANIM!");

    }// main end

}// class end
