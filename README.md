# handyderivatives

This is a command line program to get the derivatives for differentiable functions of a single variable.

## Installation
`pip install handyderivatives`

[https://pypi.org/project/handyderivatives/](https://pypi.org/project/handyderivatives/)

## Running it
To get the derivatives for an arbitrary number of functions of a single variable.

`handyderivatives --latex -d 'f(x) = x ^ 2' 'g(x) = sin(x) + 2 * x'` ...

To get the gradient for an arbitrary number of scalar functions.

`handyderivatives --latex -g 'f(x,y,z) = ln(x / (2 * y)) - z^2 * (x - 2 * y) - 3*z'` ...

Or run that with one command.

`handyderivatives -l -d 'f(x) = x ^ 2' 'g(x) = sin(x) + 2 * x' -g 'f(x,y,z) = ln(x / (2 * y)) - z^2 * (x - 2 * y) - 3*z'`

To differentiate a list of functions in a file.

`handyderivatives --latex -f functions.txt`


```
usage: handyderivatives [-h] [--input-file FILE] [--latex] [--diff [DIFFERENTIAL [DIFFERENTIAL ...]]] [--gradient [GRADIENT [GRADIENT ...]]]

Command line differential calculus tool using sympy.
Try running:
handyderivatives -l -g 'f(x,y) = sin(x) * cos(y)'

optional arguments:
  -h, --help            show this help message and exit
  --input-file FILE, -f FILE
                        Input file
  --latex, -l           Compile a LaTeX document as output
  --diff [DIFFERENTIAL [DIFFERENTIAL ...]], -d [DIFFERENTIAL [DIFFERENTIAL ...]]
                        Works for equations written in the form  'f(x) = x ^2'
  --gradient [GRADIENT [GRADIENT ...]], -g [GRADIENT [GRADIENT ...]]
                        Works for scalar functions written in form  'f(x,y,z) = x ^2 * sin(y) * cos(z)'
```

## Opening the output
Normally you want to immediately see the output, so run something like this.

`handyderivatives -l -d 'f(x) = sin(x)' && zathura equations.pdf --mode presentation`

The program used to open the PDF doesn't matter, as long as it's not something like Adobe Reader which takes a couple seconds to open on most machines.
If you can enter a PDF and it opens it, then it will work.
Zathura is nice because if you ctl + c in your terminal, or press q in the Zathura window, it will close the PDF.
This doesn't happen with all PDF viewers.

## How the input file should be formatted
Edit a file that has functions listed one per line.
The left hand side should be what your function will be differentiated with respect to, i.e *f(x)* .
The right hand side will be the expression.

```
# This is how the file for the argument -f should be formatted.

c(x) = r * (cos(x) + sqrt(-1) * sin(x))
a(t) = 1/2 * g * t ** 2
f(x) = sin(x**2) * x^2
h(w) = E ^ (w^4 - (3 * w)^2 + 9)    # Capital E is interpreted by sympy as the base of the natural log.
g(x) = exp(3 * pi)                  # So is exp(x), but written as a function taking an argument.
p(j) = csc(j^2)
```

If you don't format it like that you will likely run into errors.
You  can add comments

## TODO
Record screen while the program is executing for an example.

Add divergence.

## LaTeX PDF output

![Placeholder](https://raw.githubusercontent.com/Fitzy1293/handyderivatives/main/images/output.png)
