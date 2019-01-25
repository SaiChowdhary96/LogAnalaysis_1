#### LogAnalaysis_1

# Project Overview:
We need to create a reporting tool using python to answer the queries raised by the users.

# Required Software for the Project:
Virtual Box (https://www.virtualbox.org/)
Vagrant (https://www.vagrantup.com/)
Python (https://www.python.org/)

Firstly install Virtual Box, Vagrant and Python.
Open your project folder and add and intialize the vagrant box by using the following commands:
# $ vagrant box add ubuntu/trusty64
# $ vagrant init ubuntu/trusty64

Now use the following command to bring up the virtual machine:
# $ vagrant up

Connect to the virtual machine by using the following command:
# $ vagrant ssh

Now a terminal opens and following is displayed:
vagrant@vagrant-ubuntu-trusty-64:~$

Now install pip, psycopg2 and postgresql using the following commands:
# $ sudo apt-get install python-pip
# $ sudo apt-get install python-psycopg2
# $ sudo apt-get install postgresql 

Now download 'newsdata.zip' and extract it to the project folder.
A file with name 'newsdata.sql' will be extracted to the project folder.

Now type in the following command:
# $ psql -d news -f newsdata.sql

The above command creates a new database 'news' and dumps the database 'newsdata' into it.
Now the 'news' database consists of follwing tables:

# authors ----> This table contains details of authors
# articles ----> This table contains list of articles written by authors
# log ----> This table contains the list of users who viewed the articles

Now we need to create a reporting tool to answer the following questions:
# 1) What are the most popular 3 articles of all time?
# 2) Who are the most popular article authors of all time?
# 3) On which days did more than 1% more of requests lead to errors?

'LogAnalysis.py' is the reporting tool I created to answer the questions.
In this we use 'psycopg2' library to connect to postgresql database
The following queries are used to answer the questions:

For the first question(What are the most popular 3 articles of all time?):

requested_query = """ SELECT articles.title, count(log.path) AS total_count FROM   log,articles
            WHERE  log.path = CONCAT('/article/', articles.slug) GROUP BY articles.title
            ORDER BY total_count DESC LIMIT 3 """

For the second question(Who are the most popular article authors of all time?):
requested_query = """
            SELECT authors.name, count(*)
            AS total_count
            FROM   log, articles, authors
            WHERE  log.path = CONCAT('/article/', articles.slug)
            AND articles.author = authors.id
            GROUP BY authors.name
            ORDER BY total_count DESC;
            """    
    
For the third question(On which days did more than 1% more of requests lead to errors?):
requested_query = """
            WITH no_of_requests AS (
                SELECT time::date 
                AS day, 
                count(*) FROM log
                GROUP BY time::date
                ORDER BY time::date
              ), 
              no_of_errors AS (
                SELECT time::date AS day, count(*) FROM log
                WHERE status = '404 NOT FOUND'
                GROUP BY time::date
                ORDER BY time::date
              ),
              rate_of_error AS (
                SELECT no_of_requests.day, no_of_errors.count::float / no_of_requests.count::float * 100
                AS percentage_of_error
                FROM no_of_requests, no_of_errors
                WHERE no_of_requests.day = no_of_errors.day
              )
            SELECT * FROM rate_of_error WHERE percentage_of_error > 1;
    """

Now save the file 'LogAnalysis.py' and run it by using the following command:
# $ python LogAnalysis.py
   
