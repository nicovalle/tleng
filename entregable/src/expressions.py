#constantes que se utilizan para inicializar atributos
DEFAULT_SCALE = 1
DEFAULT_HT = 0.8
DEFAULT_DP = 0.2
DEFAULT_X = 0
DEFAULT_Y = 0
DEFAULT_HEIGHT = 1
DEFAULT_WIDTH = 0.6

#funcion que escala el nodo pasa por parametro por el scale indicado
def scale(node, scale):
	node.scale = scale
	node.height = node.height * scale
	node.dp = node.dp * scale
	node.ht = node.ht * scale
	node.width = node.width * scale
	node.minHScale = node.minHScale * scale
	node.minLScale = node.minLScale * scale

#funcion que mueve verticalmente un nodo y todos sus nodos hijos
def moveY(node, y):
	node.y += y
	node.minY += y
	node.maxY += y
	for c in node.children:
		moveY(c, y)

#funcion que mueve horizontalmente un nodo y todos sus nodos hijos
def moveX(node, x):
	node.x += x
	for c in node.children:
		moveX(c, x)

class Start(object):
	def __init__(self, child):
		self.child = child
		self.x = DEFAULT_X
		self.y = 1
		self.scale = DEFAULT_SCALE
		self.dp = DEFAULT_DP
		self.ht = DEFAULT_HT
		self.height = DEFAULT_HEIGHT
		self.minY = 1
		self.maxY = 1
		self.minHScale = DEFAULT_SCALE
		self.minLScale = DEFAULT_SCALE
		self.children = [child]

	#para debugging
	def name(self):
		return self.child.name()

	def operate(self):
		#escalamos el nodo hijo
		scale(self.child, self.scale)

		#seteamos las posiciones del nodo hijo 
		#en este caso se corresponden con la del nodo padre

		self.child.x = self.x
		self.child.y = self.y

		#computamos los atributos del nodo hijo

		self.child.operate()

		#el ht y el dp se corresponden con el del nodo hijo

		self.dp = self.child.dp
		self.ht = self.child.ht

		#ht + dp dan la altura del nodo

		self.height = self.dp + self.ht

	def translate(self):

		#escribimos el header del svg

		self.translation =  '<?xml version="1.0" standalone="no"?>\n'
		self.translation += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n'
		self.translation += '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
		self.translation += '<svg xmlns="http://www.w3.org/2000/svg" version="1.1">\n'

		#bajamos tanto como necesitemos la formula para que se vea por completo en pantalla
		#el scale es arbitrario, suficiente para 
		#visualizar correctamente la formula sin agrandarla demasiado

		self.translation += '<g transform="translate(20,' + str((self.ht-self.y + 3) * 15) + ') scale(15)" font-family="Courier">\n'
		
		#traducimos el nodo hijo

		self.translation += self.child.translate()

		#cerramos el grupo

		self.translation +='</g>\n'
		self.translation += '</svg>'
		return self.translation

