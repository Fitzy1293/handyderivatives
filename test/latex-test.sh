#!/bin/env bash

fxt='f(x, t) = tan( cos(t) ) - 3*x'
gt='g(t) = sin(t) * arcsin(t)'

python3 handyderivatives/__init__.py --latex\
    --diff "$gt" "h(l)=l^2"\
    --gradient "$fxt"\
    | cat -n

mv equations.* output
echo -e "\nmoved output to"
printf "./" && realpath --relative-to="./" "./output/equations.aux"
ls "./output" | sed 's=^=./output/='

printf '\e[0m'
exit 0
