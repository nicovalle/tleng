import lexer_rules
import parser_rules

from ply.lex import lex
from ply.yacc import yacc

lexer = lex(module=lexer_rules)

parser = yacc(module=parser_rules)

#text = "(5^{D_{BC}^{ATGDGJ}}_{t_{gv}^{xyz}})"
#text = "asc"
#text = "(A_{B_{C_D}})"
#text = "(C_{D_{E_{F_G}}})"
#text = "(C_D)"
text ="(C_{D_E})"
text ="(C_{D_{E_F}})"
text = "({B^{C^F}}/{B^{C^F}})-D"
text = "(A_{B_{D_R}}/A^{B^{D^R}})-I"
#text = "({A^B_C}/{A_B^C})"
#text = "({{A^B_C}^G}/{{A^B_C}^G})"
#text = "a(bc)d"
#text = "(C/B)D"
#text = "ABCDKAKSJD"
#text = "(A_{B^C_D})"
text = "(A/B)"


ast = parser.parse(text, lexer)

def dump_ast(ast, output_file):
    output_file.write("digraph {\n")
    
    edges = []
    queue = [ast]
    numbers = {ast: 1}
    current_number = 2
    while len(queue) > 0:
        node = queue.pop(0)
        name = node.name()
        number = numbers[node]
        output_file.write('node[width=1.5, height=1.5, shape="circle", label="%s"] n%d;\n' % (name, number))
        for child in node.children():
            numbers[child] = current_number
            edge = 'n%d -> n%d;\n' % (number, current_number)
            edges.append(edge)
            queue.append(child)
            current_number += 1

    output_file.write("".join(edges))

    output_file.write("}")

output_file = open("nico.svg", "w")
ast.operate()
output_file.write(ast.translate())
output_file.close()
