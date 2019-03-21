from logger import logger


def __sqrt(n):
	return n ** (1/2)


def __curt(n):
	return -(-n) ** (1 / 3) if n < 0 else n ** (1 / 3)


def solve_constant(a):
	"""Solves a constant equation (form: a = 0 <=> ax^0 = 0)

	Parameters
	----------
	a : `float`
		Value of the constant term.

	Returns
	-------
	s : `str`
		Solution of the equation.
	"""
	logger.debug("Solving a constant function.")

	if a == 0:
		return "All the real numbers are solution."
	return "There are not solutions."


def solve_linear(a, b):
	"""Solves a linear equation (form: ax + b = 0)

	Parameters
	----------
	a : `float`
		Value of the constant in the simple term.
	b : `float`
		Value of the constant.

	Returns
	-------

	Raises
	------
	s : `str`
		Solution of the linear polynomial.
	"""
	logger.debug("Solving a linear function of the form ax + b = 0; where a={}, b={}".format(a, b))
	if not a:
		raise Exception("A simple equation cannot have the simple member equal to 0")

	x = -b / a

	return "The solution is:\n {}".format(x)


def solve_quadratic(a, b, c):
	"""Solves a quadratic equation (form: ax^2 + bx + c = 0).

	Parameters
	----------
	a : `float`
		Value of the constant in the quadratic term.
	b : `float`
		Value of the constant in the simple term.
	c : `float`
		Value of the constant.

	Returns
	-------
	s : `str`
		Solution of the quadratic polynomial.

	Raises
	------
	"""
	logger.debug("Solving a quadratic function of the form ax^2 + bx + c = 0; where a={}, b={}, c={}".format(a, b, c))
	if not a:
		raise Exception("A quadratic equation cannot have the quadratic member equal to 0")

	logger.debug("Calculating discriminant: D = b^2 - 4ac")
	discriminant = b ** 2 - 4 * a * c

	if discriminant != 0:
		logger.debug("Discriminant is different to zero: The equation has 2 solutions, given by the formula: (-b ± sqrt(D)) / 2a")
		x1 = (-b - __sqrt(discriminant)) / (2. * a)
		x2 = (-b + __sqrt(discriminant)) / (2. * a)

		if discriminant > 0:
			return "Discriminant is strictly positive, the two solutions are:\n {}\n {}".format(x1, x2)
		else:
			return "Discriminant is strictly negative, the two solutions are:\n {}\n {}".format(x1, x2)

	else:
		logger.debug("Discriminant is zero: The equation has only one solution in the real domain: (-b + sqrt(D)) / 2a")
		x = (-b + __sqrt(discriminant)) / (2. * a)

		return "Discriminant is zero, the solution is:\n {}".format(x)


def solve(values):
	"""Give the solution to a polynomial.

	Parameters
	----------
	values : `dict`
		Dictionary containing the relation between exponent and value (``exponent`` : ``value``). Always include the
		exponent 0 with the default value of 0.0.

	Returns
	-------
	degree : `int`
		Degree of the equation.
	solution : `str`
		Solution of the equation in string, if multiples solutions one each line. Includes sign of the discriminant when
		it makes sense.
	"""
	logger.debug("Calculating solutions.")

	# Polynomial degree
	degree = max((k for k in values.keys() if values[k]), default=0)
	logger.debug("The degree of the equation is {}.".format(degree))

	# Solution of the equation
	solution = solve_constant(a=values.get(0, 0)) if degree == 0 else \
		solve_linear(a=values.get(1, 0), b=values.get(0, 0)) if degree == 1 else \
			solve_quadratic(a=values.get(2, 0), b=values.get(1, 0), c=values.get(0, 0)) if degree == 2 else \
				"The polynomial degree is strictly greater than 2, I can't solve it."

	return degree, solution
