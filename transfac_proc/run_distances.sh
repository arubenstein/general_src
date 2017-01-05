#!/bin/bash

#old script for comparing distances. a bit ugly and hacky, may need to update in the future.

path=$1
i_gld_std_path=$2
echo $i_gld_std_path
cd $path


for i in $(find . -name "*.transfac" -maxdepth 1 )
do
	if [ -z "$i_gld_std_path" ];
	then
        gld_std_path="/Users/arubenstein/Dropbox/Research/Khare/Constant_Spec_Profiles/"
	gld_std_lists="/Users/arubenstein/Dropbox/Research/Khare/Lists_Sequences/"
	if [[ $i == *1LVB*.transfac ]];then
		gld_std_path=$gld_std_path'1LVB.transfac'
                gld_std_cld=$gld_std_lists'list1LVBcleaved.txt'
                gld_std_ucld=$gld_std_lists'list1LVBuncleaved.txt'
	elif [[ $i == *3M5L*.transfac ]];then
		gld_std_path=$gld_std_path'3M5L.transfac'
                gld_std_cld=$gld_std_lists'list3M5Lcleaved.txt'
                gld_std_ucld=$gld_std_lists'list3M5Luncleaved.txt'	
        elif [[ $i == *GraB*.transfac ]];then
		gld_std_path=$gld_std_path'GraB.transfac'
                gld_std_cld=$gld_std_lists'listGraBcleaved.txt'
                gld_std_ucld=$gld_std_lists'listGraBuncleaved.txt'
	elif [[ $i == *HIVw*.transfac ]];then
		gld_std_path=$gld_std_path'HIVw.transfac'
                gld_std_cld=$gld_std_lists'listHIVwcleaved.txt'
                gld_std_ucld=$gld_std_lists'listHIVwuncleaved.txt'
        elif [[ $i == *HIVn*.transfac ]];then
                gld_std_path=$gld_std_path'HIVn.transfac'
                gld_std_cld=$gld_std_lists'listHIVncleaved.txt'
                gld_std_ucld=$gld_std_lists'listHIVnuncleaved.txt'
        elif [[ $i == *3AYU*.transfac ]];then
                gld_std_path=$gld_std_path'3AYU.transfac'
                gld_std_cld=$gld_std_lists'list3AYUcleaved.txt'
#                gld_std_ucld=$gld_std_lists'list3AYUuncleaved.txt'
        elif [[ $i == *1L3R*.transfac ]];then
                gld_std_path=$gld_std_path'1L3R.transfac'
                gld_std_cld=$gld_std_lists'list1L3Rcleaved.txt'
#                gld_std_ucld=$gld_std_lists'list1L3Runcleaved.txt'
        elif [[ $i == *1TP3*.transfac ]];then
                gld_std_path=$gld_std_path'1TP3.transfac'
                gld_std_cld=$gld_std_lists'list1TP3cleaved.txt'
#                gld_std_ucld=$gld_std_lists'list1TP3uncleaved.txt'
        elif [[ $i == *1CKA*.transfac ]];then
                gld_std_path=$gld_std_path'1CKA.transfac'
                gld_std_cld=$gld_std_lists'list1CKAcleaved.txt'
#                gld_std_ucld=$gld_std_lists'list1CKAuncleaved.txt'
        elif [[ $i == *1SPS*.transfac ]];then
                gld_std_path=$gld_std_path'1SPS.transfac'
                gld_std_cld=$gld_std_lists'list1SPScleaved.txt'
#                gld_std_ucld=$gld_std_lists'list1SPSuncleaved.txt'
        elif [[ $i == *2he4*.transfac ]];then
                gld_std_path=$gld_std_path'2he4.transfac'
                gld_std_cld=$gld_std_lists'list2he4cleaved.txt'
                gld_std_ucld=$gld_std_lists'list2he4uncleaved.txt'
        else
		gld_std_path=""
	fi
	fi

	npos=`tail -n +2 $i  | wc -l | awk '{print $1}'`	

	if [ -n "$gld_std_path" ];then
		python ~/git_repos/general_src/transfac_proc/Distances.py $i $gld_std_path
		if [ -n "$gld_std_ucld" ];then
			echo $gld_std_ucld $i first 
                        python ~/git_repos/general_src/transfac_proc/ScoreSequenceROC.py $gld_std_path $i $gld_std_cld $gld_std_ucld
#                	 python /Users/arubenstein/Dropbox/Research/Khare/Scripts/ScoreSequenceBar.py $gld_std_path $i $gld_std_cld $gld_std_ucld
                fi

		if [[ $i != *enr.transfac ]];then
                	python ~/git_repos/general_src/transfac_proc/EnrichBackground.py /Users/arubenstein/Dropbox/Research/Khare/PDB_Files/figures/peptiDB/avg'/peptiDB_'$npos.transfac $i
#			python /Users/arubenstein/Dropbox/Research/Khare/Scripts/EnrichBackground.py /Users/arubenstein/Dropbox/Research/Khare/PDB_Files/figures/figure_4_controls/sequence_tolerance/pepti_DB/peptiDB_avg.transfac $i
                	enr="${i%.*}"_enr.transfac
			python ~/git_repos/general_src/transfac_proc/Distances.py $enr $gld_std_path
			if [ -n "$gld_std_ucld" ];then
				echo $gld_std_ucld $i
                 		python ~/git_repos/general_src/transfac_proc/ScoreSequenceROC.py $gld_std_path $enr $gld_std_cld $gld_std_ucld
#                                python /Users/arubenstein/Dropbox/Research/Khare/Scripts/ScoreSequenceBar.py $gld_std_path $enr $gld_std_cld $gld_std_ucld

			fi
	                python ~/git_repos/general_src/transfac_proc/Info.py $i 
			python ~/git_repos/general_src/transfac_proc/Info.py $enr

		fi
	elif [  -n "$i_gld_std_path" ];then
		python ~/git_repos/general_src/transfac_proc/Distances.py $i $i_gld_std_path
	fi
	python ~/git_repos/general_src/transfac_proc/Info.py $i 
done
