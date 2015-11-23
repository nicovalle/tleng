class Divide(object):
	def __init__(self, left, right):
		self.left = left
		self.right = right

	def name(self):
		return self.left.name() + "/" + self.right.name()

class Concat(object):
	def __init__(self, left, right):
		self.left = left
		self.right = right

	def name(self):
		return self.left.name() + " " + self.right.name()

class Underscore(object):
	def __init__(self, left, right):
		self.left = left
		self.right = right

	def name(self):
		return self.left.name() + "_" + self.right.name()

class Circumflex(object):
	def __init__(self, left, right):
		self.left = left
		self.right = right

	def name(self):
		return self.left.name() + "^" + self.right.name()

class CircumflexUnder(object):
	def __init__(self, first, second, third):
		self.first = first
		self.second = second
		self.third = third

	def name(self):
		return self.first.name() + "^" + self.second.name() + "_" + self.third.name()

class UnderCircumflex(object):
	def __init__(self, first, second, third):
		self.first = first
		self.second = second
		self.third = third

	def name(self):
		return self.first.name() + "_" + self.second.name() + "^" + self.third.name()

class Parenthesis(object):
	def __init__(self, child):
		self.child = child
		
	def name(self):
		return "(" + self.child.name() + ")"

class Symbol(object):
	def __init__(self, value):
		self.value = value

	def name(self):
		return str(self.value)