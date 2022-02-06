from functools import wraps

from flask import session, request, current_app, render_template


def group_permission_validation():
    """
    Определяет права доступа пользователя

    Returns:
        bool. True - доступ разрешен, False - доступ запрещен
    """
    access_config = current_app.config['ACCESS_CONFIG']
    group_name = session.get('group_name', 'unauthorized')
    target_app = "" if len(request.endpoint.split('.')) == 1 \
        else request.endpoint.split('.')[1]
    # Определяется разрешен ли пользователю доступ к запрашиваемой странице
    if group_name in access_config and target_app in access_config[group_name]:
        return True
    return False


def group_permission_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if group_permission_validation():
            return f(*args, **kwargs)
        return render_template('permission_denied.html')

    return wrapper
