#!/bin/env bash

python3 cli.py --diff 'f(x) = cosh(x) * cos(x)' 'g(t) = sin(t) * arcsin(t)'

python3 cli.py --latex --gradient 'f(x,y,z) = ln(x / (2 * y)) - z^2 * (x - 2 * y) - 3*z' 'g(x, y) = sin(x) * cos(y)'
mv equations.* output/ && zathura output/equations.pdf --mode presentation
