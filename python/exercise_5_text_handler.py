
def literalCounter(text:str) -> dict:
    literals = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    total = 0
    data = {i:0 for i in literals}
    for i in text.lower():
        if i in literals:
            total+=1
            data[i]+=1

    return {i:round(data[i]/total*100,3) for i in data.keys()}

if __name__ == '__main__':
    with open('text.txt') as f:
        text = f.read()
    print(literalCounter(text))
