def scale(node, scale):
	node.scale = scale
	node.height = node.height * scale
	node.width = node.width * scale


class Start(object):
	def __init__(self, child):
		self.child = child
		self.x = 0
		self.y = 0
		self.scale = 1

	def name(self):
		return self.child.name()

	def translate(self):
		scale(self.child, self.scale)
		self.child.x = self.x
		self.child.y = self.y
		self.translation =  '<?xml version="1.0" standalone="no"?>\n'
		self.translation += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n'
		self.translation += '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
		self.translation += '<svg xmlns="http://www.w3.org/2000/svg" version="1.1">\n'
		self.translation += '<g transform="translate(0,200) scale(200)" font-family="Courier">\n'
		self.translation += self.child.translate()
		self.translation +='</g>\n'
		self.translation += '</svg>'
		return self.translation

class Divide(object):
	def __init__(self, left, right):
		self.left = left
		self.right = right

	def name(self):
		return self.left.name() + "/" + self.right.name()

class Concat(object):
	def __init__(self, left, right):
		self.scale = 1
		self.height = 1
		self.left = left
		self.right = right
		self.x = 0
		self.y = 0
		self.width = 0.6
		

	def name(self):
		return self.left.name() + " " + self.right.name()

	def translate(self):
		scale(self.left, self.scale)
		scale(self.right, self.scale)
		self.left.x = self.x
		self.left.y = self.y
		leftTranslation = self.left.translate()
		self.right.x = self.left.x + self.left.width
		self.right.y = self.y
		self.width = self.left.width + self.right.width
		self.height = max(self.left.height, self.right.height)
		self.translation = leftTranslation + self.right.translate()
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
		

	def name(self):
		return self.left.name() + "_" + self.right.name()

	def translate(self):
		scale(self.left, self.scale)
		scale(self.right,self.scale * 0.7)
		self.left.x = self.x
		self.left.y = self.y
		self.right.x = self.x + self.left.width
		self.right.y = self.y + (0.25 * self.scale)
		self.width = self.left.width + self.right.width
		self.height = self.left.height + (0.25 * self.scale)
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

	def name(self):
		return self.left.name() + "^" + self.right.name()

	def translate(self):
		scale(self.left, self.scale)
		scale(self.right, self.scale * 0.7)
		self.left.x = self.x
		self.left.y = self.y
		self.right.x = self.x + self.left.width
		self.right.y = self.y - (0.45 * self.scale)
		self.width = self.left.width + self.right.width
		self.height = self.left.height + (0.45 * self.scale)
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

	def name(self):
		return self.first.name() + "^" + self.second.name() + "_" + self.third.name()

	def translate(self):
		scale(self.first, self.scale)
		scale(self.second, self.scale * 0.7)
		scale(self.third, self.scale * 0.7)
		self.first.x = self.x
		self.first.y = self.y
		self.second.x = self.x + self.first.width
		self.second.y = self.y - (0.45 * self.scale)
		self.third.x = self.x + self.first.width
		self.third.y = + self.y + (0.25 * self.scale)
		secondTranslation = self.second.translate()
		thirdTranslation = self.third.translate()
		self.width = self.first.width + max(self.second.width, self.third.width)
		self.height = self.first.height + (0.45 * self.scale) + (0.25 * self.scale )
		self.translation = self.first.translate()
		self.translation += secondTranslation
		self.translation += thirdTranslation

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

	def name(self):
		return self.first.name() + "_" + self.second.name() + "^" + self.third.name()

	def translate(self):
		scale(self.first, self.scale)
		scale(self.second, self.scale * 0.7)
		scale(self.third, self.scale * 0.7)
		self.first.x = self.x
		self.first.y = self.y
		self.third.x = self.x + self.first.width
		self.third.y = self.y - (0.45 * self.scale)
		self.second.x = self.x + self.first.width
		self.second.y = + self.y + (0.25 * self.scale)
		secondTranslation = self.second.translate()
		thirdTranslation = self.third.translate()
		self.width = self.first.width + max(self.second.width, self.third.width)
		self.height = self.first.height +(0.45 * self.scale) + (0.25 * self.scale)
		self.translation = self.first.translate()
		self.translation += secondTranslation
		self.translation += thirdTranslation
		return self.translation		

class Parenthesis(object):
	def __init__(self, child):
		self.scale = 1
		self.x = 0
		self.y = 0
		self.width = 0.6
		self.height = 1
		self.child = child
		
	def name(self):
		return "(" + self.child.name() + ")"

	def translate(self):
		scale(self.child, self.scale)
		self.child.x = self.x + self.scale * 0.6
		self.child.y = self.y
		self.width = self.child.width + (2 * self.scale * 0.6)
		childTranslation = self.child.translate()
		self.height = self.child.height
		self.translation = '\t<text x="0" y="0" font-size="' + str(self.scale) + '" transform="'
		self.translation += 'translate(' + str(self.x) + ',' + str(self.y) + ') scale(1,' + str(self.height) + ')">(</text>\n'
		self.translation += childTranslation
		self.translation += '\t<text x="0" y="0" font-size="' + str(self.scale) + '" transform="'
		self.translation += 'translate(' + str(self.x + self.child.width + self.scale * 0.6) + ',' + str(self.y) + ') scale(1,'+ str(self.height) +')">)</text>\n'
		return self.translation

class Symbol(object):
	def __init__(self, value):
		self.value = value
		self.scale = 1
		self.width = 0.6
		self.height = 1

	def name(self):
		return str(self.value)

	def translate(self):
		return '\t<text x="' + str(self.x) + '" y="' + str(self.y) +'" font-size="' + str(self.scale) + '">' + str(self.value) + '</text>\n'