class Divide(object):
	def __init__(self, left, right):
		self.left = left
		self.right = right
		self.width  = DEFAULT_WIDTH
		self.height = DEFAULT_HEIGHT
		self.x = DEFAULT_X
		self.y = DEFAULT_Y
		self.scale = DEFAULT_SCALE
		self.dp = DEFAULT_DP
		self.ht = DEFAULT_HT
		self.minY = 1
		self.maxY = 1
		self.minHScale = DEFAULT_SCALE
		self.minLScale = DEFAULT_SCALE
		self.children = [left, right]

	#para debugging
	def name(self):

		return self.left.name() + "/" + self.right.name()

	def operate(self):

		#primero escalamos los nodos hijos
		#en este caso las escalas se mantienen en los nodos hijos

		scale(self.left, self.scale)
		scale(self.right, self.scale)
		
		#seteamos las primeras posiciones para los nodos hijos
		#inicialmente son las del nodo padre,
		#luego se moveran los nodos donde corresponda

		self.left.x = self.x
		self.left.y = self.y 
		self.right.x = self.x
		self.right.y = self.y

		#computamos los atributos de los nodos hijos

		self.left.operate()
		self.right.operate()
		
		#actualizamos el ht y el dp del nodo
		#el ht del nodo es la altura del numerador mas 
		#aproximadamente un 40% mas de la escala 
		#pues debe estar arriba de la linea de division

		self.ht = self.left.height + 0.40 * self.scale

		#el dp del nodo depende de la altura del denominador mas
		#aproximamente un 28% de la escala puesto que 
		#debe estar debajo de la linea de division

		self.dp = self.right.height + 0.28 * self.scale
		
		#la anchura es la maxima anchura de los hijos

		self.width = max(self.left.width, self.right.width)

		#reubicamos el numerador por arriba de la linea de division,
		#tanto como se haya pasado y un poco mas

		moveY(self.left, -self.left.dp - 0.50 * self.scale)
		
		#reubicamos el denominador por debajo de la linea de division

		moveY(self.right, self.right.ht + 0.28*self.scale)

		#calculamos al altura del nodo
		self.height = self.dp + self.ht

		#calculamos el centro de la division y centramos los nodos hijos
		#calculo el centro del nodo

		center = (self.x + (self.x + self.width))/2

		#calculo el centro del denominador

		rightCenter = (self.right.x + (self.right.x + self.right.width))/2

		#calculo el centro del numerador

		leftCenter = (self.left.x + (self.left.x + self.left.width))/2

		#movemos horizontalmente al numerador y al denominador
		#por la distancia que separa a sus centros del centro del nodo padre

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
		self.scale = DEFAULT_SCALE
		self.height = DEFAULT_HEIGHT
		self.left = left
		self.right = right
		self.x = DEFAULT_X
		self.y = DEFAULT_Y
		self.width = DEFAULT_WIDTH
		self.dp = DEFAULT_DP
		self.ht = DEFAULT_HT
		self.minY = 1
		self.maxY = 1
		self.minHScale = DEFAULT_SCALE
		self.minLScale = DEFAULT_SCALE
		self.children = [left, right]
		
	#para debugging
	def name(self):
		return self.left.name() + " " + self.right.name()

	def operate(self):

		#escalamos los nodos hijos
		#las escalas son las del nodo padre

		scale(self.left, self.scale)
		scale(self.right, self.scale)

		#seteamos la posicion de los nodos hijo 
		#mas a la izquierda y computamos sus atributos.

		self.left.x = self.x
		self.left.y = self.y
		self.left.operate()

		#seteamos la posicion del nodo derecho, 
		#teniendo en cuenta que debe ubicarse luego del izquierdo,
		#y computamos sus atributos

		self.right.x = self.left.x + self.left.width
		self.right.y = self.y
		self.right.operate()

		#la anchura del nodo es la suma de las anchuras de los nodos hijos

		self.width = self.left.width + self.right.width

		#actualizamos ht y dp y con ellos calculamos la altura del nodo
		#el dp y el ht corresponde a los mayores dp y ht hallados en los hijos

		self.dp = max(self.left.dp, self.right.dp)
		self.ht = max(self.left.ht, self.right.ht)
		self.height = self.dp + self.ht
		

	def translate(self):

		#traducimos el hijo izquierdo y a continuacion el hijo derecho

		self.translation = self.left.translate() + self.right.translate()
		return self.translation

