import xml.etree.ElementTree as ET
import re
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

# Variables
tree = ET.parse('trial.xml')
root = tree.getroot()

wordList = []
paragraph = "" 
beginOffset = None
endOffset = None
special = ""
stc = 0
ID = 1

annFile = open("trialcoref.ann", "w")
textFile = open("trialtext.txt", "w")
thirdFile = open("thirdFile.txt", "w")

# Creating a list of words with begin&endoffsets
for child in root.iter():

	if child.tag == 'S':
		stc = stc + 1

	elif child.tag == 'W':
		IG = child.get('IG')
		word = child.text.strip()
		spacebefore = ' '
		word = word + spacebefore

		beginOffset = len(paragraph) 
		paragraph = paragraph + word 
		endOffset = len(paragraph) - 1

		# Control for if it's a special word or not (named entity recognition for persons)
		if len(IG.split(")(")) == 1 and len(IG.split("Noun")) > 1 and not len(IG.split("+Punc")) > 1:
			special = "PER"
			annFile.write("T%d\t" % ID)
			annFile.write("%s " % special)
			annFile.write("%d " % beginOffset)
			annFile.write("%d\t" % endOffset)
			annFile.write("%s\n" % word.rstrip())

			thirdFile.write("T%d " % ID)
			thirdFile.write("%s " % child.get('IX'))
			thirdFile.write("%s\n" % stc)
			ID += 1

		else:
			special = ""

		# Here append to list the variables for each word 
		wordList.append({ 'word': word, 'begin': beginOffset, 'end': endOffset, 'special': special })
 

# Print the list 

# print (wordList)

# Print the paragraph of word strings 

# print (paragraph)

textFile.write("%s\n" % paragraph.strip())

annFile.close()
textFile.close()
thirdFile.close()
