import json

from flask import Flask, render_template, session

from bp_query.route import query
from bp_authorization.route import auth_app
from bp_basket.route import basket

app = Flask(__name__)

# Регистрация blueprint приложения
app.register_blueprint(query, url_prefix='/request-menu')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(basket, url_prefix='/basket')

# Настройка секретного ключа сессии, параметров подключения и прав пользователей
app.config['SECRET_KEY'] = 'my super secret key'
app.config['DB_CONFIG'] = json.load(open('configs/db.json'))
app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json'))


@app.route('/')
def index():
    """
    Возварщет html-страницу главного меню

    Returns:
        str. Html-страница главного меню
    """
    return render_template('main_menu.html')


@app.route('/exit')
def exit_session():
    """
    Возварщет html-страницу завершения сессии

    Returns:
        str. Html-страница завершения сессии
    """
    session.clear()
    return render_template('exit.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
