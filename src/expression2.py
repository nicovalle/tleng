def scale(node, scale):
	node.scale = scale
	node.height = node.height * scale
	node.hlow = node.hlow * scale
	node.hup = node.hup * scale
	node.width = node.width * scale

def moveY(node, y):
	node.y += y
	for c in node.children:
		moveY(c, y)

def moveX(node, x):
	node.x += x
	for c in node.children:
		moveX(c, x)

def printY(node):
	print node.name(), node.y
	for c in node.children:
		printY(c)

def getMaxY(node):
	result = node.y
	for c in node.children:
		childrenY = getMaxY(c)
		result = max(childrenY, result) 

	return result

def getMinY(node):
	result = node.y
	for c in node.children:
		childrenY = getMinY(c)
		result = min(childrenY, result) 

	return result

def getMinYNode(node):
	result = node
	for c in node.children:
		childrenY = getMinYNode(c)
		if result.y > childrenY.y:
			result = childrenY
	return result

def getMaxYNode(node):
	result = node
	for c in node.children:
		childrenY = getMaxYNode(c)
		if result.y <= childrenY.y:
			result = childrenY

	return result

class Start(object):
	def __init__(self, child):
		self.child = child
		self.x = 0
		self.y = 1
		self.scale = 1
		self.hlow = 0.2
		self.hup = 0.8
		self.children = [child]

	def name(self):
		return self.child.name()

	def operate(self):
		scale(self.child, self.scale)
		self.child.x = self.x
		self.child.y = self.y
		self.child.operate()
		self.hlow = self.child.hlow
		self.hup = self.child.hup

	def translate(self):
		self.translation =  '<?xml version="1.0" standalone="no"?>\n'
		self.translation += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n'
		self.translation += '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
		self.translation += '<svg xmlns="http://www.w3.org/2000/svg" version="1.1">\n'
		self.translation += '<g transform="translate(20,' + str((self.hup - self.y + 2) * 75) + ') scale(75)" font-family="Courier">\n'
		self.translation += self.child.translate()
		self.translation +='</g>\n'
		self.translation += '</svg>'
		return self.translation

class Divide(object):
	def __init__(self, left, right):
		self.left = left
		self.right = right
		self.width  = 0.6
		self.height = 1
		self.x = 0
		self.y = 0
		self.scale = 1
		self.hlow = 0.2
		self.hup = 0.8
		self.children = [left, right]

	def name(self):

		return self.left.name() + "/" + self.right.name()

	def operate(self):
		#primero escalamos los nodos hijos

		scale(self.left, self.scale)
		scale(self.right, self.scale)
		
		#seteamos las primeras posiciones para los nodos hijos y computamos sus atributos
		self.left.x = self.x
		self.left.y = self.y 
		self.right.x = self.x
		self.right.y = self.y
		self.left.operate()
		self.right.operate()
		
		#actualizamos el ht y el dp del nodo
		
		self.hup = self.left.height + 0.40
		self.hlow = self.right.height+ 0.28
		
		#la anchura es la maxima anchura de los hijos
		self.width = max(self.left.width, self.right.width)

		#reubicamos el numerador por arriba de la linea de division, tanto como se haya pasado y un poco mas
		moveY(self.left, -self.left.hlow - 0.50 * self.scale)
		
		#reubicamos el denominador por debajo de la linea de division
		moveY(self.right, self.right.hup + 0.28*self.scale)

		#calculamos al altura del nodo
		self.height = self.hlow + self.hup

		#calculamos el centro de la division y centramos los nodos hijos
		center = (self.x + (self.x + self.width))/2
		rightCenter = (self.right.x + (self.right.x + self.right.width))/2
		leftCenter = (self.left.x + (self.left.x + self.left.width))/2
		moveX(self.left, abs(leftCenter - center))
		moveX(self.right, abs(rightCenter - center))


			
		
	def translate(self):
		#traducimos el numerador
		self.translation = self.left.translate()

		#pintamos la linea de division
		self.translation += '\t<line x1="' + str(self.x) + '" y1="' + str(self.y - 0.28 * self.scale) + '" '
		self.translation += 'x2="' + str(self.x + self.width) +'" y2="' + str(self.y -  0.28 * self.scale) + '" '
		self.translation +='stroke-width="0.03" stroke="black"/>\n'
		
		#finalmente traducimos el denominador
		self.translation += self.right.translate()
		return self.translation



