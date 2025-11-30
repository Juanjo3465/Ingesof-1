class ApartmentFilter:
    """Filtro reutilizable para búsqueda de apartamentos"""
    
    FILTROS = {
        'propietario_email': ('id_propietario__correo__icontains', str),
        'interior': ('interior', int),
        'torre': ('torre', int),
        'numero': ('numero', int),
    }
    
    def __init__(self, queryset, params):
        self.queryset = queryset
        self.params = params
    
    def apply(self):
        for param, (lookup, cast) in self.FILTROS.items():
            if value := self.params.get(param):
                try:
                    self.queryset = self.queryset.filter(**{lookup: cast(value)})
                except (ValueError, TypeError):
                    continue  
        
        return self.queryset