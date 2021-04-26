# handyderivatives

Install with pip for the easiest use.

`pip install handyderivatives`

[https://pypi.org/project/handyderivatives/](https://pypi.org/project/handyderivatives/)

## Running it
`handyderivatives functions.txt`

## How to use it
This is a program to get the derivatives for differentiable functions of a single variable.

Edit a file that has functions listed one per line.
The left hand side should be what your function will be differentiated with respect to, i.e *f(x)* .
The right hand side will be the expression.

```
c(x) = r * (cos(x) + sqrt(-1) * sin(x))
a(t) = 1/2 * g * t ** 2
f(x) = sin(x**2) * x^2
h(w) = E ^ (w^4 - (3 * w)^2 + 9)            # Capital E is interpreted by sympy as the base of the natural log.
g(x) = exp(3 * pi)                          # So is exp(x), but written as a function.
p(j) = csc(j^2)
```

To get output that looks like this. LaTeX output is included.


![Placeholder](https://raw.githubusercontent.com/Fitzy1293/handyderivatives/main/images/output.png)