class Concat(object):
	def __init__(self, left, right):
		self.scale = 1
		self.height = 1
		self.left = left
		self.right = right
		self.x = 0
		self.y = 0
		self.width = 0.6
		self.hlow = 0.2
		self.hup = 0.8
		self.children = [left, right]
		

	def name(self):
		return self.left.name() + " " + self.right.name()

	def operate(self):
		#escalamos los nodos hijos
		scale(self.left, self.scale)
		scale(self.right, self.scale)
		#seteamos la posicion de los nodos hijo mas a la izquierda y computamos sus atributos.
		self.left.x = self.x
		self.left.y = self.y
		self.left.operate()

		#seteamos la posicion del nodo derecho, teniendo en cuenta que debe ubicarse luego del izquierdo,
		#y computamos sus atributos
		self.right.x = self.left.x + self.left.width
		self.right.y = self.y
		self.right.operate()

		#la anchura del nodo es la suma de las anchuras de los nodos hijos
		self.width = self.left.width + self.right.width

		#actualizamos ht y dp y con ellos calculamos la altura del nodo
		self.hlow = max(self.left.hlow, self.right.hlow)
		self.hup = max(self.left.hup, self.right.hup)
		self.height = self.hlow + self.hup
		

	def translate(self):
		#traducimos el hijo izquierdo y a continuacion el hijo derecho
		self.translation = self.left.translate() + self.right.translate()
		return self.translation

class Underscore(object):
	def __init__(self, left, right):
		self.x = 0
		self.y = 0
		self.left = left
		self.right = right
		self.height = 1
		self.scale = 1
		self.width = 0.6
		self.hlow = 0.2
		self.hup = 0.8
		self.children = [left, right]
		

	def name(self):
		return self.left.name() + "_" + self.right.name()

	def operate(self):
		scale(self.left, self.scale)
		scale(self.right,self.scale * 0.7)
		self.left.x = self.x
		self.left.y = self.y
		self.left.operate()
		self.right.x = self.x + self.left.width
		self.right.y = self.y + (0.25 * self.scale)
		self.right.operate()
		self.hup = max(self.left.hup, self.right.hup - 0.25 * self.scale)
		self.hlow = max(self.left.hlow, self.right.hlow + 0.25 * self.scale)
		self.width = self.left.width + self.right.width
		self.height = self.hlow + self.hup
		
	def translate(self):
		self.translation = self.left.translate()
		self.translation += self.right.translate()
		return self.translation

class Circumflex(object):
	def __init__(self, left, right):
		self.left = left
		self.right = right
		self.scale = 1
		self.height = 1
		self.x = 0
		self.y = 0
		self.width = 0.6
		self.hlow = 0.2
		self.hup = 0.8
		self.children = [left, right]

	def name(self):
		return self.left.name() + "^" + self.right.name()

	def operate(self):
		scale(self.left, self.scale)
		scale(self.right, self.scale * 0.7)
		self.left.x = self.x
		self.left.y = self.y
		self.left.operate()
		self.right.x = self.x + self.left.width
		self.right.y = self.y - (0.45 * self.scale)
		self.right.operate()
		self.hup = max(self.left.hup, self.right.hup + 0.45 * self.scale)
		self.hlow = max(self.left.hlow, self.right.hlow - 0.45 * self.scale)
		self.width = self.left.width + self.right.width
		self.height = self.hlow + self.hup
	
	def translate(self):
		self.translation = self.left.translate()
		self.translation += self.right.translate()
		return self.translation

class CircumflexUnder(object):
	def __init__(self, first, second, third):
		self.scale = 1
		self.x = 0
		self.y = 0
		self.width = 0.6
		self.height = 1
		self.hlow = 0.2
		self.hup = 0.8
		self.first = first
		self.second = second
		self.third = third
		self.children = [first, second, third]

	def name(self):
		return self.first.name() + "^" + self.second.name() + "_" + self.third.name()

	def operate(self):
		scale(self.first, self.scale)
		scale(self.second, self.scale * 0.7)
		scale(self.third, self.scale * 0.7)
		self.first.x = self.x
		self.first.y = self.y
		self.first.operate()
		self.second.x = self.x + self.first.width
		self.second.y = self.y - (0.45 * self.scale)
		self.third.x = self.x + self.first.width
		self.third.y = + self.y + (0.25 * self.scale)
		self.second.operate()
		self.third.operate()
		self.hup = max(max(self.first.hup, self.second.hup + 0.45 * self.scale), self.third.hup - 0.25 * self.scale)
		self.hlow = max(max(self.first.hlow, self.second.hlow - 0.45 * self.scale), self.third.hlow + 0.25*self.scale)
		self.width = self.first.width + max(self.second.width, self.third.width)
		self.height = self.hup + self.hlow

	def translate(self):
		self.translation = self.first.translate()
		self.translation += self.second.translate()
		self.translation += self.third.translate()
		return self.translation


