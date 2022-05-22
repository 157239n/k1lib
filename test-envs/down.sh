#!/bin/bash

for a in $(ls -d */ | grep py3); do 
	cd $a
	docker compose down
	cd ..
done

