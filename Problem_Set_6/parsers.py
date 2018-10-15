import string
import csv
import os
from os import listdir
import glob
import json
import sqlite3

################################################################################
# PART #1
################################################################################
def countWordsUnstructured(filename):
    #Initialize a word count dictionary
    wordCounts= {}

    #Open the file & read it
    datafile = open(filename).read()

    #Split out into words
    data = datafile.split()

    #Count the words
    for word in data:
        for mark in string.punctuation:
            word = word.replace(mark, "")
        if word in wordCounts:
            wordCounts[word] = wordCounts[word] + 1
        else: wordCounts[word] = 1

    #Return the word count dictionary
    return(wordCounts)

# Test your part 1 code below.
#countWordsUnstructured("./state-of-the-union-corpus-1989-2017/Bush_1989.txt")

    # This function should count the words in an unstructured text document
    # Inputs: A file name (string)
    # Outputs: A dictionary with the counts for each word
    # +1 bonus point for removing punctuation from the wordcounts

################################################################################
# PART 2
################################################################################
def generateSimpleCSV(targetfile, wordCounts):
#Open the file
    outfile = open(targetfile, "w")
#Get a csv writer
    writer = csv.writer(outfile)
    writer.writerow(['Key','Value'])
#Iterate through the word counts
    #Add to our CSV file
    for k, v in wordCounts.items():
            writer.writerow([k,v])
#Close file
    outfile.close()
#Return pointer to the file
    return(outfile)

# Test your part 2 code below
#generateSimpleCSV("Bush_1989.csv", bush_1989)

    # This function should transform a dictionary containing word counts to a
    # CSV file. The first row of the CSV should be a header noting:
    # Word, Count
    # Inputs: A word count list and a name for the target file
    # Outputs: A new CSV file named targetfile containing the wordcount data


################################################################################
# PART 3
################################################################################
def countWordsMany(directory):
#Open the directory and pull a list of file names
    files = glob.glob(os.path.join(directory,'*.txt'))
#Create a blank dictionary to hold our data
    dictionary = {}
#Populate the dictionary
    #(for) Loop through the list of files
        #For each file, call countWordsUnstructured to get the word counts for that file
    for file in files:
        dictionary[file] = countWordsUnstructured(file)
    return(dictionary)

# Test your part 3 code below
all_dictionaries = countWordsMany("./state-of-the-union-corpus-1989-2017")

    # This function should create a dictionary of word count dictionaries
    # The dictionary should have one dictionary per file in the directory
    # Each entry in the dictionary should be a word count dictionary
    # Inputs: A directory containing a set of text files
    # Outputs: A dictionary containing a word count dictionary for each
    #          text file in the directory

################################################################################
# PART 4
################################################################################
def generateDirectoryCSV(wordCounts, targetfile):
    with open('all_data.csv', 'w') as new_file:
        writer = csv.writer(new_file)
        writer.writerow(['Filename', 'Word', 'Count'])
        for k, v in all_dictionaries.items():
            for key, value in v.items():
                writer.writerow([k,key,value])

# Test your part 4 code below
#generateDirectoryCSV(all_dictionaries, 'all_data.csv')

    # This function should create a CSV containing the word counts generated in
    # part 3 with the header:
    # Filename, Word, Count
    # Inputs: A word count dictionary and a name for the target file
    # Outputs: A CSV file named targetfile containing the word count data


################################################################################
# PART 5
################################################################################
def generateJSONFile(wordCounts, targetfile):
    with open('json_file.json', 'w') as fp:
        json.dump(all_dictionaries, fp)

# Test your part 5 code below
#generateJSONFile(all_dictionaries, 'result.json')

    # This function should create an containing the word counts generated in
    # part 3. Architect your JSON file such that the hierarchy will allow
    # the user to quickly navigate and compare word counts between files.
    # Inputs: A word count dictionary and a name for the target file
    # Outputs: An JSON file named targetfile containing the word count data


################################################################################
# PART 6
################################################################################
def searchCSV(csvfile, word):
    maximum = 0
    with open(csvfile, 'r') as f:
        reader = csv.reader(f, delimiter = ',')
        next(reader)

        for row in reader:
            if word == row[1]:
                if maximum < int(row[2]):
                    maximum = int(row[2])
                    answer = row[0]
        return(answer)

# Test your part 6 code to find which file has the highest count of a given word
#searchCSV('all_data.csv','election')

    # This function should search a CSV file from part 4 and find the filename
    # with the largest count of a specified word
    # Inputs: A CSV file to search and a word to search for
    # Outputs: The filename containing the highest count of the target word

def searchJSON(JSONfile, word):
    maximum = 0
    with open(JSONfile) as json_data:
        jdata = json.loads(json_data.read())
        for key in jdata:
            value = jdata[key]
            for v in value:
                    if word == v:
                            if maximum < int(value[v]):
                                maximum = int(value[v])
                                result = key
        return result

# Test your part 6 code to find which file has the highest count of a given word
#searchJSON('all_data.json', 'election')

    # This function should search a JSON file from part 5 and find the filename
    # with the largest count of a specified word
    # Inputs: An JSON file to search and a word to search for
    # Outputs: The filename containing the highest count of the target word


# +1 bonus point for figuring out how many datapoints you had to process to
# compute this value

#Problem Set 6

#Number 2: Database Schema
'''
Bush_1989
      REAL Idx,
      REAL number,
      TEXT start,
      TEXT Filename,
      TEXT end,
      TEXT President,
      TEXT Prior,
      TEXT Vice,
      TEXT Word,
      REAL Count,


Bush_1990
      REAL Idx,
      REAL number,
      TEXT start,
      TEXT Filename,
      TEXT end,
      TEXT President,
      TEXT Prior,
      TEXT Vice,
      TEXT Word,
      REAL Count,

…
'''

#Number 3: Creating the new database
conn = sqlite3.connect('schema.db')
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS dataPresidents( Idx REAL, president_number REAL, start_term TEXT, Filename TEXT, end_term TEXT, President TEXT, Prior TEXT, Vice TEXT, Word TEXT, Count REAL)')

create_table()
