
import re, sys, string

debug = False
dict = { }
tokens = [ ]




#================================================Objects==========================================================#

		#======================================Semantic Objects===============================================#


class StatementList( object ):
	def __init__(self):
		self.statementList = []

	def addStatement(self, statement):
		self.statementList.append(statement)

	def __str__(self):
		printStr = ''
		for statement in self.statementList:
			printStr += str(statement)
		return printStr

	def meaning(self, state):
		for statement in self.statementList:
			statement.meaning(state)

		return state


# Statement class and subclasses
class Statement( object ):
	def __str__(self):
		return ""

class Assignment( Statement ):
	def __init__(self, identifier, expression):
		self.identifier = identifier
		self.expression = expression
		
	def __str__(self):
		return "= " + str(self.identifier) + " " + str(self.expression) + "\n"

	def meaning(self, state):
		state[self.identifier] = self.expression.value(state)
		return state

class WhileStatement( Statement ):
	def __init__(self, expression, block):
		self.expression = expression
		self.block = block

	def __str__(self):
		return "while " + str(self.expression) + "\n" + str(self.block) + "endwhile\n"

	def meaning(self, state):
		while self.expression.value(state):
			self.block.meaning(state)

		return state


class IfStatement( Statement ):
	def __init__(self, expression, ifBlock, elseBlock):
		self.expression = expression
		self.ifBlock = ifBlock
		self.elseBlock = elseBlock

	def __str__(self):
		#The following string representation forces and else to be printed in the abstract sytax tree
		#even if there was no else in the input. I could fix this simply, but I am imitating the sample
		#output.
		return "if " + str(self.expression) + "\n" + str(self.ifBlock) + "else\n" + str(self.elseBlock) + "endif\n"

	def meaning(self, state):
		if self.expression.value(state):
			self.ifBlock.meaning(state)
		else:
			if self.elseBlock != '':
				self.elseBlock.meaning(state)
		return state


# Expression class and subclasses
class Expression( object ):
	def __str__(self):
		return "" 
	
class BinaryExpr( Expression ):
	def __init__(self, op, left, right):
		self.op = op
		self.left = left
		self.right = right
		
	def __str__(self):
		return str(self.op) + " " + str(self.left) + " " + str(self.right)

	def value(self, state):
		left = self.left.value(state)
		right = self.right.value(state)
		if self.op == "+":
			return left + right
		elif self.op == "-":
			return left - right
		elif self.op == "*":
			return left * right
		elif self.op == "/":
			return left / right
		elif self.op == ">":
			return left > right
		elif self.op == "<":
			return left < right
		elif self.op == ">=":
			return left >= right
		elif self.op == "<=":
			return left <= right
		elif self.op == "==":
			return left == right
		elif self.op == "!=":
			return left != right
		elif self.op == "and":
			return left and right
		elif self.op == "or":
			return left or right

class Number( Expression ):
	def __init__(self, value):
		self.val = value
		
	def __str__(self):
		return str(self.value)

	def value(self, state):
		return int(self.val)

class VarRef( Expression ):
	""""Variable Reference, in other words, an identifier."""
	def __init__(self, value):
		self.val = value

	def __str__(self):
		return str(self.value)

	def value(self, state):
		return state[self.val]


class String( Expression ):
	def __init__(self, value):
		self.val = value

	def __str__(self):
		return str(self.value)

	def value(self, state):
		return self.val




		#==================================Lexer Class===============================================#


# Lexer, a private class that represents lists of tokens from a Gee
# statement. This class provides the following to its clients:
#
#   o A constructor that takes a string representing a statement
#       as its only parameter, and that initializes a sequence with
#       the tokens from that string.
#
#   o peek, a parameterless message that returns the next token
#       from a token sequence. This returns the token as a string.
#       If there are no more tokens in the sequence, this message
#       returns None.
#
#   o removeToken, a parameterless message that removes the next
#       token from a token sequence.
#
#   o __str__, a parameterless message that returns a string representation
#       of a token sequence, so that token sequences can print nicely

