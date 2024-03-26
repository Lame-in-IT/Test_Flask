function sendData() { 
    //Получение фразы на русском и оправка перевода на страницу
    var value = document.getElementById('input').value;
    $.ajax({ 
        url: '/process', 
        type: 'POST', 
        contentType: 'application/json', 
        data: JSON.stringify({ 'value': value }), 
        success: function(response) { 
            document.getElementById('output').innerHTML = response.result; 
        }, 
        error: function(error) { 
            console.log(error); 
        } 
    }); 
}


function report() {
    //создание динамической таблицы и заполнением ячеек данными
    $.ajax({ 
        url: '/table', 
        type: 'POST', 
        success: function(response) { 
            var table = '';
            var rows = response.result[2];
            var cols = 2;
            for (var r = 0; r < rows; r++)
                {
                    table += '<tr>';
                        for (var c = 0; c < cols;c++)
                        {
                            table += '<td>' + response.result[c][r] + '</td>';
                        }
                    table += '</tr>'
                }
            document.getElementById('table').innerHTML = table
        },
    }); 
}