#!/bin/env bash

fxyz='f(x,y,z) = ln(x / (2 * y)) - z^2 * (x - 2 * y) - 3*z'
fx='f(x) = cosh(x) * cos(x)'

python3 handyderivatives/cli.py\
    --diff "$fx"\
    --gradient "$fxyz"

printf '\e[0m'
exit 0
