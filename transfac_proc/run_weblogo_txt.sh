#!/bin/bash

#runs weblogo on all *.txt files in path
#makes lower_ind corresponding to correct lower_ind

path=$1
lower_ind=$2
cd $path


for i in $(find . -name "*.txt" -maxdepth 1)
do


	#weblogo -s large -F png -U probability --composition equiprobable -A protein -f $i -o ${i%.txt}.png
	
    if [  -z ${lower_ind+x} ];
    then
	if [[ $i == *1LVB*.txt ]];then
		lower_ind=-6
	elif [[ $i == *3M5L*.txt ]];then
		lower_ind=-6
	elif [[ $i == *GraB*.txt ]];then
		lower_ind=-4
	elif [[ $i == *HIV*.txt ]];then
		lower_ind=-4
	elif [[ $i == *3AYU*.txt ]]; then
		lower_ind=-2
	fi
    fi
    weblogo -s large -F png -X NO -Y YES --fineprint "" -c chemistry -U probability --composition equiprobable -A protein -f $i -o ${i%.txt}.png

done
