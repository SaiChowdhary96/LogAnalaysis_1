#!/usr/bin/env python3
import psycopg2


def popular_articles(cursor):
    """For top three popular articles"""

    requested_query = """
            SELECT articles.title, count(log.path)
            AS total_count
            FROM   log,articles
            WHERE  log.path = CONCAT('/article/', articles.slug)
            GROUP BY articles.title
            ORDER BY total_count DESC
            LIMIT 3;
            """

    cursor.execute(requested_query)
    database_records = cursor.fetchall()

    print('\nTop three most popular articles')
    print('=============================================================')

    i = 1

    for database_record in database_records:
        print("{i}{bracket}{title} ---> {views} views".
              format(i=i, bracket=')', title=database_record[0],
                     views=database_record[1]))
        i = i + 1
    print('=============================================================\n')
    return


def popular_authors(cursor):
    """For popular authors"""

    requested_query = """
            SELECT authors.name, count(*)
            AS total_count
            FROM   log, articles, authors
            WHERE  log.path = CONCAT('/article/', articles.slug)
            AND articles.author = authors.id
            GROUP BY authors.name
            ORDER BY total_count DESC;
    """
    cursor.execute(requested_query)
    database_records = cursor.fetchall()

    print('Popular authors')
    print('=============================================================')

    i = 1

    for database_record in database_records:
        print("{i}{bracket}{author} ---> {views} views"
              .format(i=i, bracket=')', author=database_record[0],
                      views=database_record[1]))
        i = i+1

    print('=============================================================\n')

    return


def errors(cursor):
    """For errors"""
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
                SELECT no_of_requests.day, no_of_errors.count::float /
                no_of_requests.count::float * 100
                AS percentage_of_error
                FROM no_of_requests, no_of_errors
                WHERE no_of_requests.day = no_of_errors.day
              )
            SELECT * FROM rate_of_error WHERE percentage_of_error > 1;
    """
    cursor.execute(requested_query)
    database_records = cursor.fetchall()

    print('Days with greater than 1% errors')
    print('=============================================================')

    i = 1

    for database_record in database_records:
        print("{i}{bracket}{date:%B %d, %Y} ---> {rate_of_error:.1f}% errors"
              .format(i=i, bracket=')', date=database_record[0],
                      rate_of_error=database_record[1]))
    print('=============================================================\n')


if __name__ == "__main__":

    try:
        db_conn = psycopg2.connect(dbname='news')
        cursor = db_conn.cursor()
    except Exception:
        print("Failed to connect to the database.")

    if cursor:
        popular_articles(cursor)
        popular_authors(cursor)
        errors(cursor)
        cursor.close()
