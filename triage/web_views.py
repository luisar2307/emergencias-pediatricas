from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from core.views import obtener_contexto_base

from .forms import TriajeForm
from .models import Triaje


@login_required
def triaje_lista(request):
    busqueda = request.GET.get("buscar", "").strip()
    nivel = request.GET.get("nivel", "").strip()

    registros = Triaje.objects.select_related(
        "paciente",
        "personal",
    ).order_by("-fecha_registro")

    if busqueda:
        registros = registros.filter(
            Q(paciente__nombre__icontains=busqueda)
            | Q(paciente__apellido__icontains=busqueda)
            | Q(paciente__historia_clinica__icontains=busqueda)
        )

    if nivel:
        registros = registros.filter(nivel_urgencia=nivel)

    total_triajes = registros.count()
    total_criticos = registros.filter(
        nivel_urgencia=Triaje.URGENCIA_CRITICO
    ).count()
    total_urgentes = registros.filter(
        nivel_urgencia=Triaje.URGENCIA_URGENTE
    ).count()
    total_moderados = registros.filter(
        nivel_urgencia=Triaje.URGENCIA_MODERADO
    ).count()
    total_normales = registros.filter(
        nivel_urgencia=Triaje.URGENCIA_NORMAL
    ).count()

    paginador = Paginator(registros, 10)
    numero_pagina = request.GET.get("page")
    pagina = paginador.get_page(numero_pagina)

    contexto = obtener_contexto_base(request.user)

    contexto.update(
        {
            "pagina": pagina,
            "triajes": pagina.object_list,
            "busqueda": busqueda,
            "nivel_seleccionado": nivel,
            "niveles": Triaje.URGENCIA_CHOICES,
            "total_triajes": total_triajes,
            "total_criticos": total_criticos,
            "total_urgentes": total_urgentes,
            "total_moderados": total_moderados,
            "total_normales": total_normales,
        }
    )

    return render(
        request,
        "triage/triaje_lista.html",
        contexto,
    )


@login_required
def triaje_crear(request):
    if request.method == "POST":
        formulario = TriajeForm(request.POST)

        if formulario.is_valid():
            triaje = formulario.save()

            messages.success(
                request,
                (
                    "El triaje fue registrado correctamente. "
                    f"Nivel asignado: {triaje.get_nivel_urgencia_display()}."
                ),
            )

            return redirect(
                "triaje_detalle",
                triaje_id=triaje.id,
            )
    else:
        formulario = TriajeForm()

    contexto = obtener_contexto_base(request.user)

    contexto.update(
        {
            "formulario": formulario,
            "titulo": "Registrar triaje",
            "texto_boton": "Guardar triaje",
        }
    )

    return render(
        request,
        "triage/triaje_formulario.html",
        contexto,
    )


@login_required
def triaje_detalle(request, triaje_id):
    triaje = get_object_or_404(
        Triaje.objects.select_related(
            "paciente",
            "personal",
        ),
        id=triaje_id,
    )

    contexto = obtener_contexto_base(request.user)

    contexto.update(
        {
            "triaje": triaje,
        }
    )

    return render(
        request,
        "triage/triaje_detalle.html",
        contexto,
    )


@login_required
def triaje_editar(request, triaje_id):
    triaje = get_object_or_404(
        Triaje,
        id=triaje_id,
    )

    if request.method == "POST":
        formulario = TriajeForm(
            request.POST,
            instance=triaje,
        )

        if formulario.is_valid():
            triaje = formulario.save()

            messages.success(
                request,
                (
                    "El triaje fue actualizado correctamente. "
                    f"Nivel actual: {triaje.get_nivel_urgencia_display()}."
                ),
            )

            return redirect(
                "triaje_detalle",
                triaje_id=triaje.id,
            )
    else:
        formulario = TriajeForm(instance=triaje)

    contexto = obtener_contexto_base(request.user)

    contexto.update(
        {
            "formulario": formulario,
            "triaje": triaje,
            "titulo": "Editar triaje",
            "texto_boton": "Guardar cambios",
        }
    )

    return render(
        request,
        "triage/triaje_formulario.html",
        contexto,
    )


@login_required
def triaje_eliminar(request, triaje_id):
    triaje = get_object_or_404(
        Triaje.objects.select_related("paciente"),
        id=triaje_id,
    )

    if request.method == "POST":
        paciente = str(triaje.paciente)
        triaje.delete()

        messages.success(
            request,
            f"El triaje de {paciente} fue eliminado correctamente.",
        )

        return redirect("triaje")

    contexto = obtener_contexto_base(request.user)

    contexto.update(
        {
            "triaje": triaje,
        }
    )

    return render(
        request,
        "triage/triaje_eliminar.html",
        contexto,
    )