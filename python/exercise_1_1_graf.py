import json
import os

cfg = { # Точка: {Путь_к_другой_точке:длинна}
    'A':{'C':10,'B':5},
    'C':{'D':10,'E':9},
    'B':{'D':2,'F':4},
    'D':{'G':10,'H':1},
    'G':{'I':9},
    'H':{'I':7},
    'E':{'G':8},
    'F':{'H':8},
    'I':{'I':'END'}
}
if not os.path.isfile('config.json'):
    with open('config.json','w+',encoding='utf-8') as file:
        file.write(json.dumps(cfg))

with open('config.json','r',encoding='utf-8') as file:
    try:
        f = json.loads(file.read())
    except json.decoder.JSONDecodeError:
        input('Ошибка преобразования содержимого файла в JSON...\nИзмените файл и повторите попытку!')

config = f or cfg
routes = []
def tree(point, route):
    for target in config[point]:
        if point != target:
            r = [f'{route[0]}-{target}', route[1]+config[point][target]]
            tree(target, r)
        else:
            routes.append(route)


tree('A',['A',0]) # Задаём начальную точку
minimal = sorted(routes, key=lambda x:x[1])[0]
print(f'Минимальный путь: {minimal[0]}\nЕго длинна: {minimal[1]}')
input('Для завершения работы нажмите любую клавишу...')
