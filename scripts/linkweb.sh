#!/bin/bash

if [[ -e /home/ubuntu/web ]]
then
	echo "Link already found: ~/web"
	exit
fi

if [[ -d /home/researcher/public_html/ ]]
then
	sudo chown ubuntu /home/researcher/public_html/
	if [[ -d /home/ubuntu/ ]]
	then
		sudo ln -s /home/researcher/public_html/ /home/ubuntu/web
		echo "Public directory linked: ~/web"
	fi
fi
