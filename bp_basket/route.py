"""Модлуь оформления новой поставки"""

import os
import datetime

from flask import Blueprint, render_template, request, redirect, session, \
    current_app

from DB.usedatabase import work_with_db, make_update
from DB.sql_provider import SQLProvider
from .utils import add_to_basket, clear_basket, delete_from_basket, \
    delete_one_item
from access import group_permission_decorator

basket = Blueprint('basket', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@basket.route('/', methods=['GET', 'POST'])
@group_permission_decorator
def list_orders_handler():
    """
    Возварщет html-страницу корзины

    Returns:
        str. Html-страница
    """
    db_config = current_app.config['DB_CONFIG']
    if request.method == 'GET':
        basket = session.get('basket', [])

        sql = provider.get('order_list.sql')
        items = work_with_db(db_config, sql)
        return render_template('basket_order_list.html',
                               basket=basket, items=items)
    else:
        book_id = request.form.get('book_id')
        izd_id = request.form.get('izd_id')
        flag_delete = request.form.get('delete')
        flag_minus = request.form.get('minus')
        flag_plus = request.form.get('plus')
        sql = provider.get('order_item.sql', book_id=book_id, izd_id=izd_id)
        items = work_with_db(db_config, sql)
        if not items:
            return render_template('no_item.html')
        elif not flag_delete and not flag_minus and not flag_plus:
            add_to_basket(items[0])
        elif flag_delete:
            delete_from_basket(items[0])
        elif flag_minus:
            delete_one_item(items[0])
        else:
            add_to_basket(items[0])
        return redirect('/basket')


@basket.route('/clear-basket')
@group_permission_decorator
def clear_basket_handler():
    """
   Возварщет html-страницу очищенной корзины

    Returns:
        str. Html-страница
    """
    if 'basket' in session:
        session.pop('basket')
        return redirect('/basket')


@basket.route('/buy')
@group_permission_decorator
def buy():
    """
    Возварщет html-страницу с сообщением об оформлении поставки

    Returns:
        str. Html-страница
    """
    basket = session.get('basket', [])
    print(basket)
    for i in basket:
        id_book = i['ID_book']
        id_doc = i['ID_doc']
        count = i['count']
        price = i['Price']
        sum = count * price
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d')
        sql = provider.get('insert.sql', date=date, sum=sum, price=price,
                           id_book=id_book, id_doc=id_doc,
                           count=count)
        make_update(current_app.config['DB_CONFIG'], sql)
    session.pop('basket')
    return render_template('buy.html')
