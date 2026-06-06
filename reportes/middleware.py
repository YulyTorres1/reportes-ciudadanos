from django.shortcuts import redirect
from django.urls import reverse

RUTAS_STAFF = ['/dashboard/', '/admin/']

class RolMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        for ruta in RUTAS_STAFF:
            if request.path.startswith(ruta) and not request.user.is_staff:
                if request.user.is_authenticated:
                    return redirect('reportes:inicio')
                return redirect('reportes:login')
        return self.get_response(request)