class Underscore(object):
	def __init__(self, left, right):
		self.x = DEFAULT_X
		self.y = DEFAULT_Y
		self.left = left
		self.right = right
		self.height = DEFAULT_HEIGHT
		self.scale = DEFAULT_SCALE
		self.width = DEFAULT_WIDTH
		self.dp = DEFAULT_DP
		self.ht = DEFAULT_HT
		self.minY = 1
		self.maxY = 1
		self.minHScale = DEFAULT_SCALE
		self.minLScale = DEFAULT_SCALE
		self.children = [left, right]
		
	#para debugging
	def name(self):
		return self.left.name() + "_" + self.right.name()

	def operate(self):

		#escalamos el nodo raiz

		scale(self.left, self.scale)

		#seteamos la posicion del nodo hijo raiz
		#corresponde con la posicion calculada para el nodo padre
		#y calculamos sus atributos

		self.left.x = self.x
		self.left.y = self.y
		self.left.operate()

		#escalo el subindice a partir del menor 
		#tamanio encontrado en el nodo raiz

		scale(self.right,self.left.minHScale * 0.7)

		#computo sus atributos del nodo indice
		#para la posicion vertical hago uso del mayor 'y' 
		#que puede encontrar en el nodo raiz
		#y lo bajo un poco mas de acuerdo al menor 
		#tamanio hallado en el nodo raiz y al ht del indice

		self.right.x = self.x + self.left.width
		self.right.operate()
		moveY(self.right, self.left.maxY + self.right.ht)

		#actualizamos dp, height, width, maxY, minHScale con lo que calculamos del nodo hijo
		#el ht no cambia, porque la formula crece para "abajo"
		#el dp corresponde al de la raiz mas la altura del indice 
		#menos aproximadamente un 25% de la minima escala encontrada en la raiz
		#para no bajar demasiado el indice

		self.dp = self.left.dp + self.right.height - 0.25 * self.left.minHScale

		#el maximo 'y' ahora corresponde al maximo 'y' del indice
		#la minima escala tambien corresponde con la minima escala del indice

		self.maxY = self.right.maxY
		self.minHScale = self.right.minHScale

		#el ancho es la suma de los anchos de la raiz y del indice

		self.width = self.left.width + self.right.width
		self.height = self.dp + self.ht
		
	def translate(self):

		#primero traducimos el nodo raiz y a continuacion el subindice

		self.translation = self.left.translate()
		self.translation += self.right.translate()
		return self.translation

class Circumflex(object):
	def __init__(self, left, right):
		self.left = left
		self.right = right
		self.scale = DEFAULT_SCALE
		self.height = DEFAULT_HEIGHT
		self.x = DEFAULT_X
		self.y = DEFAULT_Y
		self.width = DEFAULT_WIDTH
		self.dp = DEFAULT_DP
		self.ht = DEFAULT_HT
		self.minY = 1
		self.maxY = 1
		self.minHScale = DEFAULT_SCALE
		self.minLScale = DEFAULT_SCALE
		self.children = [left, right]

	#para debugging
	def name(self):
		return self.left.name() + "^" + self.right.name()

	def operate(self):

		#escalamos el nodo raiz
		scale(self.left, self.scale)

		#seteamos la posicion del nodo hijo raiz
		#la posicion es la del nodo padre
		#y calculamos sus atributos

		self.left.x = self.x
		self.left.y = self.y
		self.left.operate()

		#escalo el superindice a partir del menor tamanio encontrado en el nodo raiz

		scale(self.right,self.left.minLScale * 0.7)
		
		#seteo las posiciones del superindice y computo sus atributos

		self.right.x = self.x + self.left.width
		self.right.operate()

		#para la posicion vertical hago uso del menor 'y' 
		#que pude encontrar en el nodo raiz
		#y lo subo un poco mas de acuerdo 
		#al menor tamanio hallado en el nodo raiz y
		#y de acuerdo a cuanto se pasa por debajo 
		#de linea de base del superindice que aparece mas arriba

		moveY(self.right, self.left.minY  - self.right.dp - (0.45 * self.left.minLScale))


		#actualizamos ht, height, width, maxY, minHScale 
		#con lo que calculamos del nodo hijo
		#el dp no hace falta modificarlo puesto que la formula crece para "arriba"
		#el ht es el de la raiz mas altura del superindice menos
		#aproximadamente un 30% del la minima escala para superindices hallada

		self.ht = self.left.ht + self.right.height - 0.30 * self.left.minLScale
		
		#el minimo 'y' es el del superindice
		
		self.minY = self.right.minY
		
		#la minima escala es la del superindice
		
		self.minLScale = self.right.minLScale
		
		#el ancho es la suma de los anchos de la raiz y del superindice
		
		self.width = self.left.width + self.right.width
		self.height = self.dp + self.ht
	
	def translate(self):
		
		#primero traducimos el nodo raiz y a continuacion el superindice
		
		self.translation = self.left.translate()
		self.translation += self.right.translate()
		return self.translation

