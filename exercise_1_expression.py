"""
Решение квадратных уравнений в формате:
ax^2 + bx + c = 0
"""

def equation(a:float, b:float, c:float) -> dict:
    if [a,b].count(0) == 2:
        return {'message': 'Нет решений!', 'resultCode': 2}

    if a == 0:
        return {'x': -c / b}

    elif b == 0:
        x = -c / a
        if x < 0:
            return {'message': 'Нет решения! #1', 'resultCode': 2}
        x **= 0.5
        return {'x1':-x, 'x2':x}

    elif c == 0:
        return {'x1': -b / a, 'x2':0}

    else:
        D = b ** 2 - 4 * a * c

        if D < 0:
            return {'message': 'Нет решения! #2', 'resultCode': 2}

        x1 = (-b - D**0.5) / (2 * a)
        x2 = (-b + D**0.5) / (2 * a)

        return {'x':x1} if x1 == x2 else {'x1':x1, 'x2':x2}

