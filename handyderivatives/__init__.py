#!/bin/env python3

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

parserDescription = '\nCommand line differential calculus tool using SymPy.\nGradient ex.\nhandyderivatives -l -g \'f(x,y) = sin(x) * cos(y)\''

parser = argparse.ArgumentParser(
                                    formatter_class=RawTextHelpFormatter,
                                    description=parserDescription
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

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

if ARGS.FILE:
    if not os.path.exists(ARGS.FILE):
        parser.print_help()
        sys.exit(f"\n'{ARGS.FILE}' is not a file")


from sympy import sympify, diff, Matrix, latex
from sympy.abc import *

from subprocess import run, PIPE # For running pdflatex

# ======================================================================================================================================================================

def makeLatexFile(equations):
    startStr    = '\\documentclass{article}\n\n\\usepackage{amsmath}\n\n\\begin{document}\n\n'
    endStr      = '\n\n\\end{document}'

    print('creating equations.tex')
    with open('equations.tex', 'w+', encoding='utf-8') as f:
        f.write(startStr)
        for i, eq in enumerate(equations):
            eq = eq.replace('asin', 'arcsin').replace('acos', 'arccos')

            if i % 2 == 0:
                f.write(f'({i // 2 + 1})\n\n' + '\\begin{align*}\n')
                f.write(f'\t{eq}\\\\')

            else:
                f.write(f'\t{eq}\n' +'\\end{align*}')
                f.write('\n')

            f.write('\n')

        f.write(f'{endStr}\n')

    print('compiling to equations.pdf')
    run(['pdflatex', 'equations.tex', '-quiet'], stdout=PIPE)
    for latexBuildFile in ('equations.log', 'equations.aux'):
        os.remove(latexBuildFile)

# ======================================================================================================================================================================

def cleanEquation(possibleEquation):
    if '#' in possibleEquation:
        possibleEquation = possibleEquation[:possibleEquation.find('#')]
    if possibleEquation.strip() == '':
        return None
    else:
        # https://docs.sympy.org/latest/gotchas.html#inverse-trig-functions
            # arcsin -> asin arccos -> acos
        # FIX THIS CRAP THIS IS NOT A GOOD PRACTICE.
        return possibleEquation.replace('^', '**').replace('arcsin', 'asin').replace('arccos', 'acos').replace(' ', '').replace('\t', '')

# ======================================================================================================================================================================

def parseFncStr(functionStr):
    equationSplit = functionStr.split('=')
    leftHand      = equationSplit[0]
    rightHand     = equationSplit[1]

    if leftHand[3] == ')':
        variables  = sympify(leftHand[2])
        expression = sympify(rightHand)
    else:
         variables  = [sympify(diffVariableChar) for diffVariableChar in leftHand[2:-1].split(',')]
         expression = sympify(rightHand)

    sympifyDict = {
                        'left': leftHand,
                        'right': rightHand,
                        'variables': variables,
                        'expression': expression
                }


    return sympifyDict

# ======================================================================================================================================================================

def sympyDifferentialData(equation):
    fncDict                  = parseFncStr(equation)
    derivative               = diff(fncDict['expression'], fncDict['variables'])

    equationOutput           = f'{fncDict["left"]}{" " * 7}= {fncDict["right"]}'
    equationLatex            = f'{latex(sympify(fncDict["left"]))} &= {latex(fncDict["expression"])}'

    derivativeEquationLeft   = f'd[{fncDict["left"]}]/d{fncDict["variables"]} = '
    derivativeOutput         = f'{derivativeEquationLeft}{derivative}'

    derivativeLeftHand       = '\\frac{d \\left[ ' + fncDict["left"] + ' \\right ] }' + '{d' + str(fncDict['variables']) + '}'
    derivativeLatex          = f'{derivativeLeftHand} &= {latex(derivative)}'

    return (
            f'\t{equationOutput}\n\t{derivativeOutput}\n',
            (equationLatex, derivativeLatex)
        )

# ======================================================================================================================================================================

def gradient(equation):
    fncDict       = parseFncStr(equation)
    gradientList  = [diff(fncDict["expression"], variable) for variable in fncDict["variables"]]

    colVector     = 'grad = [\n\t\t' + ',\n\t\t'.join(str(i) for i in gradientList) + '\n\t]'

    latexLeftHand = latex(sympify(fncDict["left"]))
    latexEquation = f'{latexLeftHand} &= {latex(sympify(fncDict["right"]))}'
    latexGradient = f'\\nabla {latexLeftHand} &= {latex(Matrix(gradientList))}'

    return (
            f'\t{equation.replace("=", " = ")}\n\t{colVector}',
            (latexEquation, latexGradient)
    )

# ======================================================================================================================================================================

def divergence(vector=[]):
    pass

# ======================================================================================================================================================================

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
        equation    = cleanEquation(equationOperator[0])
        operator    = equationOperator[1]
        if not equation:
            continue

        if operator.startswith('diff'):
            terminalPrint, texTuple = sympyDifferentialData(equation)
        elif operator == 'gradient':
            terminalPrint, texTuple = gradient(equation)

        consoleOutput.append(terminalPrint)
        latexEquations.extend(texTuple)

    if ARGS.LATEX:
        makeLatexFile(latexEquations)
    else:
        for i, equationOutput in enumerate(consoleOutput):
            print(f'({i+1})\n{equationOutput}')

# ======================================================================================================================================================================


def main():
    printFmtDerivatives(ARGS.FILE, strEquations=ARGS.DIFFERENTIAL)

if __name__ == '__main__':
    main()
