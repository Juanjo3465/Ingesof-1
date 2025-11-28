from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.cache import never_cache

@require_GET
@never_cache
def verify_session(request):
    """Endpoint para verificar si la sesión sigue activa"""
    return JsonResponse({
        'authenticated': request.user.is_authenticated
    })