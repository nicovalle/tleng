import lexer_rules
import parser_rules

from sys import argv, exit
import sys

from ply.lex import lex
from ply.yacc import yacc


testsAccept = ["abc","{a^c_d}{a_d^c}","((a_b)/(e_b^c)/(A + B))", "((a^(1/2/3)_(b/c))(a^(b/c)_(1/2/3)))", "(A^BC^D/E^F_G+H)-I", "(a^({(b+c)}/d)_(b+c))", "(({{1_2}_3}_4)(1_{2_{3_4}})({{1^2}^3}^4)(1^{2^{3^4}}))", "({2*(A^2+X_i+X_{i+2}^3-4^{(3/2)*Y^5_j}+(25/133))}/{5*b^{3^2}})"]
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

if __name__ == "__main__":
	print "testAceptar"
 	result = testAceptar();
	print "testReject"
	result = result  and testRechazar();
	if result:
		print "Test superados con exito"
	else:
		print "No se superaron los tests"


