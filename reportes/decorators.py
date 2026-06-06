from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def solo_staff(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('reportes:login')
        if not request.user.is_staff:
            messages.error(request, 'No tienes permiso para acceder a esta sección.')
            return redirect('reportes:inicio')
        return view_func(request, *args, **kwargs)
    return wrapper

def login_requerido(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Debes iniciar sesión para continuar.')
            return redirect(f'/login/?next={request.path}')
        return view_func(request, *args, **kwargs)
    return wrapper