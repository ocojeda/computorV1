import re
from logger import logger


def __dicts_union(d1, d2):
	"""Makes the union operation between given dictionaries.

	Parameters
	----------
	d1 : `dict`
		First dictionary, parsed from an expression.
	d2 : `dict`
		Second dictionary, parsed from an expression.

	Returns
	-------
	d : `dict`
		Dictionary result of apply the "union" operation between ``d1`` and ``d2``; has the next format:

		- ``variable`` : Name of the variable if is the same in ``d1['variable']`` and ``d2['variable']``.
		- ``values`` : Dictionary with the relation between exponent and value, result of the sum of the constant for
		each exponent between ``d1['values']`` and ``d2[values]``.

	Raises
	------
	"""
	if d1['variable'] and d2['variable'] and d1['variable'] != d2['variable']:
		raise Exception("Conflict of variables between expressions")

	# Update the values dictionary of the left expression with the values of the right expression
	values = d1['values'].copy()
	for exponent, value in d2['values'].items():
		values[exponent] = -value if exponent not in values else (values[exponent] - value)
	return {
		'variable': d1['variable'] if d1['variable'] else d2['variable'],
		'values': values,
	}


def __parse_expression(expr):
	"""Parse the given math expression into a dictionary.

	Parameters
	----------
	expr : `str`
		Math expression to parse. Should be formatted: "(signed_float)*(alpha_char)^(int)...", without spaces.

	Returns
	-------
	d : `dict`
		Dictionary with the data parsed from ``expr``, with the the next content:

		- ``"variable"`` : Name of the variable.
		- ``"values"`` : Dictionary with the relation between exponent and value (exponent : value, ...). Always include
		the 0 exponent with the default value of 0. The value can be either <float> or <int>.

	Raises
	------
	"""
	if not expr:
		raise Exception("Expressions cannot be an empty")

	# Parse string
	d = {
		'variable': None,
		'values': {
			0: 0,
		},
	}

	regex = r"(?P<const1>(?:^|\+|\-)\d+(?:\.?\d+)?)(?:\*?(?P<var1>[a-zA-Z])(?:\^(?P<exp1>\d+))?)?|(?P<const2>(?:^|\+|\-))(?P<var2>[a-zA-Z])(?:\^(?P<exp2>\d+))?"
	matches = re.finditer(regex, expr)		# match: "<const> * <var> ^ <exp>"

	i = 0
	for match in matches:
		if i != match.start():
			raise Exception("Characters where not parsed in the expression")

		if match['const1']:
			try:
				constant = int(match['const1'])
			except ValueError:
				constant = float(match['const1'])

			variable = match['var1']
			exponent = int(match['exp1']) if match['exp1'] else 1 if match['var1'] else 0

		else:
			constant = -1 if match['const2'] == '-' else 1

			variable = match['var2']
			exponent = int(match['exp2']) if match['exp2'] else 1

		if constant != 0:
			# variable
			if d['variable'] is None:
				d['variable'] = variable
			elif variable and variable != d['variable']:
				raise Exception("Conflict of variables in the same expression")

			# exponent check
			if exponent < 0:
				raise Exception("The exponent cannot be negative")

			# exponent : value
			d['values'][exponent] = constant if exponent not in d['values'] else (d['values'][exponent] + constant)

		i = match.end()

	if i != len(expr):
		raise Exception("Characters where not parsed in the expression")

	return d


def parse(eq):
	"""Parse a polynomial equation from given string.

	Parameters
	----------
	eq : `str`
		Equation to parse. Should be formatted: "left_expression = right_expression"

	Returns
	-------
	d : `dict`
		Dictionary result from parsing the equation, with the next content:

		- ``"variable"``: Name of the variable.
		- ``"values"`` : Dictionary with the relation between exponent and value (exponent : value, ...)

	Raises
	------

	Notes
	-----
	Always the input ``eq`` will be well formatted !!!
	"""
	logger.debug("Parsing equation.")

	# Remove all whitespaces from the equation
	eq = re.sub(r"\s+", "", eq)

	# Separate the left expression from the right expression
	split = eq.split("=")
	if len(split) != 2:
		raise Exception("Left expression and right expression cannot be defined. One and only one character '=' expected")
	l_expr = split[0]
	r_expr = split[1]

	# Parse expressions
	logger.debug("Parsing left member of the equation.")
	d1 = __parse_expression(l_expr)
	logger.debug("Parsing right member of the equation.")
	d2 = __parse_expression(r_expr)

	return __dicts_union(d1, d2)
