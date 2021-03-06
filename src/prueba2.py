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
#text = "({B^{C^F}}/{B^{C^F}})-D"
#text = "(A_{B_{D_R}}/A_{B_{D_R}})-I"
#text = "({A^B_C}/{A_B^C})"
#text = "({{A^B_C}^G}/{{A^B_C}^G})"
#text = "a(b^c)d"
#text = "(C/B)D"
#text = "ABCDKAKSJD"
#text = "(A_{B^C_D})"
#text = "(A/B/C/D)"
#
#text = "({a_b}/e_{b_{c_{d_e}}}^{e^{b^{c^{d^e}}}}/q12^{e^{b^{c^{d^e}}}})"
#text = "({a_b}/e_{b_{c_{d_e}}}^{e^{b^{c^{d^e}}}}/q12^{e^{b^{c^{d^e}}}}/{q*212+aNASD+12312+e^2_1})"
#text = "{a_b}/{e_{b_{c_{d_e}}}}"
#ext = "({a_b}/e_{b_{c_{d_e}}}^{e^{b^{c^{d^e}}}})"
#text = "(({a_b})/({e_{b_{c_{d_e}}}})/(q12^{e^{b^{c^{d^e}}}}))"
#text = "{a_b}/{e_b^c}"
#text = "(q12^{e^{b^{c^{d^{e^{e^{b^{c^{d^e}}}}}}}}})"
#text = "(A^{Basdasd}_{C123123123_{asdasdasd}})-I"
#text ="(1+1) / 2"
#text = "(A_{B_{D_{R_{B_{C_L}}}}})"
#text="{A_b^c}_d^e"
#text = "(A/B^{e^{e^e}})"
#text = "(({a_b}/e_{b_{c_{d_e}}}^{e^{b^{c^{d^e}}}})/(q12^{e^{b^{c^{d^e}}}}/{q*212+aNASD+12312+e^2_1}))"
#text = "(A)"
#text = "(({a_b})/({e_{b_{c_{d_e}}}})/(q12^{e^{b^{c^{d^{e^{e^{b^{c^{d^e}}}}}}}}}))"
#text = "(a/f/a/a/s/w/1/231/3/4/4/a/f)"

#text ="({(A/B)}{(A)}{(A/B/C)}{(A/B/C/D)}{(q12^{e^{b^{c^{d^e}}}}/{B/C/D/E/F/G/H})})"
#text = "A(({1/A}/{B/C/x})(2/D/E/F/y)(3/{G/H/I/z})(A)(A/B))+"
#text = "(A/B)"
#text = "({a_b})"
#text = "(q12^{e^{b^{c^{d^a}}}})"

#text = "{a_b}/{e_{b_{c_{d_e}}}}/q12^{e^{b^{c^{d^e}}}}"
#text = "(({a_b})/({e_{b_{c_{d_e}}}})/(q12^{e^{b^{c^{d^e}}}}))"
#text = "(q12^{e^{b^{c^{d^e}}}})"
#text = "(A/B)(A)(q12^{e^{b^{c^{d^e}}}})"
#text ="(a/b/c/b/f/f/d)"
#text = "(a/b/c)"
#text = "({1/A}/{B/C/x})"
#text = "a/vb/{c/c/s}/s/f"
#text = "c/{c/s}"
#text ="((a/{b})(a/{b/c})(a/{b/c/d}))"
#text = "(a^{a^{b^c}}_{a_{b_{c_{d_{f_{g}}}}}})"
#text = "((a^{a^{b^c}}_{a_{b_{c_{d_{f_{g}}}}}})(a_{a_{b_{c_{d_{f_{g}}}}}}^{a^{b^c}}))"
#text ="(({a_b}/e_{b_{c_{d_e}}}^{e^{b^{c^{d^e}}}})/(q12^{e^{b^{c^{d^e}}}}/{q*212+aNASD+12312+e^2_1}))/(({a_b}/e_{b_{c_{d_e}}}^{e^{b^{c^{d^e}}}})/(q12^{e^{b^{c^{d^e}}}}/{q*212+aNASD+12312+e^2_1}))
text = "((({a_b}/e_{b_{c_{d_e}}}^{e^{b^{c^{d^e}}}})/(q12^{e^{b^{c^{d^e}}}}/{q*212+aNASD+12312+e^2_1}))/({(A/B)}{(A)}{(A^B)}{(A/B)}{(A_B)}{(A/B/C)}{(A/B/C/D)}{(q12^{e^{b^{c^{d^e}}}}/{B/C/D/E/F/G/H})}))"
#text = "a_b"
#text ="({{1_2}_3}_4)(1_{2_{3_4}})"
#text ="1_{2_3}"
#text ="({a_b}_c)(1_{2_3})"
#text ="({{a}^c_b}^e_d)({{a}_b^c}_d^e)"
#text ="(a)"
#text = "(a^b)^c

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
