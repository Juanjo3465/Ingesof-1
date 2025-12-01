"""Decoradores utilizados en el proyecto"""
from functools import wraps
from django.shortcuts import redirect

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            response = redirect("Inicial_page")

            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response
        
        response = view_func(request, *args, **kwargs)
        
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        
        return response
    
    return wrapper

def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            user_role = request.user.role

            if user_role.get_name() not in allowed_roles:
                return redirect('forum') 

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
