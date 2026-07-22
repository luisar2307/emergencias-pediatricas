from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import PacienteForm
from .models import Paciente


@login_required
def paciente_crear(request):
    if request.method == "POST":
        form = PacienteForm(
            request.POST
        )

        if form.is_valid():
            paciente = form.save()

            messages.success(
                request,
                (
                    f"Paciente {paciente.nombre} "
                    f"{paciente.apellido} registrado correctamente."
                ),
            )

            return redirect(
                "paciente_detalle",
                paciente_id=paciente.id,
            )
    else:
        form = PacienteForm()

    return render(
        request,
        "core/paciente_form.html",
        {
            "form": form,
            "titulo": "Registrar paciente",
            "subtitulo": (
                "Complete la información personal y clínica."
            ),
            "texto_boton": "Guardar paciente",
        },
    )


@login_required
def paciente_detalle(request, paciente_id):
    paciente = get_object_or_404(
        Paciente,
        id=paciente_id,
    )

    return render(
        request,
        "core/paciente_detalle.html",
        {
            "paciente": paciente,
        },
    )


@login_required
def paciente_editar(request, paciente_id):
    paciente = get_object_or_404(
        Paciente,
        id=paciente_id,
    )

    if request.method == "POST":
        form = PacienteForm(
            request.POST,
            instance=paciente,
        )

        if form.is_valid():
            paciente = form.save()

            messages.success(
                request,
                "Los datos del paciente fueron actualizados.",
            )

            return redirect(
                "paciente_detalle",
                paciente_id=paciente.id,
            )
    else:
        form = PacienteForm(
            instance=paciente
        )

    return render(
        request,
        "core/paciente_form.html",
        {
            "form": form,
            "paciente": paciente,
            "titulo": "Editar paciente",
            "subtitulo": (
                "Actualice los datos necesarios."
            ),
            "texto_boton": "Guardar cambios",
        },
    )


@login_required
def paciente_eliminar(request, paciente_id):
    paciente = get_object_or_404(
        Paciente,
        id=paciente_id,
    )

    if request.method == "POST":
        nombre = (
            f"{paciente.nombre} "
            f"{paciente.apellido}"
        )

        paciente.delete()

        messages.success(
            request,
            f"El paciente {nombre} fue eliminado.",
        )

        return redirect(
            "pacientes"
        )

    return render(
        request,
        "core/paciente_confirmar_eliminar.html",
        {
            "paciente": paciente,
        },
    )