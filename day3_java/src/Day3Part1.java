import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Day3Part1 {
    Scanner file;
    List<String> fileContentArray; // every element of the array contain one line of the file
    int lineLength;
    int sumOfPartsNumbers;

    private void readFile(String filename) throws FileNotFoundException {
        this.fileContentArray = new ArrayList<>();
        this.file = new Scanner(new File(filename));

        while (file.hasNextLine()) {
            this.fileContentArray.add(file.nextLine());
        }
        file.close();
        lineLength = fileContentArray.size();
    }

    // isNumber
    private boolean isNumber(char character) {
        // char character = fileContentArray.get(lineIndex).charAt(charIndex);
        return Character.isDigit(character);
    }

    // isSymbol
    private boolean isSymbol(char character) {
        // char character = fileContentArray.get(lineIndex).charAt(charIndex);

        // is not digit && is not letter && is not whitespace && is not dot
        return (!Character.isDigit(character) && !Character.isLetter(character) && !Character.isWhitespace(character)
                && character != '.');
    }

    // isDot
    // private boolean isDot(char character) {
    // return character == '.';
    // }

    // search: find the fisrt appearance of a number, get the range, send it to
    // isPart, send it to calc -> calls: isNumber, isPart, calcaluteTheSum
    private void search() {
        // loop to read line
        for (int i = 0; i < this.fileContentArray.size(); i++) {
            String line = this.fileContentArray.get(i);
            int startIndex, endIndex;
            int j = 0;
            for (j = 0; j < line.length(); j++) {
                // find a digit
                if (isNumber(line.charAt(j))) {
                    // find range (size)
                    startIndex = j;
                    endIndex = range(startIndex, i);

                    // call isPart function to find out if it's a part number or not
                    if (isPart(i, startIndex, endIndex)) {
                        // test1:
                        System.out.printf("number: %3s\tline:%3d startI:%2d endI:%2d\n", line.substring(startIndex, endIndex + 1), i, startIndex, endIndex);
                        int partNumber = Integer.parseInt(line.substring(startIndex, endIndex + 1));
                        calcaluteTheSum(partNumber);
                    }
                    j = endIndex; // to jump to the next character after the number
                }
            }
        }
    }

    // isPart(currentLineIndex, startIndex, endIndex): find out if the number is
    // adjacent to any symbol -> calls: isNumber, isSymbol, isDot
    private boolean isPart(int currentLineIndex, int startIndex, int endIndex) {
        String line = this.fileContentArray.get(currentLineIndex);

        try {
            /* ------------- check current line ------------- */
            // check before:
            if (startIndex > 0) {
                if (isSymbol(line.charAt(startIndex - 1))) {
                    return true;
                }
            }
            if (endIndex < this.lineLength - 1) {
                if (isSymbol(line.charAt(endIndex + 1))) {
                    return true;
                }
            }
        } catch (Exception e) {
            System.out.println(e);
        }

        // setting the range to search:
        if (startIndex > 0) {
            startIndex -= 1;
        }
        if (endIndex < line.length() - 1) {
            endIndex += 1;
        }

        /* ------------- check prev line ------------- */
        if (currentLineIndex != 0) { // make sure it's not the first line
            String prevLine = this.fileContentArray.get(currentLineIndex - 1);
            for (int i = startIndex; i <= endIndex; i++) {
                if (isSymbol(prevLine.charAt(i))) {
                    return true;
                }
            }
        }

        /* ------------- check next line ------------- */
        if (currentLineIndex != this.fileContentArray.size() - 1) { // make sure it's not the last line
            String nextLine = this.fileContentArray.get(currentLineIndex + 1);
            for (int i = startIndex; i <= endIndex; i++) {
                if (isSymbol(nextLine.charAt(i))) {
                    return true;
                }
            }
        }
        return false;
    }

    // calcaluteTheSum(int) receive the part number and add to total
    private void calcaluteTheSum(int number) {
        this.sumOfPartsNumbers += number;
    }

    // range(startIndex, arrayIndex): return endIndex
    private int range(int startIndex, int arrayIndex) {
        int endIndex = startIndex;
        String line = this.fileContentArray.get(arrayIndex);

        while (endIndex + 1 < lineLength && isNumber(line.charAt(endIndex + 1))) {
            endIndex++;
        }

        return endIndex;
    }

    public void run() throws FileNotFoundException {
        readFile("part1-input.txt");
        search();
        System.out.printf("The sum of all of the part numbers in the engine schematic is: %d\n",
                this.sumOfPartsNumbers);
    }
}
