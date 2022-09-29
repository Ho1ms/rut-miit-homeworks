import os
import psycopg2
import webbrowser
from flask import request, render_template, Flask
app = Flask('MAIN', template_folder=os.getcwd())
data_connect = {'dbname':'MIIT','user':'postgres','host':'localhost','password':''} # Коннект к базе

@app.route('/', methods=('GET','POST'))
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

        sql.execute(f"""
        SELECT shortname, count(shortname) 
        FROM schools 
        {'WHERE' if year != '()' or subject != '()' or status != '()' else ''}
        {year if year  != '()' else '' }
        {'AND' if subject != '()' else ''}
        {subject if subject  != '()' else ''}
        {'AND' if status != '()' else ''}
        {status if status != '()' else ''} 
        GROUP BY LOWER(REPLACE(REPLACE(REPLACE(shortname,' ',''),'»',''),'«','')), shortname 
        ORDER BY COUNT(shortname ) {'DESC' if data.get('is_desc') else ''} 
        LIMIT 100""")
        rows = sql.fetchall()

    else:
        sql.execute(f"""
        SELECT shortname, count(shortname) 
        FROM schools 
        GROUP BY LOWER(REPLACE(REPLACE(REPLACE(shortname,' ',''),'»',''),'«','')), shortname 
        ORDER BY COUNT(shortname ) DESC 
        LIMIT 100""")
        rows = sql.fetchall()

    db.close()
    return render_template('index.html', years=years, subjects=subjects, rows=rows, data_year=data.getlist('year'),data_subject=data.getlist('subject'),data_status=data.getlist('status'))

webbrowser.open("http://localhost", new=1)
app.run('0.0.0.0', port=80, debug=False)
