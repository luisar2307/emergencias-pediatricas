from rest_framework.permissions import BasePermission, SAFE_METHODS


def is_medico(user):
    return getattr(user, 'rol', None) == 'medico'


def is_enfermero(user):
    return getattr(user, 'rol', None) == 'enfermero'


def is_recepcion(user):
    return getattr(user, 'rol', None) == 'recepcion'


def is_admin(user):
    return getattr(user, 'rol', None) == 'admin'


class RolPermission(BasePermission):

    def has_permission(self, request, view):

        user = request.user

        if not user or not user.is_authenticated:
            return False

        view_name = view.__class__.__name__
        action = getattr(view, 'action', None)

        if view_name == 'UsuarioViewSet':
            return self._has_usuario_permission(user, action)

        if view_name == 'PersonalMedicoViewSet':
            return self._has_personal_medico_permission(user, action)

        if view_name == 'PacienteViewSet':
            return self._has_paciente_permission(user, action)

        if view_name == 'TutorViewSet':
            return self._has_tutor_permission(user, action)

        if view_name == 'TriajeViewSet':
            return self._has_triaje_permission(user, action)

        return False


    def has_object_permission(self, request, view, obj):

        user = request.user

        if is_admin(user):
            return True

        return True



    # ==========================
    # USUARIOS
    # ==========================

    def _has_usuario_permission(self, user, action):

        if action == 'list':
            return is_admin(user)

        if action == 'create':
            return is_admin(user)

        if action in ['retrieve', 'update', 'partial_update']:
            return is_admin(user)

        if action == 'destroy':
            return is_admin(user)

        return False



    # ==========================
    # PERSONAL MEDICO
    # ==========================

    def _has_personal_medico_permission(self, user, action):

        if action in ['list', 'retrieve']:
            return (
                is_admin(user)
                or is_medico(user)
                or is_enfermero(user)
            )

        if action == 'create':
            return is_admin(user)

        if action in ['update', 'partial_update']:
            return is_admin(user)

        if action == 'destroy':
            return is_admin(user)

        return False



    # ==========================
    # PACIENTES
    # ==========================

    def _has_paciente_permission(self, user, action):

        if action in ['list', 'retrieve']:
            return (
                is_admin(user)
                or is_recepcion(user)
                or is_medico(user)
                or is_enfermero(user)
            )


        if action == 'create':
            return (
                is_admin(user)
                or is_recepcion(user)
            )


        if action in ['update', 'partial_update']:
            return (
                is_admin(user)
                or is_recepcion(user)
            )


        if action == 'destroy':
            return is_admin(user)


        if action == 'agregar_tutor':
            return (
                is_admin(user)
                or is_recepcion(user)
            )


        if action == 'tutores':
            return (
                is_admin(user)
                or is_recepcion(user)
                or is_medico(user)
                or is_enfermero(user)
            )


        return False



    # ==========================
    # TUTORES
    # ==========================

    def _has_tutor_permission(self, user, action):

        if action in ['list', 'retrieve']:
            return (
                is_admin(user)
                or is_recepcion(user)
                or is_medico(user)
                or is_enfermero(user)
            )


        if action in ['create', 'update', 'partial_update']:
            return (
                is_admin(user)
                or is_recepcion(user)
            )


        if action == 'destroy':
            return is_admin(user)


        return False



    # ==========================
    # TRIAJE
    # ==========================

    def _has_triaje_permission(self, user, action):

        if action in ['list', 'retrieve']:
            return (
                is_admin(user)
                or is_medico(user)
                or is_enfermero(user)
            )


        if action in ['create', 'update', 'partial_update']:
            return (
                is_admin(user)
                or is_medico(user)
                or is_enfermero(user)
            )


        if action == 'destroy':
            return is_admin(user)


        return False