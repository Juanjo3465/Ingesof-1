"""Decoradores utilizados en el proyecto"""
from functools import wraps
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache

def login_required(view_func):
    @never_cache
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("Inicial_page")
        return view_func(request, *args, **kwargs)
    return wrapper

def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            user_role = request.user.role

            if user_role.get_name() not in allowed_roles:
                return redirect('Menu') #Update when the home page be ready

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
