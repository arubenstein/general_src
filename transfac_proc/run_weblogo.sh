#!/bin/bash

#runs weblogo on all *.transfac files in path
#makes lower_ind corresponding to correct lower_ind

path=$1

cd $path

gld_std_path="/Users/arubenstein/Dropbox/Research/Khare_Lab/Constant_Spec_Profiles/"

for i in $(find . -name "*.transfac" -maxdepth 1)
do


	weblogo -s large -F png -U probability --composition equiprobable -A protein -f $i -o ${i%.transfac}.png
	

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

    weblogo -s large -F png -X NO -Y NO --fineprint "" -c chemistry -U probability --composition equiprobable -A protein -f $i -o ${i%.transfac}.png

#	if [ -n "gld_std_path" ];then
#		python /Users/arubenstein/Dropbox/Research/Khare_Lab/Scripts/distances.py $i $gld_std_path ${i%.transfac}_distances.txt
#	fi

	gld_std_path="/Users/arubenstein/Dropbox/Research/Khare_Lab/Constant_Spec_Profiles/"
done
