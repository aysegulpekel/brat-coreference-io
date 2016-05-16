# brat-coreference-io

The Scripts

parser.py
This script is for xml parsing and creating files in standoff format of Brat.

Also another file called “thirdfile” is created for keeping the index and sentence numbers of each entities.

Named entity recognition, in this case nouns for person tag, differentiated by the IG= attribute. IG attributes contain the morphological structure of words and easy to split just nouns.
Three files which are created by this script include:
.ann file for annotations. .ann file is structured for text spans with entity id, entity type, begin offset, end offset and the word itself and relationships with relation id, relation type and the arguments which have the relation between.
Text file just for keeping the text in a plain format.
And the third file is for holding the sentence and index numbers of every word. This file is used by creater.py later on but it also allows user to reach easily the location of words without checking raw xml files.

creater.py
Creater script uses created the thirdfile and the .ann file which comes from Brat with all annotations and coreference relations.
It basically converts .ann and the third files into a new xml file. This is done because of storing the information should be platform independent and standoff format is only compatible with Brat. New xml file data format is as follows:
 
For entities:
<mention ID="T1" Type="PER" fromtok="1" stc="3" totok="1" />
For chains: <chains>
<chain ID="R4" Type="Coreference"> <mention T2="T2" />
<mention T1="T1" />
<mention T3="T3" />
</chain>
Chains are created for holding the connected relations so that relations can be kept in a less number identifier and more logical.
The script also differentiate the token numbers which is handled with the content of the third file and counted the word numbers after the beginning token. So it’s also possible to tag multiwords and store them in xml file.