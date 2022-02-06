"""Модуль работы с запросами"""

import os

from flask import Blueprint, render_template, request, current_app

from DB.usedatabase import work_with_db
from DB.sql_provider import SQLProvider
from access import group_permission_decorator

query = Blueprint('query', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@query.route('/')
@group_permission_decorator
def form_request_menu():
    """
    Возварщет html-страницу меню-запросов

    Returns:
        str. Html-страница меню запросов
    """
    return render_template('request_menu.html')


@query.route('/z1', methods=['GET', 'POST'])
@group_permission_decorator
def request_form1():
    """
    Возварщет html-страницу первого запроса или его результат

    Returns:
        str. Html-страница
    """
    if request.method == 'GET':
        return render_template('form_request_z1.html')
    else:
        publishing = '"' + request.form.get('publishing') + '"'
        if publishing:
            sql = provider.get('z1.sql', publishing=publishing)
            books = work_with_db(current_app.config['DB_CONFIG'], sql)
            if not books:
                return render_template('error_z1.html')
            else:
                return render_template('z1.html',
                                       publishing=publishing, books=books)
        else:
            return render_template('error_z1.html')


@query.route('/z2', methods=['GET', 'POST'])
@group_permission_decorator
def request_form2():
    """
        Возварщет html-страницу второго запроса или его результат

        Returns:
            str. Html-страница
        """
    if request.method == 'GET':
        return render_template('form_request_z2.html')
    else:
        publishing = '"' + request.form.get('publishing') + '"'
        year = request.form.get('year')
        if publishing and year:
            sql = provider.get('z2.sql', publishing=publishing, year=year)
            info = work_with_db(current_app.config['DB_CONFIG'], sql)
            print(info)
            if len(info) == 0:
                return render_template('error_z2.html')
            else:
                title = ["Название", "Общая сумма", "Общее количество"]
                return render_template('z2.html',
                                       info=info, year=year,
                                       publishing=publishing, title=title)
        else:
            return render_template('error_z2.html')


@query.route('/z3', methods=['GET', 'POST'])
@group_permission_decorator
def request_form3():
    """
        Возварщет html-страницу третьего запроса или его результат

        Returns:
            str. Html-страница
        """
    if request.method == 'GET':
        return render_template('form_request_z3.html')
    else:
        year = request.form.get('year')
        if year:
            sql = provider.get('z3.sql', year=year)
            books_info = work_with_db(current_app.config['DB_CONFIG'], sql)
            if len(books_info) == 0:
                return render_template('error_z3.html')
            else:
                title = ["Название", "Цена", "Количество"]
                return render_template('z3.html',
                                       books=books_info, year=year, title=title)
        return render_template('error_z3.html')
