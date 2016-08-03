#!/bin/bash

#runs weblogo on all *.txt files in path
#makes lower_ind corresponding to correct lower_ind

path=$1
lower_ind=$2
cd $path


for i in $(find . -name "*.txt" -maxdepth 1)
do


	weblogo -s large -F png -U probability --composition equiprobable -A protein -f $i -o ${i%.transfac}.png
	
    if [  -z ${lower_ind+x} ];
    then
	if [[ $i == *1LVB*.transfac ]];then
		lower_ind=-6
	elif [[ $i == *3M5L*.transfac ]];then
		lower_ind=-6
	elif [[ $i == *GraB*.transfac ]];then
		lower_ind=-4
	elif [[ $i == *HIV*.transfac ]];then
		lower_ind=-4
	elif [[ $i == *3AYU*.transfac ]]; then
		lower_ind=-2
	fi
    fi
    #weblogo -s large -F png -X NO -Y NO --fineprint "" -c chemistry -U probability --composition equiprobable -A protein -f $i -o ${i%.transfac}.png

done
