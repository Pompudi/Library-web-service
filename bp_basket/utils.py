"""Модуль изменения корзины"""

from flask import session


def add_to_basket(item: dict) -> None:
    """
    Добавляет товар в корзину или увеличивает его количество

    Args:
        item: dict. Добавляемый товар
    """
    basket = session.get('basket', [])
    flag = True
    for i in basket:
        if item['ID_book'] == i['ID_book'] and item['Price'] == i['Price']:
            i['count'] += 1
            flag = False
    if flag:
        item['count'] = 1
        basket.append(item)
    session['basket'] = basket


def delete_from_basket(item: dict) -> None:
    """
    Убирает товар из корзины.

    Args:
        item: dict. Удаляемый товар
    """
    basket = session.get('basket', [])
    print("basket" + str(basket))
    for i in basket:
        if i['ID_book'] == item['ID_book'] and i['ID_doc'] == item['ID_doc']:
            basket.remove(i)
    session['basket'] = basket


def delete_one_item(item: dict) -> None:
    """
    Уменьшает количество товара в корзине на 1.

    Args:
        item: dict. Удаляемый товар
    """
    basket = session.get('basket', [])
    for i in basket:
        if item['ID_book'] == i['ID_book'] and item['Price'] == i['Price']:
            i['count'] -= 1
            if i['count'] == 0:
                basket.remove(i)
    session['basket'] = basket


def clear_basket() -> None:
    """
        Очищает корзину
    """
    if 'basket' in session:
        session.pop('basket')
