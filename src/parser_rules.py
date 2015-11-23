from lexer_rules import tokens 
from expressions import Divide, Concat, Underscore, Circumflex, CircumflexUnder, UnderCircumflex, Parenthesis, Symbol

def p_start_expression(subexpressions):
	'start : expression'
	subexpressions[0] = subexpressions[1]
	
def p_expression_divide(subexpressions):
	'expression : expression DIVIDE term'
	subexpressions[0] = Divide(subexpressions[1], subexpressions[3])

def p_expression_term(subexpressions):
	'expression : term'
	subexpressions[0] = subexpressions[1]

def p_term_concat(subexpressions):
	'term : term factor'
	subexpressions[0] = Concat(subexpressions[1], subexpressions[2])

def p_term_factor(subexpressions):
	'term : factor'
	subexpressions[0] = subexpressions[1]

def p_factor_g(subexpressions):
	'factor : g'
	subexpressions[0] = subexpressions[1]

def p_factor_g_under_g(subexpressions):
	'factor : g UNDERSCORE g'
	subexpressions[0] = Underscore(subexpressions[1], subexpressions[3])

def p_factor_g_circum_g(subexpressions):
	'factor : g CIRCUMFLEX g'
	subexpressions[0] = Circumflex(subexpressions[1], subexpressions[3])

def p_factor_g_circum_g_under_g(subexpressions):
	'factor : g CIRCUMFLEX g UNDERSCORE g'
	subexpressions[0] = CircumflexUnder(subexpressions[1], subexpressions[3], subexpressions[5])

def p_factor_g_under_g_circum_g(subexpressions):
	'factor : g UNDERSCORE g CIRCUMFLEX g'
	subexpressions[0] = UnderCircumflex(subexpressions[1], subexpressions[3], subexpressions[5])

def p_g_bracket_expression(subexpressions):
	'g : LBRACKET expression RBRACKET'
	subexpressions[0] = subexpressions[2]

def p_g_parenthesis_expression(subexpressions):
	'g : LPARENT expression RPARENT'
	subexpressions[0] = Parenthesis(subexpressions[2])	

def p_g_symbol(subexpressions):
	'g : SYMBOL'
	subexpressions[0] = Symbol(subexpressions[1])

def p_error(subexpressions):
    raise Exception("Syntax error.")