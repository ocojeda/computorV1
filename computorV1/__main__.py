#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse
import matplotlib.pyplot as plt
import numpy as np

from core import solve
from logger import logger
from eq_parser import parse


def graph(formula, variable, degree):
	"""Plot the function in a new windows

	Parameters
	----------
	formula : `str`
		Reduced form of the given equation.
	variable : `char`
		Name of the variable.
	degree : `int`
		Polynomial degree of the equation. Needed to don't print unnecessary members of the equation.

	Returns
	-------

	"""
	if not degree:
		logger.warning("The equation cannot be plotted, missing a dimension.")
		return

	formula = formula.replace(variable, 'x')
	formula = formula.replace('^', '**')

	x_range = range(-100, 100)

	x = np.array(x_range)
	y = eval(formula)

	plt.plot(x, y)
	plt.show()


def __get_arguments():
	for i, arg in enumerate(sys.argv):
		if arg[0] == '-' and arg != '-v' and arg != '-g':
			sys.argv[i] = ' ' + arg

	p = argparse.ArgumentParser()

	p.add_argument('equation', help="Equation to solve")
	p.add_argument('-v', '--verbose', action='store_true', help="Display intermediate steps of the program execution")
	p.add_argument('-g', '--graphic', action='store_true', help="Display graphic of the polynomial between [-100, 100]")

	return p.parse_args()


def __reduced_form(d, degree):
	"""Give the reduced form of an equation expressed as dictionary.

	Parameters
	----------
	d : `dict`
		Dictionary result from parsing an equation; should have the next format:

		- ``"variable"`` : Name of the variable.
		- ``"values"`` : Dictionary with the relation between exponent and value (exponent : value, ...)
	degree : `int`
		Polynomial degree of the equation. Needed to don't print unnecessary members of the equation.

	Returns
	-------
	reduced_form: `str`
		Reduced form of the equation expressed as ``d``.
	"""
	logger.debug("Finding reduced form of the given equation.")

	def signed_const(n):
		return " - {}".format(abs(n)) if n < 0 else " + {}".format(abs(n))

	if 'variable' not in d or 'values' not in d:
		raise Exception("Dictionary not well formatted")

	reduced_form = ""

	var = d['variable']
	for exp, const in d['values'].items():
		if const or (degree == 0 and exp == 0):
			if not reduced_form:
				reduced_form += "{}".format(const) if exp == 0 else \
					"{} * {}".format(const, var) if exp == 1 else \
						"{} * {}^{}".format(const, var, exp)
			else:
				reduced_form += "{}".format(signed_const(const)) if exp == 0 else \
					"{} * {}".format(signed_const(const), var) if exp == 1 else \
						"{} * {}^{}".format(signed_const(const), var, exp)

	return reduced_form


def __print_solution(reduced_form, degree, solution):
	"""Print the solution of the equation in the correct format.

	Parameters
	----------
	reduced_form : `str`
		Reduced form of the given equation.
	degree : `int`
		Polynomial degree of the equation.
	solution : `str`
		Solution of the equation, as well the sign of the discriminant when it makes sense.
	"""
	print("Reduced form: {} = 0".format(reduced_form))
	print("Polynomial degree: {}".format(degree))
	print(solution)


def main():
	args = __get_arguments()
	if args.verbose:
		logger.setLevel('DEBUG')

	d = parse(args.equation)

	degree, solution = solve(d['values'])
	reduced_form = __reduced_form(d, degree)

	__print_solution(reduced_form, degree, solution)

	if args.graphic and degree <= 2:
		graph(reduced_form, d['variable'], degree)


if __name__ == '__main__':

	try:
		main()

	except Exception as e:
		logger.error("Exception occurred during the execution of the program:\n {}".format(e))
