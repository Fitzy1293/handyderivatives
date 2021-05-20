#!/bin/env bash

fxt='f(x, t) = tan( cos(t) ) - 3*x'
gt='g(t) = sin(t) * arcsin(t)'

python3 handyderivatives/cli.py --latex\
    --diff "$gt" "h(l)=l^2"\
    --gradient "$fxt"\

mv equations.* output
echo -e "\nmoved output to"
ls -d1 "$PWD"/output/*

printf '\e[0m'
exit 0
