import sys
from sympy import sympify, diff, latex
from sympy.abc import *

'''
Program to solve differentiable functions of one variable.
LHS defines what variable it's a function of.
No format checking right now.

Example of line separated file, one equation per line.

c(x) = r * (cos(x) + sqrt(-1)*sin(x))
a(t) = 1/2 * g * t ** 2
f(x) = sin(x**2) * x^2
h(w) = E ^ (w^4 - (3 * w)^2 + 9)
g(x) = exp(i * pi)
p(j) = csc(j^2)

With that it gives you the derivative, and both the equation and derivative in LaTeX.

'''
def printFmtDerivatives():
    with open(sys.argv[1], 'r') as functionsFile:
        for i,  equation in enumerate(functionsFile.read().splitlines()):
            equationSplit            = equation.replace('^', '**').split('=')
            leftHand                 = equationSplit[0].strip()
            rightHand                = equationSplit[1].strip()

            differentiableExpression = sympify(rightHand)
            differentiableVariable   = sympify(leftHand[2])

            derivative               = diff(differentiableExpression, differentiableVariable)

            equationOutput           = f'{leftHand}{" " * 7}= {rightHand}'
            derivativeOutput         = f'd[{leftHand}]/d{differentiableVariable} = {derivative}'
            equationLatex            = latex(differentiableExpression)
            derivativeLatex          = latex(derivative)
            
            print(f'({i+1})')
            print(f'\t{equationOutput}')
            print(f'\t{derivativeOutput}')
            print()
            print(f'\tTeX fnc.{" " * 5}{equationLatex}')
            print(f'\tTeX deriv.{" " * 3}{derivativeLatex}')

def main():
    printFmtDerivatives()

if __name__ == '__main__':
    main()