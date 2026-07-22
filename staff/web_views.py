from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from core.views import obtener_contexto_base

from .forms import PersonalMedicoForm
from .models import PersonalMedico


@login_required
def personal_lista(request):
    busqueda = request.GET.get(
        "buscar",
        "",
    ).strip()

    estado_turno = request.GET.get(
        "turno",
        "",
    ).strip()

    personal = PersonalMedico.objects.select_related(
        "user"
    ).order_by(
        "user__first_name",
        "user__last_name",
        "user__username",
    )

    if busqueda:
        personal = personal.filter(
            Q(user__first_name__icontains=busqueda)
            | Q(user__last_name__icontains=busqueda)
            | Q(user__username__icontains=busqueda)
            | Q(user__email__icontains=busqueda)
            | Q(especialidad__icontains=busqueda)
            | Q(registro_medico__icontains=busqueda)
        )

    if estado_turno == "activo":
        personal = personal.filter(en_turno=True)

    elif estado_turno == "inactivo":
        personal = personal.filter(en_turno=False)

    total_personal = personal.count()

    total_en_turno = personal.filter(
        en_turno=True
    ).count()

    total_fuera_turno = personal.filter(
        en_turno=False
    ).count()

    total_especialidades = (
        personal.exclude(especialidad="")
        .values("especialidad")
        .distinct()
        .count()
    )

    paginador = Paginator(
        personal,
        10,
    )

    numero_pagina = request.GET.get("page")

    pagina = paginador.get_page(
        numero_pagina
    )

    contexto = obtener_contexto_base(
        request.user
    )

    contexto.update(
        {
            "pagina": pagina,
            "personal": pagina.object_list,
            "busqueda": busqueda,
            "estado_turno": estado_turno,
            "total_personal": total_personal,
            "total_en_turno": total_en_turno,
            "total_fuera_turno": total_fuera_turno,
            "total_especialidades": total_especialidades,
        }
    )

    return render(
        request,
        "staff/personal_lista.html",
        contexto,
    )


@login_required
def personal_crear(request):
    if request.method == "POST":
        formulario = PersonalMedicoForm(
            request.POST
        )

        if formulario.is_valid():
            personal = formulario.save()

            messages.success(
                request,
                (
                    "El miembro del personal médico "
                    "fue registrado correctamente."
                ),
            )

            return redirect(
                "personal_detalle",
                personal_id=personal.id,
            )

    else:
        formulario = PersonalMedicoForm()

    contexto = obtener_contexto_base(
        request.user
    )

    contexto.update(
        {
            "formulario": formulario,
            "titulo": "Registrar personal médico",
            "texto_boton": "Guardar personal",
        }
    )

    return render(
        request,
        "staff/personal_formulario.html",
        contexto,
    )


@login_required
def personal_detalle(request, personal_id):
    personal = get_object_or_404(
        PersonalMedico.objects.select_related(
            "user"
        ),
        id=personal_id,
    )

    contexto = obtener_contexto_base(
        request.user
    )

    contexto.update(
        {
            "personal": personal,
        }
    )

    return render(
        request,
        "staff/personal_detalle.html",
        contexto,
    )


@login_required
def personal_editar(request, personal_id):
    personal = get_object_or_404(
        PersonalMedico,
        id=personal_id,
    )

    if request.method == "POST":
        formulario = PersonalMedicoForm(
            request.POST,
            instance=personal,
        )

        if formulario.is_valid():
            personal = formulario.save()

            messages.success(
                request,
                (
                    "La información del personal "
                    "fue actualizada correctamente."
                ),
            )

            return redirect(
                "personal_detalle",
                personal_id=personal.id,
            )

    else:
        formulario = PersonalMedicoForm(
            instance=personal
        )

    contexto = obtener_contexto_base(
        request.user
    )

    contexto.update(
        {
            "formulario": formulario,
            "personal": personal,
            "titulo": "Editar personal médico",
            "texto_boton": "Guardar cambios",
        }
    )

    return render(
        request,
        "staff/personal_formulario.html",
        contexto,
    )


@login_required
def personal_eliminar(request, personal_id):
    personal = get_object_or_404(
        PersonalMedico.objects.select_related(
            "user"
        ),
        id=personal_id,
    )

    if request.method == "POST":
        nombre = (
            personal.user.get_full_name()
            or personal.user.username
        )

        personal.delete()

        messages.success(
            request,
            (
                f"{nombre} fue eliminado "
                "del personal médico."
            ),
        )

        return redirect("medicos")

    contexto = obtener_contexto_base(
        request.user
    )

    contexto.update(
        {
            "personal": personal,
        }
    )

    return render(
        request,
        "staff/personal_eliminar.html",
        contexto,
    )