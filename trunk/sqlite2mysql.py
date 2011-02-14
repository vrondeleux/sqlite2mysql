#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
sqlite2mysql [options]

sqlite2mysql - Convert a SQLite database file to a MySQL database
%s
version : %s    
"""
        
__author__ = "Vincent Rondeleux : <vincent.rondeleux@yahoo.fr>"
__copyright__ = "(c) Floret Interactive 2011"
__version__ = "0.1"

import sys
import os
import re
import optparse
import subprocess  
import platform
import hashlib
import time
import tempfile

options = None

def display_error(message, exiting=True):
    """
    Displays an error message and exit
    @param message the error output header (string)
    """
    sys.stderr.write(u"An error occured: %s" % message)
    if exiting:
        sys.exit('')
        
def dump_sqlite(sqlite_exe):
    """
    This function realises the dump of an Sqlite database and store it in memory
    with a subprocess.
    @param sqlite_exe the path for the Sqlite executable, verified by find_sqlite()
    """
    sqlite_dump = subprocess.Popen([sqlite_exe, options.filename, ".dump"],
                                    stdout=subprocess.PIPE)
    stdout, stderr = sqlite_dump.communicate()
    return stdout
    
def prepare_dump_sqlite(resultat):    
    """
    This function modifies the Sqlite dump (stored in memory), adapting it to Mysql server.
    It uses regular expressions for finding and modifying required expressions. 
    And returns the modified dump file.
    @param sqlite_dump the dump from the Sqlite database file.
    """ 
    encode_string = "SET NAMES %s;\n" % options.encoding
    encode_string = encode_string.encode("UTF8", 'replace')
    resultat = encode_string + resultat    
    if options.debug == True:
        print u"encoding= %s" % options.encoding
    
    if options.verbose == True:
        print "Remove PRAGMA"
    regex = re.compile(r'(pragma.*?;)', re.IGNORECASE)  
    resultat = regex.sub("", resultat, 1)
    
    if options.verbose == True:
        print "Remove BEGIN TRANSACTION;"
    regex = re.compile(r'(begin.*?;)', re.IGNORECASE)
    resultat = regex.sub("", resultat, 1)
    
    if options.verbose == True:
        print "Remove COMMIT"
    regex = re.compile(r'(commit.*?;)', re.IGNORECASE)
    resultat = regex.sub("", resultat, 1)
    
    if options.ignore:                
        options_list = options.ignore.split(";")
        for table in options_list:
            if options.verbose == True:
                print "Ignoring table creation for %s" % table
            pattern= r'create\s+table\s+.%s.*?\);' % table
            regex = re.compile(pattern, re.MULTILINE | re.IGNORECASE | re.DOTALL)
            findall = regex.findall(resultat)
            for index in findall:
                delete_string = "%s" % index
                resultat = resultat.replace(delete_string, "")
    
    
    if options.verbose == True:
        print "Replacing CREATE TABLE name"
        
    regex = re.compile(r'create\s+table\s+(".*?")(.*?)\);', re.IGNORECASE | re.MULTILINE | re.DOTALL)
    for res in regex.findall(resultat):
        result = "`%s`" % res[0][1:-1]
        
        tablename = resultat.replace(res[0], result)
        res1 = res[1].replace('"', '`')
        resultat = resultat.replace("%s%s);" % (res[0], res[1]),"%s%s);"%(result, res1))
        
         
    if options.ignore:        
        options_list = options.ignore.split(";")
    
        for table in options_list:
            if options.verbose == True:
                print "Ignoring insertions for %s" % table
                
            pattern = r'insert\s+into\s+.%s.*\);' % table
            regex = re.compile(pattern, re.MULTILINE | re.IGNORECASE |re.DOTALL)
            findall = regex.findall(resultat)
            for index in findall:
                delete_string = "%s" % index
                resultat = resultat.replace(delete_string, "")
        
    if options.verbose:
        print "Replacing table insertion name"  
    regex = re.compile(r'insert\s+into\s+(".*?")(.*?)\);', re.IGNORECASE | re.MULTILINE | re.DOTALL)
    for res in regex.findall(resultat):
        result = "`%s`" % res[0][1:-1]

        tablename = resultat.replace(res[0], result)
        res1 = res[1].replace('"', '`')
        resultat = resultat.replace("%s%s);" % (res[0], res[1]),"%s%s);"%(result, res1)) 
     
    if options.ignore:        
        options_list = options.ignore.split(";")
    
        for table in options_list:
            if options.verbose == True:
                print "Ignoring index creations for %s" % table
                
            pattern = r'create\s+index.*?on\s+"%s".*?\;' % table
            regex = re.compile(pattern, re.IGNORECASE | re.MULTILINE | re.DOTALL)
            findall = regex.findall(resultat)

            for index in findall:
                delete_string = "%s" % index
                resultat = resultat.replace(delete_string, "")
    
    
    if options.verbose:
        print "Replacing index creation"
    regex = re.compile(r'create\s+index\s+(".*?")(.*?)\);', re.IGNORECASE | re.MULTILINE | re.DOTALL)
    for res in regex.findall(resultat):
        result = "`%s`" % res[0][1:-1]

        tablename = resultat.replace(res[0], result)
        res1 = res[1].replace('"', '`')
        resultat = resultat.replace("%s%s);" % (res[0], res[1]),"%s%s);"%(result, res1))
        
            
        
    if options.verbose == True:
        print "Replacing  double quote in tables name"

 
    resultat = resultat.replace("PRIMARY KEY", 'PRIMARY KEY AUTO_INCREMENT')
    resultat = resultat.replace("AUTOINCREMENT", "")
    regex = re.compile(r'(.*?varchar.*?PRIMARY KEY) (AUTO_INCREMENT).*?\n',
                       re.IGNORECASE | re.MULTILINE)
    
    for res in regex.findall(resultat):
        resultat = resultat.replace('%s %s' % (res[0], res[1]), res[0])
     
    if options.verbose == True:
        print "Replacing  \\'' by '' "
    resultat = resultat.replace("\\''", "''")
    
    if options.debug == True:
        open('debug.sql', 'w').write(resultat)
        
    return resultat.decode("UTF-8")
   
def parse_cmd_line():
    """
    This function implements a command-line parser for the program. 
    It returns the values called as arguments in the command line. 
    All options are required.
    """
    global options
   
    parser = optparse.OptionParser(usage=__doc__ % (__copyright__, __version__))
    parser.add_option("-f", "--file",
                      dest="filename",
                      help=u"The Sqlite database file to export")
    parser.add_option("-s", "--server",
                      dest="servername",
                      help=u"Your MySql server name") 
    parser.add_option("-u", "--user",
                      dest="username",
                      help=u"Your Mysql username",)
    parser.add_option("-p", "--password",
                      dest="password",
                      help=u"Your Mysql password",)
    parser.add_option("-d", "--dbname",
                      dest="dbname",
                      help=u"Mysql database name")
    parser.add_option("-l", "--sqlite",
                      dest="sqlite_path",
                      help=u"Your Sqlite executable's path")
    parser.add_option("-e", "--execute",
                      action="store_true",
                      dest="execute",
                      help=u"Use this option to realise the Sqlite to Mysql export")
    parser.add_option("-t", "--test",
                      action="store_true",
                      dest="test",
                      help=u"Use this option to test the Sqlite to Mysql export")
    parser.add_option("-v", "--verbose",
                      dest="verbose",
                      help=u"Use this option for commentaries",
                      action="store_true")
    parser.add_option("-c", "--encoding",
                      dest="encoding",
                      help=u"Use this option to choose the encoding of your mysql database", default="UTF8")
    parser.add_option("-b", "--debug",
                      dest="debug",
                      help=u"Use this option to see the program thinking",
                      action="store_true",
                      default=False)
    parser.add_option("-i", "--ignore table1;table2;table3;table4;table5",
                      dest="ignore",
                      help=u"Use this option if you want to delete a table from the import"
                      )
    parser.add_option("-m", "--mysql",
                      dest="mysqlbin",
                      help=u"MySQL binary path")
    parser.add_option('-o', '--output',
                      dest="output",
                      default=os.path.join(tempfile.gettempdir(), hashlib.md5(str(time.time())).hexdigest()),
                      help="Set the output filename. Default is random name in system temp directory")
    (options, args) = parser.parse_args()
    

    errorString = u""
    if options.filename is None:
        errorString += 'Sqlite dump filename is required\n' 
    elif not os.path.exists(options.filename): 
        errorString += u"%s : File not found\n" % options.filename
        
    if options.dbname is None:
        errorString += "Mysql database is required\n"
        
    if options.servername is None:
        errorString += "Mysql server name is required\n"
    
    if options.test == True and options.execute == True:
        errorString += 'Only --test OR --execute, not both\n'
    
    if  options.test is None and options.execute is None: 
        errorString += ' --test or --execute required'
      
    if len(errorString):
        display_error(errorString)
    
    if options.debug == True:
        print "Parse errors: %s" % errorString

def find_binary(binname, defaultname):
    """ """
    if binname is not None:
        if os.path.exists(binname):
            return binname
        display_error("%s not found" % binname)
    
    pathes = os.environ["PATH"] 
    plateforme = platform.system()
    
    if plateforme == "Windows":
        pathes = pathes.split(";")
        defaultname += ".exe"
    else:
        pathes = pathes.split(":")
        
    for dir in pathes:
        dir = os.path.normcase(dir)
        try:
            for f in os.listdir(dir):
                if defaultname == f:
                    file_path= os.path.join(dir, defaultname)
                    return '"%s"' % file_path
        except:
            pass
    return False

def fill_mysql_db(mysqlclientpath, export_file):
    """
    Function used for importing the modified Sqlite dump using a sub shell
    """
    args = []
    args.append(mysqlclientpath)
    args.append('--host=%s' % options.servername)
    
    if options.username:
        args.append('--user=%s' % options.username)
    
    if options.password:
        args.append('--password=%s' % options.password)
        args.append('--database=%s' % options.dbname)
        
    mysql_export = subprocess.Popen(args,
                                    stdin = subprocess.PIPE)
    stdout, stderr = mysql_export.communicate(input=export_file)
    return stdout   
    
if __name__ == '__main__':
    """
    If the program is launched directly with the command line
    Parses the command-line options
    If options.test is called, prints the result in standard output but does not realise the export into MySQL
    If options.execute is called the program realises the export into Mysql server using the parameters given in command-line.
    """
    parse_cmd_line()
    if options.verbose == True:
        print "Trying to establish MySQL connection"

    if options.verbose == True:
        print "Trying to find SQLite in your current PATH"
    sqlite_exe = find_binary(options.sqlite_path, 'sqlite3')
    if options.verbose == True:
        print "Trying to find MySQL client binary in your system path"
    mysqlbin = find_binary(options.mysqlbin, 'mysql')    
    if mysqlbin == False:
        display_error("mysql not found")

    if sys.platform != "Windows":
        sqlite_exe = sqlite_exe[1:-1]
        mysqlbin = mysqlbin[1:-1]

    if options.verbose == True:
        print "Dump SQLite database"
    sqlite_dump = dump_sqlite(sqlite_exe)
    
    if options.debug == True or options.verbose == True:
        print "Dump done"
        print "Modifying SQLite dump for MySQL import"
        
    export_file = prepare_dump_sqlite(sqlite_dump)
    export_file = export_file.encode('UTF-8', 'replace')
    if options.test == True:
        if options.debug == True:
            open('debug.sql', 'w').write(export_file)
        print export_file
        
    if options.verbose == True:
        print "Importing SQLite modified dump into MySQL database"
        
    if options.execute == True:
        if options.debug == True:
            open("debug.sql", "w").write(export_file)
        
        try:
            fill_mysql_db(mysqlbin, export_file)
        except Exception, e:
            sys.exit(e)

    if options.verbose == True:
        print "Job's done. Have a cool day"
    
