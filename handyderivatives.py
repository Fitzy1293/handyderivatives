import sys
from sympy import sympify, diff, latex
from sympy.abc import *

'''
Example of file:
c(x) = r * (cos(x) + sqrt(-1)*sin(x))
a(t) = 1/2 * g * t ** 2
f(x) = sin(x**2) * x^2
h(w) = E ^ (w^4 - (3 * w)^2 + 9)
g(x) = exp(i * pi)
p(j) = csc(j^2)
'''

with open(sys.argv[1], 'r') as functionsFile:
    for i,  equation in enumerate(functionsFile.read().splitlines()):
        equationSplit            = equation.split('=')
        leftHand                 = equationSplit[0].strip()
        rightHand                = equationSplit[1].strip().replace('^', '**')

        differentiableExpression = sympify(rightHand)
        differentiableVariable   = sympify(leftHand[2])

        derivative               = diff(differentiableExpression, differentiableVariable)

        equationOutput           = f'{leftHand}{" " * 7}= {rightHand}'
        derivativeOutput         = f'd[{leftHand}]/d{differentiableVariable} = {derivative}'
        
        print(f'({i+1})')
        print(f'\t{equationOutput}')
        print(f'\t{derivativeOutput}')

