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

import sys
# Want this to fail quick for taking the ~1s that importing sympy takes.
if len(sys.argv) == 1:
        exit('enter a filename')
import os
import subprocess # For running pdflatex
import argparse

from sympy import sympify, diff, latex
from sympy.abc import *

parser = argparse.ArgumentParser(description='Differentiate functions of a single variable.')
parser.add_argument('--input-file', '-f', dest='FILE', help='Input file')
parser.add_argument('--latex', '-l', dest='LATEX', default=False, action='store_true', help='Compile a LaTeX document as output')
ARGS = parser.parse_args()

def makeLatexFile(equations):
    startStr    = '\\documentclass{article}\n\n\\usepackage{amsmath}\n\n\\begin{document}\n\n'
    endStr      = '\n\n\\end{document}'

    print('creating equations.tex')
    with open('equations.tex', 'w+') as f:
        f.write(startStr)
        for i, eq in enumerate(equations):
            if i % 2 == 0:
                f.write(f'({i // 2 + 1})\n')

            f.write(f'$${eq}$$')

            if i %2 != 0:
                f.write('\\\\')
                f.write('\n')

            f.write('\n')

        f.write(f'{endStr}\n')

    print('compiling to equations.pdf')
    subprocess.run(['pdflatex', 'equations.tex', '-quiet'], stdout=subprocess.PIPE)
    for latexBuildFile in ('equations.log', 'equations.aux'):
        os.remove(latexBuildFile)


def printFmtDerivatives(file):
    with open(file, 'r') as functionsFile:

        validLineCt     = 0
        latexEquations  = []
        consoleOutput   = []

        for equation in functionsFile.read().splitlines():
            if '#' in equation:
                equation = equation[:equation.find('#')]
            if equation.strip() in (''):
                continue

            equationSplit            = equation.replace('^', '**').split('=')
            leftHand                 = equationSplit[0].strip()
            rightHand                = equationSplit[1].strip()

            differentiableExpression = sympify(rightHand)
            differentiableVariable   = sympify(leftHand[2])

            derivativeEquationLeft   = f'd[{leftHand}]/d{differentiableVariable} = '
            derivative               = diff(differentiableExpression, differentiableVariable)

            equationOutput           = f'{leftHand}{" " * 7}= {rightHand}'
            derivativeOutput         = f'{derivativeEquationLeft}{derivative}'

            equationLatex            = f'{latex(leftHand)}{latex(" = ")}{latex(differentiableExpression)}'
            derivativeLatex          = f'{latex(derivativeEquationLeft)}{latex(derivative)}'


            latexEquations.extend((equationLatex, derivativeLatex))

            output = (
                        f'({validLineCt+1})',
                        f'\t{equationOutput}',
                        f'\t{derivativeOutput}\n',
                        f'\tTeX fnc.{" " * 5}{equationLatex}',
                        f'\tTeX deriv.{" " * 3}{derivativeLatex}'
                    )

            consoleOutput.append('\n'.join(output))

            validLineCt += 1

        if ARGS.LATEX:
            makeLatexFile(latexEquations)
        else:
            for equationOutput in consoleOutput:
                print(equationOutput)


def main():
    printFmtDerivatives(ARGS.FILE)

if __name__ == '__main__':
    main()
