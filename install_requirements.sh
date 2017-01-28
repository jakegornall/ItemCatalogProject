#!/bin/bash
( 
	(
		# try to use pip or easy_install to install requirements.txt
		pip install -r requirements.txt || \
		easy_install "cat requirements.txt"
	) && \
	echo "Successfully Installed Requirements!"
	echo "Go to https://www.tutorialspoint.com/sqlite/sqlite_installation.htm to install Sqlite3."
	sleep 5s
) || (
# if pip and easy_install both fail, alert user and close window after 10s
echo "Unable To Install Requirements..."
echo "Please make sure that Python and pip are correctly installed..."
echo "Closing Window In 10 Seconds..."
sleep 10s
)
