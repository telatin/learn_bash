#!/bin/bash

if [ ! -d /home/researcher/public_html ]; then
   echo "This script is designed for training using the MRC CLIMB infrastructure (GVL image)"
   exit 1
fi

if [[ -e /home/ubuntu/web ]]
then
	echo "Link already found: ~/web"
	exit 0
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
