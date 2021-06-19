# handyderivatives

[PyPi link](https://pypi.org/project/handyderivatives/)

A command line program to do some differential calculus.
This is essentially a wrapper for some of [SymPy's](https://github.com/sympy/sympy) calculus tools.
[Here is SymPy's calculus documentation.](https://docs.sympy.org/latest/tutorial/calculus.html)


*Right now it has the functionality listed below.*

- Differentiate elementary functions.
- Get the gradient of a scalar field.


## Installation
```
pip3 install handyderivatives
```

## Running it
To get the derivatives for an arbitrary number of functions of a single variable.

```
handyderivatives -d 'f(x) = x ^ 2' 'g(x) = sin(x) + 2 * x'
```

To get the gradient for an arbitrary number of scalar functions.

```
handyderivatives -g 'f(x,y,z) = ln(x / (2 * y)) - z^2 * (x - 2 * y) - 3*z'
```
Or run that with one command.

```
handyderivatives -d 'f(x) = x ^ 2' 'g(x) = sin(x) + 2 * x' -g 'f(x,y,z) = ln(x / (2 * y)) - z^2 * (x - 2 * y) - 3*z'
```

To differentiate a list of functions in a file and output that to a LaTeX document.

```
handyderivatives --latex -f functions.txt
handyderivatives -l -f functions.txt
```

The `-l` flag can also be used in the earlier examples.

### Help
```
usage: handyderivatives [-h] [--input-file FILE] [--latex] [--diff [DIFFERENTIAL [DIFFERENTIAL ...]]] [--gradient [GRADIENT [GRADIENT ...]]]

Command line differential calculus tool using SymPy.
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

## How the input file should be formatted
Edit a file that has functions listed one per line.
The left hand side should be what your function will be differentiated with respect to, i.e *f(x)* .
The right hand side will be the expression.

```
# This is how the file for the argument -f should be formatted.

c(x) = r * (cos(x) + sqrt(-1) * sin(x))
a(t) = 1/2 * g * t ** 2
f(x) = sin(x**2) * x^2
h(w) = E ^ (w^4 - (3 * w)^2 + 9) # Capital E is interpreted by SymPy as the base of the natural log.
g(x) = exp(3 * pi)               # So is exp(x), but written as a function taking an argument.
p(j) = csc(j^2)
```

If you don't format it like that you will likely run into errors.
You  can add comments.

<!--
## TODO
- Importing things from SymPy takes up a significant amount of time when the program first loads.
Right now it's the main bottleneck, maybe there's some way to do this faster.
- Add divergence.

## Sample PDF

![PDF-Example](https://raw.githubusercontent.com/Fitzy1293/handyderivatives/main/images/output.png)
-->