class Lexer :
	
	
	# The constructor with some regular expressions that define Gee's lexical rules.
	# The constructor uses these expressions to split the input expression into
	# a list of substrings that match Gee tokens, and saves that list to be
	# doled out in response to future "peek" messages. The position in the
	# list at which to dole next is also saved for "nextToken" to use.
	
	special = r"\(|\)|\[|\]|,|:|;|@|~|;|\$"
	relational = "<=?|>=?|==?|!="
	arithmetic = "\+|\-|\*|/"
	#char = r"'."
	string = r"'[^']*'" + "|" + r'"[^"]*"'
	number = r"\-?\d+(?:\.\d+)?"
	literal = string + "|" + number
	#idStart = r"a-zA-Z"
	#idChar = idStart + r"0-9"
	#identifier = "[" + idStart + "][" + idChar + "]*"
	identifier = "[a-zA-Z]\w*"
	lexRules = literal + "|" + special + "|" + relational + "|" + arithmetic + "|" + identifier
	
	def __init__( self, text ) :
		self.tokens = re.findall( Lexer.lexRules, text )
		self.position = 0
		self.indent = [ 0 ]
	
	
	# The peek method. This just returns the token at the current position in the
	# list, or None if the current position is past the end of the list.
	
	def peek( self ) :
		if self.position < len(self.tokens) :
			return self.tokens[ self.position ]
		else :
			return None
	
	
	# The removeToken method. All this has to do is increment the token sequence's
	# position counter.
	
	def next( self ) :
		self.position = self.position + 1
		return self.peek( )

	#Rewinds the token position back to the beginning - to be used when done parsing and 
	#right before semantic evaluation begins.
	def rewind( self ):
		self.position = 0
	
	
	# An "__str__" method, so that token sequences print in a useful form.
	
	def __str__( self ) :
		return "<Lexer at " + str(self.position) + " in " + str(self.tokens) + ">"



#========================================Stand Alone Functions=========================================================#



# The "parse" function. This builds a list of tokens from the input string,
# and then hands it to a recursive descent parser for the PAL grammar.
# This is where the work is started after the tokens are loaded in correctly.
def parse( text ) :
	global tokens
	tokens = Lexer( text )
	stmtlist = parseStmtList( )
	#print (stmtlist)
	return stmtlist

def semanticState(statementList):
	state = {}
	state = statementList.meaning(state)
	print ("\n" + printState(state))
	return


	#======================================Statement Parsing Functions=================================#



def parseStmtList(  ):
	""" stmtList =  {  statement  } """
	tok = tokens.peek( )
	statementList = StatementList()

	while tok not in [None ,"~"]: #have to account for undent that signals an end of block

		statement = parseStatement()
		statementList.addStatement(statement)
		tok = tokens.peek()

	return statementList


def parseStatement():
	"""statement = ifStatement |  whileStatement  |  assign"""

	tok = tokens.peek()
	if debug: print ("Statement: ", tok)

	if tok == "if":
		return parseIfStatement()

	elif tok == "while":
		return parseWhileStatement()


	elif re.match(Lexer.identifier, tok):
		return parseAssign()


	error("Invalid Initial Statement Token (not an identifier, 'if', or 'while'.")
	return


def parseAssign():
	"""assign = ident "=" expression  eoln"""

	identifier = tokens.peek()
	if debug: print ("Assign statement: ", left)

	if tokens.next() != "=":
		error("Assignment does not have equal sign.")

	tokens.next()
	exp = expression()

	tok = tokens.peek()
	if tok != ";":
		error("Assignment did not end with an end of line.")

	tokens.next()

	return Assignment(identifier, exp)
	


def parseIfStatement():
	"""ifStatement = "if" expression block   [ "else" block ] """

	tok = tokens.next()
	if debug: print ("If statement: ", tok)

	expr = expression()
	ifBlock = parseBlock()
	elseBlock = ''

	if tokens.peek() == "else":
		tok = tokens.next()
		if debug: print ("Else statement: ", tok)
		elseBlock = parseBlock()

	return IfStatement(expr, ifBlock, elseBlock)


def parseWhileStatement():
	"""whileStatement = "while"  expression  block"""
	tok = tokens.next()
	if debug: print ("While statement: ", tok)

	expr = expression()
	block = parseBlock()

	return WhileStatement(expr, block)



def parseBlock():
	"""block = ":" eoln indent stmtList undent"""

	tok = tokens.peek()
	if debug: print ("Block: ", tok)
	
	# Check to make sure each of the appropriate terminal tokens exist and are in the right place
	if tok != ":":
		error("Block is missing ':' character.")

	tok = tokens.next()

	if tok != ";":
		error("Block is missing end of line character.")

	tok = tokens.next()

	if tok != "@":
		error("Block is not indented after end of line.")

	tok = tokens.next()

	stmtList = parseStmtList()

	if tokens.peek() != "~":
		error("Block is not undented after statements.")

	tokens.next()

	return stmtList



	#======================================Expression Parsing Functions=================================#

