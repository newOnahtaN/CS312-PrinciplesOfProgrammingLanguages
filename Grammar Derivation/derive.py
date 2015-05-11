import string
from collections import deque

class RuleMaker(object):

	def __init__(self, fileName):
		#generate grammar rules from the file provided
		self.fileName = fileName
		self.grammarDictionary = {}
		self.startSymbol = None

	def generateGrammarRules(self):

		for line in open(self.fileName, "r"):
			lineElements = line.split()

			nonTerminal, derivation = lineElements[0], lineElements[2:]

			if self.startSymbol == None:
				self.startSymbol = nonTerminal

			#add an alternative to an existing derivation to the grammar dictionary
			if self.grammarDictionary.has_key(nonTerminal):
				self.grammarDictionary[nonTerminal] += [derivation]

			#Add the completely new derivation to the grammar dictionary
			else:
				self.grammarDictionary[nonTerminal] = [derivation]


		return self


	def getStartSymbol(self):
		return self.startSymbol

	def getGrammarDictionary(self):
		return self.grammarDictionary

	def __str__(self):
		return "Grammar Dictionary: " + str(self.grammarDictionary)

	def __repr__(self):
		self.__str__()


class terminalStringExplorer(object):

	def __init__(self):
		pass

	def explore(self, grammarRules, length):
		startSymbol = grammarRules.getStartSymbol()
		workList = deque([[startSymbol]])
		generatedSentences = []

		#Explore and print out all possible terminal sentences under the specified length
		while len(workList) != 0:

			sentence = workList.popleft()

			if len(sentence) > length:
				continue

			terminalSentence = True
			index = 0

			for element in sentence:

				#Check if there is a non terminal element in the sentence
				if grammarRules.getGrammarDictionary().has_key(element):
					terminalSentence = False
					firstNonTerminal = element
					break

				index += 1


			if terminalSentence == True:
				printStr = ""

				for element in sentence:
					printStr += element + " "

				print printStr

			else:

				for derivation in grammarRules.getGrammarDictionary()[firstNonTerminal]:

					temp = sentence[:index] + derivation + sentence[index+1:]
					
					if temp not in generatedSentences:
						generatedSentences.append(temp)
						workList.append(temp)

			#print str(workList) + '\n\n'

		

if __name__ == "__main__":

	length = int(raw_input("Length? "))
	fileName = raw_input("Filename: ")

	#Take input file and interpret grammar rules from it
	ruleMaker = RuleMaker(fileName)
	grammarRules = ruleMaker.generateGrammarRules()

	#Take the grammar rules and explore all the possibilities up to a certain length
	explorer = terminalStringExplorer()
	explorer.explore(grammarRules, length)



