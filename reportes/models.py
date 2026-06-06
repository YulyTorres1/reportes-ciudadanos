from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    icono  = models.CharField(max_length=50, default='📍')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Categorías'


class Reporte(models.Model):

    ESTADO_CHOICES = [
        ('pendiente',   'Pendiente'),
        ('en_revision', 'En revisión'),
        ('resuelto',    'Resuelto'),
    ]

    titulo        = models.CharField(max_length=200)
    descripcion   = models.TextField()
    estado        = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    latitud       = models.FloatField(null=True, blank=True)
    longitud      = models.FloatField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario       = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria     = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.titulo} — {self.get_estado_display()}'

    class Meta:
        ordering = ['-fecha_creacion']


class Imagen(models.Model):
    reporte = models.ForeignKey(Reporte, on_delete=models.CASCADE, related_name='imagenes')
    archivo = models.ImageField(upload_to='reportes/')

    def __str__(self):
        return f'Imagen de {self.reporte.titulo}'


class Comentario(models.Model):
    reporte   = models.ForeignKey(Reporte, on_delete=models.CASCADE, related_name='comentarios')
    usuario   = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.usuario.username} en {self.reporte.titulo}'

    class Meta:
        ordering = ['fecha']