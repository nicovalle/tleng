tokens = [
	'SYMBOL',
	'LPARENT',
	'RPARENT',
	'LBRACKET',
	'RBRACKET',
	'DIVIDE',
	'CIRCUMFLEX',
	'UNDERSCORE'
]

t_LPARENT = r"\("
t_RPARENT = r"\)"
t_LBRACKET = r"\{"
t_RBRACKET = r"\}"
t_DIVIDE = r"\/"
t_CIRCUMFLEX = r"\^"
t_UNDERSCORE = r"\_"

def t_SYMBOL(token):
	r"[^\_\^\{\}\(\)\/]"
	return token

t_ignore = " \t\n"

def t_error(token):
    message = "Token desconocido:"
    message += "\ntype:" + token.type
    message += "\nvalue:" + str(token.value)
    message += "\nline:" + str(token.lineno)
    message += "\nposition:" + str(token.lexpos)
    raise Exception(message)
