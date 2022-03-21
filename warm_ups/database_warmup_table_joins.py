# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 09:50:35 2022

@author: youmisuk
"""
# python
import sqlite3

# create some data
company_hq = [
        ('NVDA','Santa Clara'),
        ('AAPL','Cupertino'),
        ('GOOG','Mountain View')]

company_ceos = [
        ('NVDA','Jensen Huang'),
        ('AAPL','Tim Cook')]


# connect to db

# update with your path to the database
path_to_db = "C:/Users/oubra/anaconda3/Lib/site-packages/sqlalchemy/dialects/sqlite/mydata.db"    

# create db connection
conn = sqlite3.connect(path_to_db)

# create cursor
cur = conn.cursor()

# create a table in the db called "hq" and pass schema (ticker text, location text)
# end the transaction with a commit

#cur.execute('create table hq (ticker, location)')
#conn.commit()

# create a table in the db called "ceo" and pass schema (ticker text, ceo text)

# cur.execute('create table ceo (ticker, ceo)')

# insert records into hq table

hq = [
        ('a', 'loc1'),
        ('b', 'loc2'),
        ('c', 'loc3')
]
cur.execute('insert into hq values (?,?)', hq)

# insert records into ceo table

ceo = [
       ('a', 'ceo1'),
       ('b', 'ceo2'),
       ('c', 'ceo3') 
]
cur.execute('insert into ceo values (?,?)', ceo)

conn.commit()
# query each table to make sure all the data has been loaded
for row in cur.execute('select * from hq'):
    print(row)

# repeat for ceo table
for row in cur.execute('select * from ceo'):
    print(row)

# join the two tables together, printing records with columns: ticker, location, ceo

# Run the code below, notice the result, and we will discuss it.
    
for row in conn.execute('select hq.ticker, hq.location, ceo.ceo \
                        from hq inner join ceo \
                        on hq.ticker = ceo.ticker'):
    print(row)
    
# Next, change inner join to left join, run the query, and notice the result

for row in conn.execute('select hq.ticker, hq.location, ceo.ceo \
                        from hq left join ceo \
                        on hq.ticker = ceo.ticker'):
    print(row)

# For discussion:
# 1) notation: table.field; for example hq.ticker
# 2) inner join vs left join
# 3) joining "on" fields