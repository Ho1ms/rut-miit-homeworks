import os
import psycopg2
import webbrowser
from flask import request, render_template, Flask
app = Flask('MAIN', template_folder=os.getcwd())
data_connect = {'dbname':'MIIT','user':'postgres','host':'localhost','password':''} # Коннект к базе

@app.route('/rating/olimp', methods=('GET','POST'))
def main():
    db = psycopg2.connect(**data_connect)
    sql = db.cursor()

    sql.execute('SELECT year FROM schools GROUP BY year') # будем в форму выводить данные для выборки по годам
    years = sql.fetchall()
    sql.execute('SELECT subject FROM schools GROUP BY subject') # будем в форму выводить данные для выборки
    subjects = sql.fetchall()

    data = request.form
    if request.method == 'POST': # Если пользователь изменил данные в форме будем создавать SQL запрос

        year = "(" + ''.join([f"year='{r}' OR " for r in data.getlist('year') if r != 'all'])[:-3]+')'
        subject =  "(" + ''.join([f"subject='{r}' OR " for r in data.getlist('subject') if r != 'all'])[:-3]+')'
        status =  "(" + ''.join([f"status='{r}' OR " for r in data.getlist('status') if r != 'all'])[:-3]+')'
        print(year)
        print(subject)
        print(status)
        q = f"""
        SELECT fullname, count(fullname) 
        FROM schools 
        {'WHERE' if year != '()' or subject != '()' or status != '()' else ''}
        {year if year  != '()' else '' }
        {'AND' if year != '()' and (subject != '()' or status != '()') else ''}
        {subject if subject  != '()' else ''}
        {'AND' if subject != '()' and status !='()' else ''}
        {status if status != '()' else ''} 
        GROUP BY LOWER(REPLACE(REPLACE(REPLACE(fullname,' ',''),'»',''),'«','')), fullname 
        ORDER BY COUNT(fullname ) {'DESC' if data.get('is_desc') else ''} 
        LIMIT 100"""
        print(q)
        sql.execute(q)
        rows = sql.fetchall()

    else:
        sql.execute(f"""
        SELECT fullname, count(shortname) 
        FROM schools 
        GROUP BY LOWER(REPLACE(REPLACE(REPLACE(fullname,' ',''),'»',''),'«','')), fullname 
        ORDER BY COUNT(fullname ) DESC 
        LIMIT 100""")
        rows = sql.fetchall()

    db.close()
    return render_template('olimp.html', years=years, subjects=subjects, rows=rows, data_year=data.getlist('year') or ('all'),data_subject=data.getlist('subject') or ('all'),data_status=data.getlist('status') or ('all'))

@app.route('/rating/exams', methods=('GET','POST'))
def rating():
    db = psycopg2.connect(**data_connect)
    sql = db.cursor()

    sql.execute("""SELECT CAST(SUM(passes_over_220*3 + passer_under_160*2 + oge_score)/50 AS numeric(6,2)) as balls, ege.edu_name FROM ege INNER JOIN oge ON ege.edu_name = oge.edu_name  AND oge.year=ege.year GROUP BY LOWER(REPLACE(REPLACE(REPLACE(ege.edu_name,' ',''),'»',''),'«','')), ege.edu_name  ORDER BY balls DESC LIMIT 100;""")
    exams = sql.fetchall()  # EGE raiting
    return render_template('exams.html', rows=exams)


webbrowser.open("http://localhost/rating/olimp", new=1)
app.run('0.0.0.0', port=80, debug=False)
