import lexer_rules
import parser_rules

from sys import argv, exit
import sys

from ply.lex import lex
from ply.yacc import yacc


testsAccept = ["abc", "abcd","a^c_d","{a_b}/(e_b^c)/q12"]
testsReject = ["a{","a_b_c", "1^2^3", "{", ")" ]
def testAceptar():
	result = True
	try:	
		for t in testsAccept:
			lexer = lex(module=lexer_rules)
			parser = yacc(module=parser_rules)
			ast = parser.parse(t, lexer)
			ast.operate()
			ast.translate()
	except Exception as e:
		result = False
	return result 
         
def testRechazar():
	result = False
	try:	
		for t in testsReject:
			lexer = lex(module=lexer_rules)
			parser = yacc(module=parser_rules)
			ast = parser.parse(t, lexer)
			ast.operate()
			ast.translate()
	except Exception as e:
		result = True
	return result 

def testPrecedencia():
	

if __name__ == "__main__":
	print "testAceptar"
 	result = testAceptar();
	print "testReject"
	result = result  and testRechazar();
	if result:
		print "Test superados con exito"
	else:
		print "No se superaron los tests"