class UnderCircumflex(object):
	def __init__(self, first, second, third):
		self.scale = 1
		self.x = 0
		self.y = 0
		self.width = 0.6
		self.height = 1
		self.hlow = 0.2
		self.hup = 0.8
		self.first = first
		self.second = second
		self.third = third
		self.children = [first, second, third]

	def name(self):
		return self.first.name() + "_" + self.second.name() + "^" + self.third.name()

	def operate(self):
		scale(self.first, self.scale)
		scale(self.second, self.scale * 0.7)
		scale(self.third, self.scale * 0.7)
		self.first.x = self.x
		self.first.y = self.y
		self.first.operate()
		self.third.x = self.x + self.first.width
		self.third.y = self.y - (0.45 * self.scale)
		self.second.x = self.x + self.first.width
		self.second.y = + self.y + (0.25 * self.scale)
		self.second.operate()
		self.third.operate()
		self.hup = max(max(self.first.hup, self.third.hup + 0.45 * self.scale), self.second.hup - 0.25 * self.scale)
		self.hlow = max(max(self.first.hlow, self.third.hlow - 0.45 * self.scale), self.second.hlow + 0.25*self.scale)	
		self.width = self.first.width + max(self.second.width, self.third.width)
		self.height = self.hup + self.hlow

	def translate(self):
		self.translation = self.first.translate()
		self.translation += self.second.translate()
		self.translation += self.third.translate()
		return self.translation		

class Parenthesis(object):
	def __init__(self, child):
		self.scale = 1
		self.x = 0
		self.y = 0
		self.width = 0.6
		self.height = 1
		self.hlow = 0.2
		self.hup = 0.8
		self.child = child
		self.children = [child]
		
	def name(self):
		return "(" + self.child.name() + ")"

	def operate(self):
		#escalamos el nodo hijo
		scale(self.child, self.scale)

		#horizontalmente movemos el nodo hijo para dejar lugar al parentesis que abre
		#la posicion vertical del hijo es la del nodo
		self.child.x = self.x + self.scale * 0.6
		self.child.y = self.y

		#computamos los atributos del nodo hijo
		self.child.operate()

		#la anchura del nodo es la del hijo 
		#mas el ancho del parentesis que abre mas el ancho del parentesis que cierra
		self.width = self.child.width + (2 * self.scale * 0.6)

		#actualizamos los ht y dp y la altura del nodo
		self.hlow = self.child.hlow
		self.hup = self.child.hup
		self.height = self.hlow + self.hup

	def translate(self):
		#escala es un valor que se utiliza para escalar los parentesis de manera tal que cubran toda la formula 
		#y para reubicarlos. se lo divide por self.scale para contrarrestar el efecto del font-size al transformar
		escala = self.height * 1.33 / self.scale
		self.translation = '\t<text x="0" y="0" font-size="' + str(self.scale) + '" transform="'

		#se escribe el parentesis que abre.
		#verticalmente se ubica un poco por encima de donde empieza el nodo hijo,
		#dado que el simbolo de parentesis se escribe un poco por debajo en la fuente elegida
		#se lo escala por el valor escala calculado
		self.translation += 'translate(' + str(self.x) + ',' + str(self.y + self.hlow - 0.18 * escala) + ') scale(1,' + str(escala) + ')">(</text>\n'
		
		#traducimos el nodo hijo
		self.translation += self.child.translate()

		#escribimos el parentesis que cierra.
		#idem al partentesis  que abre,
		# con la excepcion de que verticalmente aparece mas a la derecha tanto como anchura tenga el nodo hijo
		self.translation += '\t<text x="0" y="0" font-size="' + str(self.scale) + '" transform="'
		self.translation += 'translate(' + str(self.x + self.child.width + self.scale * 0.6) + ',' + str(self.y + self.hlow - 0.18 * escala) + ') scale(1,'+ str(escala) +')">)</text>\n'
		return self.translation

class Symbol(object):
	def __init__(self, value):
		self.value = value
		self.scale = 1
		self.width = 0.6
		self.height = 1
		self.hlow = 0.2
		self.hup = 0.8
		self.x = 0
		self.y = 0
		self.children = []

	def name(self):
		return str(self.value)

	def operate(self):
		# no hay ningun calculo de atributos para hacer, ya que es una hoja del ast
		pass

	def translate(self):
		return '\t<text x="' + str(self.x) + '" y="' + str(self.y) +'" font-size="' + str(self.scale) + '">' + str(self.value) + '</text>\n'
