import lexer_rules
import parser_rules

from sys import argv, exit
import sys

from ply.lex import lex
from ply.yacc import yacc

if __name__ == "__main__":
    if len(argv) != 3:
        print "Parametros invalidos."
        print "Uso:"
        print "traductor2.py archivo_entrada archivo_salida"
        exit()
    text = ""
    with open(argv[1], "r") as fp:
        for line in fp:
            text = line
	    break;
    	fp.close()
    output_file = open(argv[2], "w")

    try:
        lexer = lex(module=lexer_rules)
        parser = yacc(module=parser_rules)
        ast = parser.parse(text, lexer)
	ast.operate()
	translation = ast.translate()
        output_file.write(ast.translate())
    except Exception as e:
        print >>sys.stderr, "Error:\n" + str(e)
        exit(1)

    output_file.close()