class CircumflexUnder(object):
	def __init__(self, first, second, third):
		self.scale = DEFAULT_SCALE
		self.x = DEFAULT_X
		self.y = DEFAULT_Y
		self.width = DEFAULT_WIDTH
		self.height = DEFAULT_HEIGHT
		self.dp = DEFAULT_DP
		self.ht = DEFAULT_HT
		self.minY = 1
		self.maxY = 1
		self.minHScale = DEFAULT_SCALE
		self.minLScale = DEFAULT_SCALE
		self.first = first
		self.second = second
		self.third = third
		self.children = [first, second, third]

	#para debugging
	def name(self):
		return self.first.name() + "^" + self.second.name() + "_" + self.third.name()

	def operate(self):
		
		#escalamos el nodo raiz
		
		scale(self.first, self.scale)

		#seteamos la posicion del nodo hijo raiz
		#la posicion se corresponde con la del nodo padre
		#y calculamos sus atributos
		
		self.first.x = self.x
		self.first.y = self.y
		self.first.operate()

		#escalo el superindice a partir del menor 
		#tamanio encontrado de superindices en el nodo raiz
		#escalo el subindice a partir del menor 
		#tamanio encontrado de subindices en el nodo raiz

		scale(self.second, self.first.minLScale * 0.7)
		scale(self.third, self.first.minHScale * 0.7)

		#seteo las posiciones del superindice y del subindice y computo sus atributos
		#luego del computo se moveran verticalmente como corresponda

		self.second.x = self.x + self.first.width
		self.third.x = self.x + self.first.width
		self.second.operate()
		self.third.operate()
		
		#para la posicion vertical del superindice hago uso del menor 'y' 
		#que pude encontrar en el nodo raiz
		#y lo subo un poco mas de acuerdo al menor tamanio 
		#hallado para superindices en el nodo raiz y
		#y de acuerdo a cuanto se pasa por debajo de la 
		#linea de base del superindice que aparece mas arriba
		#para la posicion vertical del subindice hago uso del mayor 'y' 
		#que puede encontrar en el nodo raiz
		#y lo bajo un poco mas de acuerdo al menor tamanio 
		#hallado para subindices en el nodo raiz y al ht del indice

		moveY(self.second, self.first.minY  - self.second.dp - (0.45 * self.first.minLScale))
		moveY(self.third, self.first.maxY + self.third.ht)

		#actualizamos ht, dp, height, width, maxY, minHScale, minY, minLScale 
		#con lo que calculamos de los nodos hijos
		#el ht es el de la raiz mas la altura del superindice menos
		#aproximadamente un 30% del la minima escala para superindices hallada

		self.ht = self.first.ht + self.second.height - 0.30 * self.first.minLScale

		#el dp corresponde al de la raiz mas la altura del subindice 
		#menos aproximadamente un 25% de la minima 
		#escala para subindices encontrada en la raiz
		
		self.dp = self.first.dp + self.third.height - 0.25 * self.first.minHScale
		
		#el minimo 'y' es el del superindice
		
		self.minY = self.second.minY
		
		#la minima escala para superindices es la minima 
		#escala hallada en el superindice
		
		self.minLScale = self.second.minLScale
		
		#el maximo 'y' ahora corresponde al maximo 'y' del subindice
		
		self.maxY = self.third.maxY
		
		#la minima escala para subindices tambien corresponde 
		#con la minima escala hallada en el subindice
		
		self.minHScale = self.third.minHScale
		
		#el ancho es la suma del ancho de la raiz mas 
		#la maxima anchura entre el superindice y el subindice
		
		self.width = self.first.width + max(self.second.width, self.third.width)
		self.height = self.ht + self.dp

	def translate(self):

		#traducimos en primer lugar la raiz
		#luego traducimos el superindice
		#finalmente traducimos el subindice
		
		self.translation = self.first.translate()
		self.translation += self.second.translate()
		self.translation += self.third.translate()
		return self.translation


