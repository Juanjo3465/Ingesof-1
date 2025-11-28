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