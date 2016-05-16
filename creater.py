import re
from xml.etree import ElementTree as ET

annFile = open("trialcoref.ann", "r+")
thirdFile = open("thirdfile.txt", "r+")

# For pretty printing from http://effbot.org/zone/element-lib.htm#prettyprint
def indent(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i

def createXML():
  
  coreferences = ET.Element("coreferences")
  mentions = ET.SubElement(coreferences, "mentions")
  chains = ET.SubElement(coreferences, "chains")   
  tree = ET.ElementTree(coreferences)
  chainClusterList = [] 
  chainCluster = []

  # For every line of the file, it splits tabs and spaces, by split it becomes a tuple to reach its elements.
  for line in annFile:
    annList = re.split("([^\t ]+)\s+", line)

    # If it encounters with any T then it saves the mentions (entities).
    if re.match("T", line):
      mention = ET.SubElement(mentions, "mention")
      mention.attrib["ID"] = annList[1]
      mention.attrib["Type"] = annList[3]

      # From the third file, getting the number of sentence 
      for aline in thirdFile:
        thirdList = re.split("([^\t ]+)\s+", aline)
        mention.attrib["stc"] = thirdList[5]
        mention.attrib["fromtok"] = thirdList[3]
        break

      # It counts the word number after partition
      multiWords = line.partition(annList[7])
      bagOfWords = multiWords[2].split(' ')
      
      # If it's a multiword
      if len(bagOfWords) > 1:
        mention.attrib["totok"] = str(len(bagOfWords) + 1)

      # If it's a single word
      else:
        mention.attrib["totok"] = thirdList[3]
      # print(bagOfWords)
    
    # If it encounters with any R then it saves the relations as chains:
    if re.match("R", line):
      arg1, fromArg = annList[5].split(':')
      arg2, toArg = annList[7].split(':')
      added = False

      for chainCluster in chainClusterList:

        # If any argument is in the chain, than add the other one
        if fromArg in chainCluster or toArg in chainCluster:
          chainCluster.add(fromArg)
          chainCluster.add(toArg)
          added = True  

      # If both argument are not added yet into the chains list    
      if not added: 
        chainClusterList.append(set([fromArg,toArg]))
  
  # print(chainClusterList)

  # Create chain tags 
  for element in chainClusterList:

    chain = ET.SubElement(chains, "chain")
    chain.attrib["ID"] = annList[1]
    chain.attrib["Type"] = annList[3]
    element = list(element)
    
    # Create mentions belong to the chain
    for each in element:
      itsMention = ET.SubElement(chain, "mention") 
      itsMention.attrib["ID"] = each

  # Pretty printing the xml
  indent(coreferences) 
  tree.write("coreferences.xml", xml_declaration=True, encoding='utf-8', method="xml")

if __name__ == "__main__":

  createXML()


