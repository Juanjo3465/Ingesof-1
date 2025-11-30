"""Definien contextos globales"""

def apartment_url(request):
    """
    Define la url para acceder a la informacion 
    del apartamento dependiendo del rol
    """
    if not request.user.is_authenticated:
        return {'apartment_url': ''}
    
    user = request.user
    url = user.role.get_apartment_url()
        
    return {'apartment_url': url}

def menu_context(request):
    """
    Context processor para el menú lateral.
    Devuelve los items del menú según el rol del usuario.
    """
    if not request.user.is_authenticated:
        return {'menu_items': []}
    
    user = request.user
    menu_items = user.role.get_menu()
        
    return {'menu_items': menu_items}