from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from transliterate import translit
from creat_xlsx import creat_xksx

import os

app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_flask.db'
db = SQLAlchemy(app)

def get_translit(ru_text) -> str:
    """Перевод фразы транслитерация"""
    return translit(ru_text, language_code='ru', reversed=True)

class Post(db.Model):
    """Работа с базой данных"""
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    translat = db.Column(db.Text, nullable=False)

    def __init__(self, text, translat):
        self.text = text
        self.translat = translat

@app.route("/")
def index():
    """Приветственная страница"""
    return render_template('index.html')
    
@app.route('/process', methods=['POST']) 
def process():
    """Перевод фразы, вывод транслитерации на страницу, запись данных в бд"""
    data = request.get_json()
    text = data['value']
    translat = get_translit(text)
    post = Post(text=text, translat=translat)
    try:
        db.session.add(post)
        db.session.commit()
        return jsonify(result=translat)
    except:
        return jsonify(result="Произошла ошибка.")
    
@app.route('/table', methods=['POST']) 
def table():
    """Вывод таблицы с последними 10 записями из бд, создание xlsx файла"""
    postt = db.session.query(Post).order_by(Post.id.desc()).limit(10).all()
    list_text = []
    list_translat = []
    for item in postt:
        list_text.append(item.text)
        list_translat.append(item.translat)
    full_list =  [list_text, list_translat, len(list_text)]
    creat_xksx(full_list)
    return jsonify(result=full_list)

@app.route('/download')
def download():
    """Скачивание заранее подготовленного файла"""
    path = 'Данные таблицы переводов.xlsx'
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)