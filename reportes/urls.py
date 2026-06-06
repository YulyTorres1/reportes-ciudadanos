from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('',                      views.inicio,          name='inicio'),
    path('crear/',                views.crear_reporte,   name='crear'),
    path('reporte/<int:pk>/',     views.detalle_reporte, name='detalle'),
    path('dashboard/',            views.dashboard,       name='dashboard'),
    path('registro/',             views.registro,        name='registro'),
    path('login/',                views.login_view,      name='login'),
    path('logout/',               views.logout_view,     name='logout'),
    path('mis-reportes/',         views.mis_reportes,    name='mis_reportes'),
    path('reporte/<int:pk>/cambiar-estado/', views.cambiar_estado, name='cambiar_estado'),
]