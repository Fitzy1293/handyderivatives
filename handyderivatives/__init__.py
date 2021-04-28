'''
Repo: https://github.com/Fitzy1293/handyderivatives
PyPi: https://pypi.org/project/handyderivatives/


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
import os
import argparse
from argparse import RawTextHelpFormatter
from pprint import pprint

parser = argparse.ArgumentParser(
                                formatter_class=RawTextHelpFormatter,
                                description='Command line differential calculus tool using sympy.\nTry running:\nhandyderivatives -l -g \'f(x,y) = sin(x) * cos(y)\''
                                )
parser.add_argument(
                        '--input-file',
                		 '-f',
                		 dest='FILE',
                		 help='Input file'
                    )
parser.add_argument(
                        '--latex',
                        '-l',
                		dest='LATEX',
                		 action='store_true',
                		 help='Compile a LaTeX document as output'
         )
parser.add_argument(
                        '--diff',
                        '-d',
                        dest='DIFFERENTIAL',
                        nargs='*',
                        help='Works for equations written in the form  \'f(x) = x ^2\''
         )
parser.add_argument(
                        '--gradient',
                        '-g',
                        dest='GRADIENT',
                        nargs='*',
                        help='Works for scalar functions written in form  \'f(x,y,z) = x ^2 * sin(y) * cos(z)\''
         )


ARGS = parser.parse_args()

ARGC = len(sys.argv)
if ARGC == 1:
    parser.print_help()
    sys.exit()

if ARGS.FILE:
    if not os.path.exists(ARGS.FILE):
        parser.print_help()
        sys.exit(f"\n'{ARGS.FILE}' is not a file")

import subprocess # For running pdflatex
from sympy import sympify, diff, latex, Matrix
from sympy.abc import *


def makeLatexFile(equations):
    startStr    = '\\documentclass{article}\n\n\\usepackage{amsmath}\n\n\\begin{document}\n\n'
    endStr      = '\n\n\\end{document}'

    print('creating equations.tex')
    with open('equations.tex', 'w+') as f:
        f.write(startStr)
        for i, eq in enumerate(equations):
            if i % 2 == 0:
                f.write(f'({i // 2 + 1})\n\n' + '\\begin{align*}\n')
                f.write(f'\t{eq}\\\\')

            else:
                f.write(f'\t{eq}\n' +'\\end{align*}')
                f.write('\n')

            f.write('\n')


        f.write(f'{endStr}\n')

    print('compiling to equations.pdf')
    subprocess.run(['pdflatex', 'equations.tex', '-quiet'], stdout=subprocess.PIPE)
    for latexBuildFile in ('equations.log', 'equations.aux'):
        os.remove(latexBuildFile)


def cleanEquation(possibleEquation):
    if '#' in possibleEquation:
        possibleEquation = possibleEquation[:possibleEquation.find('#')]
    if possibleEquation.strip() in (''):
        return None
    else:
        return possibleEquation.replace('^', '**')

def sympyDifferentialData(equation):
    equationSplit            = equation.split('=')
    leftHand                 = equationSplit[0].strip()
    rightHand                = equationSplit[1].strip()

    differentiableExpression = sympify(rightHand)
    differentiableVariable   = sympify(leftHand[2])
    derivative               = diff(differentiableExpression, differentiableVariable)

    equationOutput           = f'{leftHand}{" " * 7}= {rightHand}'
    equationLatex            = f'{latex(sympify(leftHand))} &= {latex(differentiableExpression)}'

    derivativeEquationLeft   = f'd[{leftHand}]/d{differentiableVariable} = '
    derivativeOutput         = f'{derivativeEquationLeft}{derivative}'

    derivativeLeftHand       = '\\frac{d \\left[ ' + leftHand + ' \\right ] }' + '{d' + str(differentiableVariable) + '}'
    derivativeLatex          = f'{derivativeLeftHand} &= {latex(derivative)}'

    output = (
                f'\t{equationOutput}',
                f'\t{derivativeOutput}\n',
                f'\tTeX fnc.{" " * 5}{equationLatex}',
                f'\tTeX deriv.{" " * 3}{derivativeLatex}'
            )

    return ('\n'.join(output), (equationLatex, derivativeLatex))


def gradient(scalarFunctionStr):
    equation = cleanEquation(scalarFunctionStr)
    equationSplit                = equation.split('=')
    leftHand                     = equationSplit[0].strip()
    rightHand                    = equationSplit[1].strip()

    differentiableExpression     = sympify(rightHand)
    variables                    = leftHand.replace(' ', '')[2:-1].split(',')

    gradientComponents           = [diff(differentiableExpression, sympify(variable)) for variable in variables]

    latexLeftHand                = latex(sympify(leftHand))
    latexEquation                = f'{latexLeftHand} &= {latex(differentiableExpression)}'
    gradientVectorFormatting     = Matrix(gradientComponents)
    latexGradient                = f'\\nabla {latexLeftHand} &= {latex(gradientVectorFormatting)}'

    return (f'\t{equation}\n\t< {str(gradientComponents)[1:-1]} >', (latexEquation, latexGradient))


def printFmtDerivatives(file, strEquations=[]):
    equations = []

    if file:
        with open(file, 'r') as functionsFile:
            for equation in functionsFile.read().splitlines():
                equations.append((equation, 'diff-file'))

    if strEquations:
        for equation in strEquations:
            equations.append((equation, 'diff'))

    if ARGS.GRADIENT:
        for inputGradient in ARGS.GRADIENT:
            equations.append((inputGradient, 'gradient'))

    latexEquations  = []
    consoleOutput   = []
    for equationOperator in equations:
        equation = cleanEquation(equationOperator[0])
        operator = equationOperator[1]
        if not equation:
            continue

        if operator.startswith('diff'):
            terminalPrint, latexFunctionDerivativeTuple = sympyDifferentialData(equation)
        elif operator == 'gradient':
            terminalPrint, latexFunctionDerivativeTuple = gradient(equation)


        consoleOutput.append(terminalPrint)
        latexEquations.extend(latexFunctionDerivativeTuple)


    if ARGS.LATEX:
        makeLatexFile(latexEquations)
    else:
        for i, equationOutput in enumerate(consoleOutput):
            print(f'({i+1})\n{equationOutput}')


def main():
    printFmtDerivatives(ARGS.FILE, strEquations=ARGS.DIFFERENTIAL)

if __name__ == '__main__':
    main()
