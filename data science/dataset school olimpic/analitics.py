import json
import psycopg2
import pandas as pd

# oge = pd.read_json( open('oge.json','r').read())
# oge.to_sql('oge','postgresql://postgres@localhost/MIIT')
#
# ege = pd.read_json( open('ege.json','r').read())
# ege.to_sql('ege','postgresql://postgres@localhost/MIIT')
data_connect = {'dbname':'MIIT','user':'postgres','host':'localhost','password':''} # Коннект к базе

db = psycopg2.connect(**data_connect)
sql = db.cursor()

sql.execute("""SELECT SUM(passes_over_220*3 ) as balls, edu_name FROM ege GROUP BY LOWER(REPLACE(REPLACE(REPLACE(edu_name,' ',''),'»',''),'«','')) ORDER BY balls DESC LIMIT 100""")
ege = sql.fetchall() # EGE raiting
sql.execute("""SELECT SUM(oge_score) as balls, edu_name FROM oge GROUP BY LOWER(REPLACE(REPLACE(REPLACE(edu_name,' ',''),'»',''),'«','')) ORDER BY balls DESC LIMIT 100""")
oge = sql.fetchall() # OGE raiting

sql.execute("""SELECT fullname, SUM(CASE WHEN (status='победитель') THEN 5 ELSE 4)  FROM schools  GROUP BY LOWER(REPLACE(REPLACE(REPLACE(fullname,' ',''),'»',''),'«','')), fullname ORDER BY COUNT(fullname ) DESC  LIMIT 100""")
