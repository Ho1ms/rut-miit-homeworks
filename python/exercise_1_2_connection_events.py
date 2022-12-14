from flask import Flask, request
import numpy as np
import os, signal
app = Flask(__name__)

@app.route('/', methods=('GET','POST'))
def main():
    if request.method == 'POST':
        if request.form.get('quit'):
            os.kill(os.getpid(), signal.SIGINT)
        elif request.json():
            arr = request.json.get('data')
            arr_2 = request.json.get('data2')
            l = len(arr)

            ranks = [int(i) + 1 for i in np.array(arr).argsort().argsort()]
            ranks_2 = [int(i) + 1 for i in np.array(arr_2).argsort().argsort()]
            if len(ranks) != len(ranks_2):
                return 'Массивы не совпадают'
            n = 0
            for i in range(l):
                n += (ranks[i] - ranks_2[i]) ** 2
            conn_value = abs(1 - (6 * n / (l * (l ** 2 - 1))))

            val_type = 'Незначительная'
            if conn_value > 0.7:
                val_type = 'сильная'
            elif conn_value > 0.5:
                val_type = 'значительная'
            elif conn_value > 0.3:
                val_type = 'умеренная'

            return {'val_index':conn_value,'val_type':val_type, 'r1':ranks, 'r2':ranks_2}, 200
    return page

page = """
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Ранги чисел</title>
</head>
<body>
<div>
    <style>

       button {

  /* usual styles */
  padding:15px;
  border:none;
  background-color:#3F51B5;
  color:#fff;
  font-weight:600;
  border-radius:5px;
  box-shadow:6px 6px 10px rgba(0,0,0,0.2);
  resize: vertical;

}
input {
  resize: vertical;
  padding:15px;
  border-radius:15px;
  border:0;
  box-shadow:6px 6px 10px rgba(0,0,0,0.2);
}
table {
   border: 1px solid #69c;
   border-collapse: separate;
   empty-cells: hide;
}
th, td {
   border: 2px solid #69c;
}
    </style>
    <div style="width: 30%; margin: 0 auto;">
        <h1>Расчитать связь между категориями событий</h1>
        <input type="text" id="value" placeholder="Массив 1" style="margin-bottom:10px">
        <input type="text" id="value2" placeholder="Массив 2">
        <div>
            <button onclick="get_ranks();" style="margin-bottom:10px">Расчитать</button>  
            <button onclick="close_app();" style='background-color:red' >Закрыть</button>  
        </div>
        <table style="margin-top: 20px">
            <tbody>
                <tr id="index">
                    <td>Индекс</td>
                </tr>
                <tr id="type">
                    <td>Связь</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
<script>
    function $ (id){
        return document.getElementById(id)
    }
    function close_app () {
        console.log(123)
        fetch('/',{'method':'POST','body':'quit=1','headers':{'Content-Type':'application/x-www-form-urlencoded'}})
        alert('Закрываю приложение...')
        document.location.replace('https://ya.ru/')
    }
    function get_ranks() {
        let arr = $('value').value.split(' ')
        let arr2 = $('value2').value.split(' ')
        let array = []
        let array2 = []
        
        for (let i=0;i<arr.length;i++) {
            a = parseFloat(arr[i])
            b = parseFloat(arr2[i])
            console.log(a,b)
            if (a) {
                array.push(a)
               
            }
            if (b) {
                array2.push(b)
            }
        }
        
        if (array.length !== array2.length || array.length === 0) return alert('Массивы разной длинны или они пусты!!!')
        
        let xhttp = new XMLHttpRequest();
        xhttp.open('POST',document.location.origin, true)
        xhttp.setRequestHeader('Content-Type','application/json;charset=UTF-8')
        xhttp.send(JSON.stringify({'data':array,'data2':array2}))
        xhttp.onreadystatechange = function () {
            if (this.status === 200 && this.readyState === 4){
                let index = $('index');
                let type = $('type');

                let data = JSON.parse(this.responseText);
                index.innerHTML = '<td>Массив</td>'
                type.innerHTML = '<td>Ранги</td>'
 
                index.innerHTML += `<td>${data['val_index']}</td>`
                type.innerHTML += `<td>${data['val_type']}</td>`
                
                console.log(data['r1'])
                console.log(data['r2'])
            }
        }

    }
</script>

</body>
</html>
"""


os.system(f'explorer http://127.0.0.1:5000')
app.run()