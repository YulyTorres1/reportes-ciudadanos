from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import Reporte, Categoria, Comentario
from .forms import ReporteForm, ImagenForm, ComentarioForm
from .decorators import solo_staff, login_requerido


# ─── Autenticación ────────────────────────────────────────────────────────────

def registro(request):
    if request.user.is_authenticated:
        return redirect('reportes:inicio')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}! Tu cuenta fue creada exitosamente.')
            return redirect('reportes:inicio')
    else:
        form = UserCreationForm()
    return render(request, 'reportes/registro.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('reportes:inicio')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'reportes:inicio')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'reportes/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('reportes:inicio')


# ─── Vistas públicas ──────────────────────────────────────────────────────────

def inicio(request):
    reportes = Reporte.objects.select_related('categoria', 'usuario').all()
    categorias = Categoria.objects.all()

    categoria_id = request.GET.get('categoria')
    estado = request.GET.get('estado')
    busqueda = request.GET.get('q')

    if categoria_id:
        reportes = reportes.filter(categoria_id=categoria_id)
    if estado:
        reportes = reportes.filter(estado=estado)
    if busqueda:
        reportes = reportes.filter(titulo__icontains=busqueda)

    total       = Reporte.objects.count()
    pendientes  = Reporte.objects.filter(estado='pendiente').count()
    en_revision = Reporte.objects.filter(estado='en_revision').count()
    resueltos   = Reporte.objects.filter(estado='resuelto').count()

    return render(request, 'reportes/inicio.html', {
        'reportes':    reportes,
        'categorias':  categorias,
        'total':       total,
        'pendientes':  pendientes,
        'en_revision': en_revision,
        'resueltos':   resueltos,
    })


def detalle_reporte(request, pk):
    reporte = get_object_or_404(Reporte, pk=pk)
    comentario_form = ComentarioForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('reportes:login')
        comentario_form = ComentarioForm(request.POST)
        if comentario_form.is_valid():
            c = comentario_form.save(commit=False)
            c.reporte = reporte
            c.usuario = request.user
            c.save()
            return redirect('reportes:detalle', pk=pk)
    return render(request, 'reportes/detalle_reporte.html', {
        'reporte':         reporte,
        'comentario_form': comentario_form,
    })


# ─── Ciudadano ────────────────────────────────────────────────────────────────

@login_requerido
def crear_reporte(request):
    if request.method == 'POST':
        form        = ReporteForm(request.POST)
        imagen_form = ImagenForm(request.POST, request.FILES)
        if form.is_valid():
            reporte         = form.save(commit=False)
            reporte.usuario = request.user
            reporte.save()
            try:
                if imagen_form.is_valid() and imagen_form.cleaned_data.get('archivo'):
                    img         = imagen_form.save(commit=False)
                    img.reporte = reporte
                    img.save()
            except Exception as e:
                messages.warning(request, f'Reporte creado pero hubo un problema con la imagen: {e}')
            messages.success(request, '¡Reporte enviado exitosamente!')
            return redirect('reportes:detalle', pk=reporte.pk)
    else:
        form        = ReporteForm()
        imagen_form = ImagenForm()
    return render(request, 'reportes/crear_reporte.html', {
        'form':        form,
        'imagen_form': imagen_form,
    })


@login_requerido
def mis_reportes(request):
    reportes = Reporte.objects.filter(usuario=request.user).select_related('categoria')
    return render(request, 'reportes/mis_reportes.html', {'reportes': reportes})


# ─── Funcionario / Admin ──────────────────────────────────────────────────────

@solo_staff
def dashboard(request):
    total       = Reporte.objects.count()
    pendientes  = Reporte.objects.filter(estado='pendiente').count()
    en_revision = Reporte.objects.filter(estado='en_revision').count()
    resueltos   = Reporte.objects.filter(estado='resuelto').count()

    por_categoria = Reporte.objects.values(
        'categoria__nombre', 'categoria__icono'
    ).annotate(total=Count('id')).order_by('-total')

    ultimos = Reporte.objects.select_related('categoria', 'usuario').order_by('-fecha_creacion')[:8]

    porcentaje_resueltos = round((resueltos / total * 100), 1) if total > 0 else 0

    return render(request, 'reportes/dashboard.html', {
        'total':               total,
        'pendientes':          pendientes,
        'en_revision':         en_revision,
        'resueltos':           resueltos,
        'por_categoria':       por_categoria,
        'ultimos':             ultimos,
        'porcentaje_resueltos': porcentaje_resueltos,
    })


@solo_staff
def cambiar_estado(request, pk):
    reporte = get_object_or_404(Reporte, pk=pk)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in ['pendiente', 'en_revision', 'resuelto']:
            reporte.estado = nuevo_estado
            reporte.save()
            messages.success(request, f'Estado actualizado a "{reporte.get_estado_display()}".')
    return redirect('reportes:detalle', pk=pk)
def error_403(request, exception=None):
    return render(request, '403.html', status=403)