#!/bin/bash

http='http://'

while read line; do
	url="${http}${line}"
	echo "${url}"
	sudo timeout 17 google-chrome --no-sandbox "${url}"
	sudo pkill chrome
	sudo rm -rf ~/.cache/google-chrome
done < topsites50.txt