def expression():
	"""expression = andExpr { "or" andExpr }"""
	tok = tokens.peek( )
	if debug: print ("expression: ", tok)
	left = andExpr( )
	tok = tokens.peek( )
	while tok == "or":
		tokens.next()
		right = andExpr( )
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek( )
	return left


def andExpr():
	"""andExpr    = relationalExpr { "and" relationalExpr }"""
	tok = tokens.peek( )
	if debug: print ("andExpr: ", tok)
	left = relationalExpr( )
	tok = tokens.peek( )
	while tok == "and":
		tokens.next()
		right = relationalExpr( )
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek( )
	return left


def relationalExpr():
	"""relationalExpr = addExpr [ relation addExpr ]"""
	tok = tokens.peek( )
	if debug: print ("relationalExpr: ", tok)
	left = addExpr( )
	tok = tokens.peek( )
	while re.match(Lexer.relational, tok):
		tokens.next()
		right = addExpr( )
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek( )
	return left


def addExpr( ):
	""" addExpr    = term { ('+' | '-') term } """

	tok = tokens.peek( )
	if debug: print ("addExpr: ", tok)
	left = term( )
	tok = tokens.peek( )
	while tok == "+" or tok == "-":
		tokens.next()
		right = term( )
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek( )
	return left



def term( ):
	""" term    = factor { ('*' | '/') factor } """

	tok = tokens.peek( )
	if debug: print ("Term: ", tok)
	left = factor( )
	tok = tokens.peek( )
	while tok == "*" or tok == "/":
		tokens.next()
		right = factor( )
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek( )
	return left


def factor( ):
	"""factor  = number | string | ident |  "(" expression ")" """

	tok = tokens.peek( )

	if debug: print ("Factor: ", tok)

	if re.match(Lexer.number, tok):
		expr = Number(tok)
		tokens.next( )
		return expr

	elif re.match(Lexer.string, tok):
		expr = String(tok)
		tokens.next()
		return expr

	elif re.match(Lexer.identifier, tok):
		expr = VarRef(tok)
		tokens.next()
		return expr

	if tok == "(":
		tokens.next( )  # or match( tok )
		expr = expression( )
		tokens.peek( )
		tok = match(")")
		return expr

	error("Invalid operand")
	return




	#=======================================Suppor Methods========================================#


def match(matchtok):
	tok = tokens.peek( )
	if (tok != matchtok): error("Expecting "+ matchtok)
	tokens.next( )
	return tok

def error( msg ):
	#print msg
	sys.exit(msg)

def printState(stateDict):
	string = "{"
	for key, value in stateDict.items():
		string += "<" + str(key) + ", " + str(value) + ">, " 

	return string[:-2] + "}"



#======================================Main Function and File IO========================================#


def main():
	"""main program for testing"""
	global debug
	ct = 0
	for opt in sys.argv[1:]:
		if opt[0] != "-": break
		ct = ct + 1
		if opt == "-d": debug = True
	if len(sys.argv) < 2+ct:
		print ("Usage:  %s filename" % sys.argv[0])
		return
	statements = parse("".join(mklines(sys.argv[1+ct])))
	semanticState(statements)
	return


def mklines(filename):
	"""Helper funciton to read in lines of given file in appropriate format."""
	inn = open(filename, "r")
	lines = [ ]
	pos = [0]
	ct = 0
	for line in inn:
		#Added in to print out original file as per semantic project spec
		print (line, end = "")
		ct += 1
		line = line.rstrip( )+";"
		line = delComment(line)
		if len(line) == 0 or line == ";": continue
		indent = chkIndent(line)
		line = line.lstrip( )
		if indent > pos[-1]:
			pos.append(indent)
			line = '@' + line
		elif indent < pos[-1]:
			while indent < pos[-1]:
				del(pos[-1])
				line = '~' + line
		#Uncomment the print below to display the input as in the last project
		#print (ct, "\t", line)
		lines.append(line)
	# print len(pos)
	undent = ""
	for i in pos[1:]:
		undent += "~"
	lines.append(undent)
	# print undent
	return lines


def chkIndent(line):
	ct = 0
	for ch in line:
		if ch != " ": return ct
		ct += 1
	return ct
		

def delComment(line):
	pos = line.find("#")
	if pos > -1:
		line = line[0:pos]
		line = line.rstrip()
	return line


main()
