from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Reporte, Imagen, Comentario

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display  = ['titulo', 'categoria', 'estado_badge', 'usuario', 'fecha_creacion']
    list_filter   = ['estado', 'categoria', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion', 'usuario__username']
    readonly_fields = ['fecha_creacion', 'usuario']

    def estado_badge(self, obj):
        colores = {
            'pendiente':   '#ffc107',
            'en_revision': '#0dcaf0',
            'resuelto':    '#198754',
        }
        color = colores.get(obj.estado, '#ccc')
        return format_html(
            '<span style="background:{};padding:3px 10px;border-radius:12px;font-size:12px;color:#000">{}</span>',
            color, obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'icono']

admin.site.register(Imagen)
admin.site.register(Comentario)

admin.site.site_header = 'Panel Municipal — Reportes Ciudadanos'
admin.site.site_title  = 'Reportes Ciudadanos'
admin.site.index_title = 'Gestión de reportes'