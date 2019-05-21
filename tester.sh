#!/bin/bash

catalog_name="tests"
directory_name=$(pwd)

counter=0

for file in $directory_name/$catalog_name/*
do
	(( counter++ ))
	echo "running on test №$counter:"
	flag=1
	while read line
	do
		if [ $flag -eq 0 ]
		then
			break
		fi

		eval "$line" || flag=0
	done < $file

	if [ $flag -eq 0 ]
	then
		break
	fi

	echo "OK"
done