class UnderCircumflex(object):
	def __init__(self, first, second, third):
		self.scale = DEFAULT_SCALE
		self.x = DEFAULT_X
		self.y = DEFAULT_Y
		self.width = DEFAULT_WIDTH
		self.height = DEFAULT_HEIGHT
		self.dp = DEFAULT_DP
		self.ht = DEFAULT_HT
		self.minY = 1
		self.maxY = 1
		self.minHScale = DEFAULT_SCALE
		self.minLScale = DEFAULT_SCALE
		self.first = first
		self.second = second
		self.third = third
		self.children = [first, second, third]

	#para debugging
	def name(self):
		return self.first.name() + "_" + self.second.name() + "^" + self.third.name()

	def operate(self):

		#escalamos el nodo raiz
		
		scale(self.first, self.scale)

		#seteamos la posicion del nodo hijo raiz
		#la posicion se corresponde con la del nodo padre
		#y calculamos sus atributos
		
		self.first.x = self.x
		self.first.y = self.y
		self.first.operate()

		#escalo el superindice a partir del menor 
		#tamanio encontrado de superindices en el nodo raiz
		#escalo el subindice a partir del menor 
		#tamanio encontrado de subindices en el nodo raiz

		scale(self.third, self.first.minLScale * 0.7)
		scale(self.second, self.first.minHScale * 0.7)

		#seteo las posiciones del superindice y del subindice y computo sus atributos
		#luego del computo se moveran verticalmente como corresponda

		self.third.x = self.x + self.first.width
		self.second.x = self.x + self.first.width
		self.third.operate()
		self.second.operate()

		#para la posicion vertical del superindice hago uso del menor 'y' 
		#que pude encontrar en el nodo raiz
		#y lo subo un poco mas de acuerdo al menor tamanio 
		#hallado para superindices en el nodo raiz y
		#y de acuerdo a cuanto se pasa por debajo de la 
		#linea de base del superindice que aparece mas arriba
		#para la posicion vertical del subindice hago uso del mayor 'y' 
		#que puede encontrar en el nodo raiz
		#y lo bajo un poco mas de acuerdo al menor tamanio hallado 
		#para subindices en el nodo raiz y al ht del indice
		
		moveY(self.third, self.first.minY  - self.third.dp - (0.45 * self.first.minLScale))
		moveY(self.second, self.first.maxY + self.second.ht)

		#actualizamos ht, dp, height, width, maxY, minHScale, minY, minLScale 
		#con lo que calculamos de los nodos hijos
		#el ht es el de la raiz mas la altura del superindice menos
		#aproximadamente un 30% del la minima escala para superindices hallada
		
		self.ht = self.first.ht + self.third.height - 0.30 * self.first.minLScale
		
		#el dp corresponde al de la raiz mas la altura del subindice 
		#menos aproximadamente un 25% de 
		#la minima escala para subindices encontrada en la raiz
		
		self.dp = self.first.dp + self.second.height - 0.25 * self.first.minHScale
		
		#el minimo 'y' es el del superindice
		
		self.minY = self.third.minY
		
		#la minima escala para superindices es 
		#la minima escala hallada en el superindice
		
		self.minLScale = self.third.minLScale
		
		#el maximo 'y' ahora corresponde al maximo 'y' del subindice
		
		self.maxY = self.second.maxY
		
		#la minima escala para subindices tambien 
		#corresponde con la minima escala hallada en el subindice
		
		self.minHScale = self.second.minHScale
		
		#el ancho es la suma del ancho de la raiz 
		#mas la maxima anchura entre el superindice y el subindice

		self.width = self.first.width + max(self.second.width, self.third.width)
		self.height = self.ht + self.dp

	def translate(self):

		#traducimos en primer lugar la raiz
		#luego traducimos el subindice
		#finalmente traducimos el superindice
		
		self.translation = self.first.translate()
		self.translation += self.second.translate()
		self.translation += self.third.translate()
		return self.translation		

