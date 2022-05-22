#!/bin/bash

stage=${1:-10}

if [ "$stage" -gt 0 ]; then
	yes | rm -r test-outputs/*
	mkdir test-outputs
	docker build -t k1lib_test_base .
fi

if [ "$stage" -gt 1 ]; then
	for a in $(ls -d */ | grep py3); do
		cd $a
		./build.sh
		cd ..
	done
fi

read -p "Press enter to combine all test outputs into 1 and quit"

cd test-outputs
cat `ls -t` > combined
cd ..

