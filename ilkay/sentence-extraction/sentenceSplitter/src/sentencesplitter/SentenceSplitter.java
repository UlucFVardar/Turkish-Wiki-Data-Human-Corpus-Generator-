package sentencesplitter;

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
        String readableFilePath = "../../outputs/output.txt";
        String writableFilePath = "../../outputs/splitted_outputs_v2.txt";

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
                        pw.print(line + "#");
                    } catch (NumberFormatException e) {

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
