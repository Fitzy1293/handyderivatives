#!/bin/env python3

'''
handyderivatives: a program to solve differentiable functions of one variable and get latex output 

Repo: https://github.com/Fitzy1293/handyderivatives
PyPi: https://pypi.org/project/handyderivatives/

'''

import sys
import os
from subprocess import run, PIPE # For running pdflatex

from argparse import RawTextHelpFormatter, ArgumentParser

parserDescription = '\nCommand line differential calculus tool using SymPy.\nGradient ex.\nhandyderivatives -l -g \'f(x,y) = sin(x) * cos(y)\''

parser = ArgumentParser(formatter_class=RawTextHelpFormatter, description=parserDescription)
parser.add_argument(
                    '--input-file',
                    '-f',
                    dest='FILE',
                    default=False,
                    help='input file'
)
parser.add_argument(
                    '--latex',
                    '-l',
                    dest='LATEX',
                    action='store_true',
                    help='compile a LaTeX document as output'
)
parser.add_argument(
                    '--diff',
                    '-d',
                    dest='DIFFERENTIAL',
                    nargs='+',
                    action='extend',
                    help='works for equations written in the form  \'f(x) = x ^2\''
)
parser.add_argument(
                    '--gradient',
                    '-g',
                    dest='GRADIENT',
                    nargs='+',
                    action='extend',
                    help='works for scalar functions written in form  \'f(x,y,z) = x ^2 * sin(y) * cos(z)\''
)
parser.add_argument(
                    '--test',
                    '-t',
                    dest='TEST',
                    action='store_true',
                    help='testing, meant for development'
)
ARGS = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

if ARGS.FILE and not os.path.exists(ARGS.FILE):
    print(f"\n'{ARGS.FILE}' is not a file"  )
    closeScript = True
elif ARGS.FILE and ARGS.DIFFERENTIAL:
    print('invalid combination: -d --diff and -f --file')
    print('--file cannot be used with --diff or --gradient')
    print('run `handyderivatives --help` for usage')
    closeScript = True
elif ARGS.FILE and ARGS.GRADIENT:
    print('invalid combination: -g --gradient and -f --file')
    print('--file cannot be used with --diff or --gradient')
    print('run `handyderivatives --help` for usage')
    closeScript = True
else:
    closeScript = False

if not closeScript:
    from sympy import sympify, diff, Matrix, latex
    from sympy.abc import *
else:
    sys.exit(1)

# ======================================================================================================================================================================

def makeLatexFile(equations):

    startStr    = '\\documentclass[fontsize=100pt]{article}\n\n\\usepackage{amsmath}\n\n\\begin{document}\n\n'
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
        os.remove(latexBuildFile) #IF IT FAILS I'LL REMOVE IT, DISLIKE THE CLUTTER.

# ======================================================================================================================================================================

def cleanEquation(possibleEquation):
    if '#' in possibleEquation:
        cleaned = possibleEquation[:possibleEquation.find('#')]
        if cleaned.strip() == '':
            return None
        else:
            return cleaned 
    if possibleEquation.strip() == '':
        return None
    else:
        # https://docs.sympy.org/latest/gotchas.html#inverse-trig-functions
            # arcsin -> asin arccos -> acos
        # FIX THIS CRAP THIS IS NOT A GOOD PRACTICE.
        return possibleEquation.replace('^', '**').replace('arcsin', 'asin').replace('arccos', 'acos').replace(' ', '').replace('\t', '')

# ======================================================================================================================================================================

def parseFncStr(functionStr):
    leftHand, rightHand = functionStr.split('=')

    if leftHand[3] == ')': # f(x) - implying it's a scalar fnc of a single ind. variable. 
        variables, expression  = sympify(leftHand[2]), sympify(rightHand)
    else: # f(x, y, z) - variables is a list of xyz.  
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

    #equationOutput           = f'{fncDict["left"]}&= {fncDict["right"]}'
    equationLatex            = f'{latex(sympify(fncDict["left"]))} &= {latex(fncDict["expression"])}'

    derivativeEquationLeft   = f'd[{fncDict["left"]}]/d{fncDict["variables"]} = '
    derivativeOutput         = f'{derivativeEquationLeft}{derivative}'

    derivativeLeftHand       = '\\frac{d \\left[ ' + fncDict["left"] + ' \\right ] }' + '{d' + str(fncDict['variables']) + '}'
    derivativeLatex          = derivativeLeftHand + ' &= ' + latex(derivative)

    return ( derivativeOutput, (equationLatex, derivativeLatex) )

# ======================================================================================================================================================================

def gradient(equation):
    # Gets the gradient by using 
    fncDict       = parseFncStr(equation)
    gradientList  = [diff(fncDict["expression"], variable) for variable in fncDict["variables"]]


    latexLeftHand = latex(sympify(fncDict["left"]))
    latexEquation = f'{latexLeftHand} &= {latex(sympify(fncDict["right"]))}'
    latexGradient = f'\\nabla {latexLeftHand} &= {latex(Matrix(gradientList))}'

    return ( str(gradientList), (latexEquation, latexGradient) )

# ======================================================================================================================================================================

def fileEqGetter(file):
    with open(file, 'r') as functionsFile:
        for equation in functionsFile.read().splitlines():
            cleaned = cleanEquation(equation)
            if cleaned is not None:
                yield cleanEquation(equation)

# ======================================================================================================================================================================

def runner(argsparseobj):
    argsparseDict = vars(argsparseobj)
    latexList = []

    # Will separate into subfunctions, repeating a lot here
    
    if argsparseDict.get('TEST'):
        print(argsparseDict, end='\n\n')

    fileEqsVar  = argsparseDict.get('FILE')
    cliDiffVar  = argsparseDict.get('DIFFERENTIAL')
    gradientVar = argsparseDict.get('GRADIENT')
    latexFlag   = argsparseDict.get('LATEX')

    if cliDiffVar:
        for eq in cliDiffVar:
            diffData, latexData = sympyDifferentialData(cleanEquation(eq))
            print(f'function | {eq}', '|', diffData)
            print(f'latex | {latexData[0]} |', latexData[1])
            latexList.extend(latexData)

    if gradientVar:
        for eq in gradientVar:
            gradData, latexData = gradient(cleanEquation(eq))
            print(f'function | {eq}', '| gradient =>', gradData)
            print(f'latex | {latexData[0]} |', latexData[1])

            latexList.extend(latexData)
    
    if fileEqsVar:
        for eq in fileEqGetter(fileEqsVar):
            diffData, latexData = sympyDifferentialData(eq)
            print(f'function | {eq}', '| derivative =>', diffData)
            print(f'latex | {latexData[0]} |', latexData[1])
            latexList.extend(latexData)

    if latexFlag:
        makeLatexFile(latexList)

# ======================================================================================================================================================================

def main():
    runner(ARGS)

# ======================================================================================================================================================================


if __name__ == '__main__':
    main()
   