class Parenthesis(object):
	def __init__(self, child):
		self.scale = DEFAULT_SCALE
		self.x = DEFAULT_X
		self.y = DEFAULT_Y
		self.width = DEFAULT_WIDTH
		self.height = DEFAULT_HEIGHT
		self.dp = DEFAULT_DP
		self.ht = DEFAULT_HT
		self.minY = 1
		self.maxY = 1
		self.minHScale = DEFAULT_SCALE
		self.minLScale = DEFAULT_SCALE
		self.child = child
		self.children = [child]
	
	#para debugging	
	def name(self):
		return "(" + self.child.name() + ")"

	def operate(self):

		#escalamos el nodo hijo
		
		scale(self.child, self.scale)

		#horizontalmente movemos el nodo hijo 
		#para dejar lugar al parentesis que abre
		#la posicion vertical del hijo es la del nodo
		
		self.child.x = self.x + self.scale * 0.6
		self.child.y = self.y

		#computamos los atributos del nodo hijo
		self.child.operate()

		#la anchura del nodo es la del hijo 
		#mas el ancho del parentesis que abre 
		#mas el ancho del parentesis que cierra
		
		self.width = self.child.width + (2 * self.scale * 0.6)

		#actualizamos los ht y dp y la altura del nodo
		#corresponden a los hy y dp del hijo
		
		self.dp = self.child.dp 
		self.ht = self.child.ht  
		self.height = self.dp + self.ht

	def translate(self):
		#escala es un valor que se utiliza para escalar los 
		#parentesis de manera tal que cubran toda la formula 
		#y para reubicarlos. se lo divide por self.scale 
		#para contrarrestar el efecto del font-size al transformar
		# el 1.33 es un valor que 
		#probando descubrimos que parece funcionar correctamente 

		escala = self.height * 1.33 / self.scale
		
		#se escribe el parentesis que abre.
		
		self.translation = '\t<text x="0" y="0" font-size="' + str(self.scale) + '" transform="'
		
		#verticalmente se ubica un poco por encima 
		#de donde empieza el nodo hijo,
		#dado que el simbolo de parentesis 
		#se escribe un poco por debajo en la fuente elegida
		#se lo escala por el valor escala calculado

		self.translation += 'translate(' + str(self.x) + ',' + str(self.y + self.dp - 0.18 * escala) + ') scale(1,' + str(escala) + ')">(</text>\n'
		
		#traducimos el nodo hijo

		self.translation += self.child.translate()

		#escribimos el parentesis que cierra.
		#idem al partentesis  que abre,
		# con la excepcion de que verticalmente 
		#aparece mas a la derecha tanto como anchura tenga el nodo hijo

		self.translation += '\t<text x="0" y="0" font-size="' + str(self.scale) + '" transform="'
		self.translation += 'translate(' + str(self.x + self.child.width + self.scale * 0.6) + ',' + str(self.y + self.dp - 0.18 * escala) + ') scale(1,'+ str(escala) +')">)</text>\n'
		return self.translation

class Symbol(object):
	def __init__(self, value):
		self.value = value
		self.scale = DEFAULT_SCALE
		self.width = DEFAULT_WIDTH
		self.height = DEFAULT_HEIGHT
		self.dp = DEFAULT_DP
		self.ht = DEFAULT_HT
		self.x = DEFAULT_X
		self.y = DEFAULT_Y
		self.minY = 1
		self.maxY = 1
		self.minHScale = DEFAULT_SCALE
		self.minLScale = DEFAULT_SCALE
		self.children = []

	#para debugging
	def name(self):
		return str(self.value)

	def operate(self):
		#calculo los maxY y minY para el caso en el 
		#que el nodo padre es un subindice o superindice
		#o alguna combinacion de subindice y superindices 
		#como undercircumflex o circumflexunder
		
		self.maxY = self.y
		self.minY = self.y
		pass

	def translate(self):
		#traduzco el nodo de acuerdo a los 
		#atributos que se computaron en operate
		
		return '\t<text x="' + str(self.x) + '" y="' + str(self.y) +'" font-size="' + str(self.scale) + '">' + str(self.value) + '</text>\n'
