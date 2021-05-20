#!/bin/env bash
#clear

green='\e[0;32m'
cyan='\e[0;36m'
end='\e[0m'
blue='\e[1;34m'
magenta='\e[1;35m'

echo -e "${cyan}handyderivatives development test${end}\n"

echo -e "${blue}testing with the latex flag${green}\n"
time ./test/latex-test.sh
echo
echo -e "${blue}testing to stdout${green}\n"
time ./test/stdout-test.sh

printf ${end}
exit 0
