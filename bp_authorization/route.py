"""Модуль авторизации пользователя"""

import os

from flask import Blueprint, session, render_template, request, current_app

from access import group_permission_decorator
from DB.usedatabase import work_with_db
from DB.sql_provider import SQLProvider

auth_app = Blueprint('auth', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@auth_app.route('/', methods=['GET', 'POST'])
def auth():
    """
    Возварщет html-страницу аутентификации и результат авторизации пользователя

    Returns:
        str. Html-страница
    """
    if request.method == 'GET':
        return render_template('login.html')
    else:
        log = request.form.get('login')
        passw = request.form.get('password')
        if log and passw:
            sql = provider.get('auth.sql', log=log, passw=passw)
            group = work_with_db(current_app.config['DB_CONFIG'], sql)
            if not group:
                return render_template('auth_error.html')
            session['group_name'] = group[0]['grp']
            return render_template('success_auth.html', group=group[0]['grp'])
        else:
            return render_template('auth_error.html')
