def scale(node, scale):
	node.scale = scale
	node.height = node.height * scale
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
		self.children = [child]

	def name(self):
		return self.child.name()

	def operate(self):
		scale(self.child, self.scale)
		self.child.x = self.x
		self.child.y = self.y
		self.child.operate()

	def translate(self):
		self.translation =  '<?xml version="1.0" standalone="no"?>\n'
		self.translation += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n'
		self.translation += '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
		self.translation += '<svg xmlns="http://www.w3.org/2000/svg" version="1.1">\n'
		self.translation += '<g transform="translate(20,' + str(abs(getMinY(self.child) - self.y - 2) * 200) + ') scale(200)" font-family="Courier">\n'
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
		self.children = [left, right]

	def name(self):

		return self.left.name() + "/" + self.right.name()

	def operate(self):
		scale(self.left, self.scale)
		scale(self.right, self.scale)
		self.left.x = self.x
		self.left.y = self.y - 0.40 * self.scale
		self.right.x = self.x
		self.right.y = self.y
		self.left.operate()
		self.right.operate()
		rightMinNode = getMinYNode(self.right)
		rightMinScale = rightMinNode.scale
		rightMinHeight = rightMinNode.height
		rightMinY = rightMinNode.y
		#moveY(self.right, self.right.height - 0.50 * self.scale)
		#print self.right.name(), rightMinY, self.y 
		if(rightMinY < self.y):
			#print "IF", self.right.name()
			#print "miny", rightMinNode.name()
			#moveY(self.right, self.right.height - 0.50 * self.scale)
			moveY(self.right, abs((rightMinY-rightMinHeight) - (self.y - 0.28 * self.scale)))# + 0.50 * self.scale)
		else:
			#print "ELSE", self.right.name()
			moveY(self.right, 0.50 * self.scale)
		#if ((self.y-0.28 * self.scale) > rightMinY):		
		#	moveY(self.right, self.right.height - 0.50 * self.scale)
		#else:
		#	moveY(self.right, self.y - 0.50 *  self.scale)
			
		leftMaxY = getMaxY(self.left)
		if(leftMaxY > self.y - 0.28 * self.scale):		
			moveY(self.left, - abs((self.y - 0.50 * self.scale) - leftMaxY))
		self.width = max(self.left.width, self.right.width)
		self.height = self.left.height + self.right.height + 2* 0.28 * self.scale
		center = (self.x + (self.x + self.width))/2
		rightCenter = (self.right.x + (self.right.x + self.right.width))/2
		leftCenter = (self.left.x + (self.left.x + self.left.width))/2
		moveX(self.left, abs(leftCenter - center))
		moveX(self.right, abs(rightCenter - center))


			
		
	def translate(self):
		self.translation = self.left.translate()
		self.translation += '\t<line x1="' + str(self.x) + '" y1="' + str(self.y - 0.28 * self.scale) + '" '
		self.translation += 'x2="' + str(self.x + self.width) +'" y2="' + str(self.y -  0.28 * self.scale) + '" '
		self.translation +='stroke-width="0.03" stroke="black"/>\n'
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
		self.children = [left, right]
		

	def name(self):
		return self.left.name() + " " + self.right.name()

	def operate(self):
		scale(self.left, self.scale)
		scale(self.right, self.scale)
		self.left.x = self.x
		self.left.y = self.y
		self.left.operate()
		self.right.x = self.left.x + self.left.width
		self.right.y = self.y
		self.right.operate()
		self.width = self.left.width + self.right.width
		self.height = max(self.left.height, self.right.height)
		

	def translate(self):
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
		self.width = self.left.width + self.right.width
		self.height = self.left.height + self.right.height - (0.25 * self.scale)

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
		self.width = self.left.width + self.right.width
		self.height = self.left.height + self.right.height - (0.45 * self.scale)
	
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
		self.width = self.first.width + max(self.second.width, self.third.width)
		self.height = self.first.height + self.second.height + self.third.height - (0.45 * self.scale) -  (0.25 * self.scale)
	
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
		self.width = self.first.width + max(self.second.width, self.third.width)
		self.height = self.first.height + self.second.height + self.third.height - (0.45 * self.scale) -  (0.25 * self.scale)

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
		self.child = child
		self.children = [child]
		
	def name(self):
		return "(" + self.child.name() + ")"

	def operate(self):
		scale(self.child, self.scale)
		self.child.x = self.x + self.scale * 0.6
		self.child.y = self.y
		self.child.operate()
		self.width = self.child.width + (2 * self.scale * 0.6)
		self.height = self.child.height

	def translate2(self):
		self.translation = '\t<text x="0" y="0" font-size="' + str(self.scale) + '" transform="'
		#self.translation += 'translate(' + str(self.x) + ',' + str(getMaxY(self.child) - 0.13 * self.child.height) + ') scale(1,' + str( 0.9 * self.height) + ')">(</text>\n'
		#if self.child.name() == "(1/A/B/C/x) (2/D/E/F/y) (3/G/H/I/z)": 
		print "DESDE ACA"
		minYNode = getMinYNode(self.child)
		print self.child.height
		#print getMinY(self.child), getMaxY(self.child)
		#print abs(getMaxY(self.child)-getMinY(self.child)), "vs", 0.9*self.child.height
		print "HASTA ACA"
		#	print "lala", self.child.name(), getMinYNode(self.child).name() , getMaxYNode(self.child).name()
		#	print "los y "
		#	printY(self.child)
		#print "lala", abs(getMinY(self.child)), abs(getMaxY(self.child)), str(abs(abs(getMinY(self.child)) - abs(getMaxY(self.child)))), self.child.height
		self.translation += 'translate(' + str(self.x) + ',' + str(getMaxY(self.child) - 0.13 * self.child.height) + ') scale(1,' + str(abs(getMaxY(self.child)-(getMinY(self.child)-minYNode.height)) - 0.1 * self.height) + ')">(</text>\n'
		self.translation += self.child.translate()
		self.translation += '\t<text x="0" y="0" font-size="' + str(self.scale) + '" transform="'
		#self.translation += 'translate(' + str(self.x + self.child.width + self.scale * 0.6) + ',' + str(getMaxY(self.child) - 0.13 * self.child.height) + ') scale(1,'+ str(0.9 * self.height) +')">)</text>\n'
		self.translation += 'translate(' + str(self.x + self.child.width + self.scale * 0.6) + ',' + str(getMaxY(self.child) - 0.13 * self.child.height) + ') scale(1,'+ str(abs(getMaxY(self.child)-(getMinY(self.child)-minYNode.height))) +')">)</text>\n'
		return self.translation

	def translate3(self):
		print 0, self.child.name()
		print 1, self.child.height
		print 2, abs(getMaxY(self.child)-(getMinY(self.child) - getMinYNode(self.child).height))
		self.translation = '\t<text x="0" y="0" font-size="' + str(self.scale) + '" transform="'
		#self.translation += 'translate(' + str(self.x) + ',' + str(getMaxY(self.child) - 0.13 * self.child.height) + ') scale(1,' + str(0.9* self.height) + ')">(</text>\n'
		self.translation += 'translate(' + str(self.x) + ',' + str(getMaxY(self.child)*0.5) + ') scale(1,' + str(0.8* abs(getMaxY(self.child)-(getMinY(self.child) - getMinYNode(self.child).height)) + 0.10 * self.child.height) + ')">(</text>\n'
		self.translation += self.child.translate()
		self.translation += '\t<text x="0" y="0" font-size="' + str(self.scale) + '" transform="'
		self.translation += 'translate(' + str(self.x + self.child.width + self.scale * 0.6) + ',' + str(getMaxY(self.child)) + ') scale(1,'+ str(abs(getMaxY(self.child)-(getMinY(self.child) - getMinYNode(self.child).height))) +')">)</text>\n'
		return self.translation

	def translate(self):
		self.translation = '\t<text x="0" y="0" font-size="' + str(self.scale) + '" transform="'
		self.translation += 'translate(' + str(self.x) + ',' + str(getMaxY(self.child)) + ') scale(1,' + str(self.height) + ')">(</text>\n'
		self.translation += self.child.translate()
		print "mirrar", getMinYNode(self.child).name(), getMaxY(self.child), getMinY(self.child), getMinYNode(self.child).height
		print "dale", str(abs(getMaxY(self.child)-(getMinY(self.child) - getMinYNode(self.child).height)))
		self.translation += '\t<text x="0" y="0" font-size="' + str(self.scale) + '" transform="'
		self.translation += 'translate(' + str(self.x + self.child.width + self.scale * 0.6) + ',' + str(getMaxY(self.child)) + ') scale(1,'+ str(abs(getMaxY(self.child)-(getMinY(self.child) - getMinYNode(self.child).height)))+')">)</text>\n'
		return self.translation	
class Symbol(object):
	def __init__(self, value):
		self.value = value
		self.scale = 1
		self.width = 0.6
		self.height = 1
		self.x = 0
		self.y = 0
		self.children = []

	def name(self):
		return str(self.value)

	def operate(self):
		pass

	def translate(self):
		return '\t<text x="' + str(self.x) + '" y="' + str(self.y) +'" font-size="' + str(self.scale) + '">' + str(self.value) + '</text>\n'
