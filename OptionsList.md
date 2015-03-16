# Details #

<b><u>Required parameters:</u></b>

-f | --file:   sqlite database file.

-s | --server: MySQL server's name.

-d | --dbname: MySQL database name

Use only one of the two following options:

-t | --test  : Launches a simulation of the program and prints the       modified dump in stdout

-e | --execute: Execute the program using all the parameters given and transfers the sqlite database into the given void MySQL database.


<b><u>Optional parameters:</u></b>

-s | --server  : Name of the distant MySQL server. If the server is local the program automatically uses the my.ini configuration.

-u | --user    : MySQL user name. Only rquired if the my.ini file is not configured or the server is distant.

-p | --password: MySQL password. Only rquired if the my.ini file is not configured or the server is distant.

-l | --sqlite  :  Sqlite executable's name.

-m | --mysql   : MySQL client's path.

-o | --output  : "Set the output filename. Default is random name in system temp directory"

-c | --encoding: Encoding of the MySQL database. Defaults to "UTF-8"

-b | --debug   : Use this option if you want the result of all methods used in the program.

-v | --verbose : Use this option if you just want to see where the program fails.

-i | --ignore  : Use this if you want to ignore one or more tables in the Sqlite dump. You can ignore as mmany as 5 tables. If you want to be able to ignore more than 5 tables go to line 256 in sqlite2mysql.py and  add table parameters separated by a ";".