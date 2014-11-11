#!/bin/bash

FILE="4ii"
X="Percentage of extra gates"
Y="Percentage of success"

gnuplot <<- EOF
	set terminal latex
	set output "$FILE.tex"
    set xlabel "$X"
    set ylabel "\\\rotatebox{90}{$Y}"
    plot "$FILE.dat" using 1:2 notitle
    #plot "$FILE.dat" using 1:2 lc rgb "blue" title "Our algorithm", "$FILE.dat" using 1:3 lc rgb "green" title "Optimal", "$FILE.dat" using 1:4 lc rgb "red" title "Difference"
EOF