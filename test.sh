#!/bin/env bash
cat equations/* > .temp-equations
python3 -B cli.py -f .temp-equations
python3 -B cli.py -f .temp-equations --latex
rm .temp-equations
mv equations.* output/
