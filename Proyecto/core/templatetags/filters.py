from django import template

register = template.Library()

@register.filter
def format_phone(value:str):
    """Formatea un número de teléfono en formato 3 3 4"""
    if not value:
        return ''
    
    phone_str = value.strip()
    
    phone_str = phone_str.replace(' ', '').replace('-', '')
    
    if len(phone_str) >= 10:
        return f"{phone_str[:3]} {phone_str[3:6]} {phone_str[6:]}"
    
    return phone_str