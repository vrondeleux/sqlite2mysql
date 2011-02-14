What is Sqlite2mysql?
******************

Sqlite2mysql is a free Python module created to easily and automatically transfer Sqlite databases files into already created but void MySql databases.  It works correctly in both Linux and Windows environnement.   


What's the point of it? 
*******************************

 FloretInteractive is a small company, located in Reunion Island and owned by Regis Floret. Specialised in Python Web development, it creates custom-built sites for companies. 
 	These sites'datas were firstly stocked on Sqlite databases but needed to be transfered on Mysql databases for better performance. Vincent Rondeleux, engaged for a 4 monts training, realised it as his first Python project in the company.

How to install:
***************

This module is used in command line in both windows and Linux. You also need Python 2.6 or higher in Windows, or Python 2.5 or higher in Linux. 
 
To use it, just copy it in the directory you want, and from the command line access this directory and type the required options at least: 

Example:
python sqlitetomysql.py -f sqlite_filename -s MySql_server -d MySql_database -l Sqlite_exe -e   

This module implements a specific command line parser and therefore uses several options, described as following:

Required parameters:
-f | --file: The name of the Sqlite database file  
-s | --server: MySql server's name
-d | --dbname: MySql database name path.
-l | --sqlite: The path for the Sqlite executable

-t | --test: Launches a simulation for the transfer and prints the modified dump 		 in stdout
-e | --execute: Executes the accurate transfer using all the given parameters. 

Important: You may use only one of the last two options, but at least one is required. Using either zero or both options will raise an error and exit the program. 

Optional parameters: 

-u | --user: 	MySql username; Optional only if MySql « my.ini » file is 			 	configured to default 	the username.
-p | --password:  MySql password; Optional only if MySql « my.ini » file is 				configured to default 	the password.

--debug:		This option is used for printing a complete set of results for all the commands used in the program. It does not correct mistakes but permits to know exactly what went wrong.

-i | --ignore: Permits to ignore as much as five tables in the original Sqlite 		   database. Just separate the table names with a « ; » and they 		   will be erased from the final modified dump.
		   Example: -i  auth_user ; company_adress
	
Web sites:
***********

Web site of the company:

http://www.floretinteractive.fr

Project download: 

http://code.google.com/p/sqlite2mysql

