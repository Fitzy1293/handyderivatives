#!/bin/env bash
cat equations/* > .temp-equations
python3 -B test_package.py -f .temp-equations
python3 -B test_package.py -f .temp-equations --latex
rm .temp-equations
mv equations.* output/
