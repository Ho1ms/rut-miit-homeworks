import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
psql = 'postgresql://postgres@localhost/data_science'

# Переносим данные из excel в postgresql:
# firms = pd.read_excel('data.xlsx', sheet_name=1)
# firms.to_sql('firms',psql)

# questionnaires = pd.read_excel('data.xlsx', sheet_name=2)
# questionnaires.to_sql('questionnaires',psql)

# reports = pd.read_excel('data.xlsx', sheet_name=3)
# reports.to_sql('reports',psql)

"""
Используем SQL запросы для добавления суммы с вычетом налогов
ALTER TABLE reports ADD COLUMN salary bigint;
UPDATE reports SET salary = "Сумма оклада за период (до вычета налогов)"*(1-"Величина налога,%"*0.01)

Очищаем данные, для этого ищем ошибки с помощью запроса:
SELECT q."Компания", f."Наименование" FROM questionnaires as q FULL JOIN firms as f ON q."Компания" = f."Наименование" GROUP BY q."Компания", f."Наименование" ORDER BY f."Наименование";
См. img_1.jpg

UPDATE questionnaires SET "Компания" = 'ГРИНРУС-АТОМ' WHERE "Компания" = 'GREENRUS-ATOM';
UPDATE questionnaires SET "Компания" = 'ООО "КБ-14"' WHERE "Компания" = 'ООО "КБ-140"';
UPDATE questionnaires SET "Компания" = 'ФГУБ "Салют-3"' WHERE "Компания" in ('ФГУБ "Салют"','ФГУБ "Салют3"');

Создаём таблицу report с полями company_id - id компании, total_salary - ЗП за 4 квартала
CREATE TABLE report
(
    user_id "char",
    company_id bigint,
    total_salary bigint
);

Дальше, запросом

INSERT INTO report SELECT "id-сотрудника" as user_id, "id-компании" as company_id, SUM(salary) as total_salary FROM reports GROUP BY "id-сотрудника","id-компании";

Переносим данные из reports в report
"""

data_connect = {'dbname':'data_science','user':'postgres','host':'localhost','password':''} # Коннект к базе

db = psycopg2.connect(**data_connect)
sql = db.cursor()
f1 = '("Годовой доход после вычета налого")'
f2 = '(total_salary)'
funcs = ('AVERAGE', 'MEDIAN', 'MAXIMUM','MINIMUM')


def get_data():
    sql.execute(f"""SELECT  f."Наименование", AVG{f1}, PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY {f1}), MAX{f1}, MIN{f1} 
    FROM firms as f RIGHT JOIN questionnaires as q ON q."Компания" = f."Наименование"  
    WHERE f."Отрасль" = 'Зелёная энергетика' 
    GROUP BY f."Наименование" """)
    questionnaires = sql.fetchall()

    sql.execute(
        f"""SELECT  f."Наименование", AVG{f2}, PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY {f2}), MAX{f2}, MIN{f2} 
        FROM firms as f RIGHT JOIN report as r ON r.company_id = f."id" 
         WHERE f."Отрасль" = 'Зелёная энергетика' GROUP BY f."Наименование" """)
    reports = sql.fetchall()

    data_1 = {}
    data_2 = {}
    for firm in questionnaires:
        data_1[firm[0]] = {}
        for i, _type in enumerate(funcs, start=1):
            data_1[firm[0]][_type] = int(firm[i])

    for firm in reports:
        data_2[firm[0]] = {}
        for i, _type in enumerate(funcs, start=1):
            data_2[firm[0]][_type] = int(firm[i])

    return data_1, data_2

def drawing():
    data_1, data_2 = get_data()

    for i in data_1:
        df2 = pd.Series(data_2[i])
        df1 = pd.Series(data_1[i])
        plt.title(f'Статистика по {i}')
        plt.bar(df1.index,df1)
        plt.bar(df1.index,df2, color=(0.01, 0.1, 0.2,0.5), width=0.5)

        plt.savefig(f"""{i.replace('"','')}""")
        plt.close()

# Единожды запускаем эту функцию, чтобы она отрисовала нам картинки, котрые мы будем смотреть:)
if __name__ == '__main__':
    drawing()
