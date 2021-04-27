# handyderivatives

This is a command line program to get the derivatives for differentiable functions of a single variable.

## Installation
`pip install handyderivatives`

[https://pypi.org/project/handyderivatives/](https://pypi.org/project/handyderivatives/)

## Running it
To simply print back to the terminal.

`handyderivatives -f functions.txt`

To automatically compile a LaTeX document with pdflatex

`handyderivatives -f functions.txt --latex`

## Opening the output 
Normally you want to immediately see the output, so run something like this.

`handyderivatives -f functions.txt --latex && zathura equations.pdf`

The program used to open the PDF doesn't matter, as long as it's not something like Adobe Reader which takes a couple seconds to open on most machines.
If you can enter a PDF and it opens it, then it will work. Zathura is nice because if you ctl + c in your terminal the the window with the PDF closes, this doesn't happen with them all.

## How the input file should be formatted
Edit a file that has functions listed one per line.
The left hand side should be what your function will be differentiated with respect to, i.e *f(x)* .
The right hand side will be the expression.

```
# This is how the file for the argument -f should be formatted.

c(x) = r * (cos(x) + sqrt(-1) * sin(x))
a(t) = 1/2 * g * t ** 2
f(x) = sin(x**2) * x^2
h(w) = E ^ (w^4 - (3 * w)^2 + 9)            # Capital E is interpreted by sympy as the base of the natural log.
g(x) = exp(3 * pi)                          # So is exp(x), but written as a function taking an argument.
p(j) = csc(j^2)
```

If you don't format it like that you will likely run into errors.
You  can add comments

## TODO 
Make the program take an expression as one argument, and the variable it's being differentiated with respect to another argument. 

`handyderivatives --diff 'sin(x) + E ^ (sqrt(-1) * x)' x`


## LaTeX PDF output

![Placeholder](https://raw.githubusercontent.com/Fitzy1293/handyderivatives/main/images/output.png)
